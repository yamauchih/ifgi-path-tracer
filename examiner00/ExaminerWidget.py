#!/usr/bin/env python
#
# Examiner version 0.0.0
#
# \author Yamauchi, Hitoshi
#

"""IFGI Examiner Version 0.0.0"""

import sys
import math
import OpenGL
import numpy

from PyQt4  import QtCore, QtGui, QtOpenGL
from OpenGL import GL
from OpenGL import GLU


import enum
import ifgimath
import Camera

#
# Examiner's action mode
#
ActionMode = enum.Enum(['ExamineMode', 'PickingMode'])

#
# 2d point to 3d point map
#
# \param[in]  _point2d point in a window coordinate
# \param[in]  _win_width  window width
# \param[in]  _win_height window height
# \return pos3d, position on a sphere
def mapToSphere(_win_point2d, _win_width, _win_height):
    assert(_win_width  > 0)
    assert(_win_height > 0)

    wx = float(_win_point2d.x())
    wy = float(_win_point2d.y())

    # check _win_point2d is in range
    if ((wx < 0) or (wx >= _win_width) or (wy < 0) or (wy >= _win_height)):
        raise StandardError, ('out of range coordinate [' + str(wx) + ',' + str(wy) +
                              '] should be in [' +
                              str(_win_width) + ',' + str(_win_height) + ']')

    # get window normalized relative to center coordinate
    rel_x = (wx - (_win_width  / 2)) / _win_width
    rel_y = (wx - (_win_height / 2)) / _win_height

    # get
    sinx       = math.sin(math.pi * rel_x * 0.5);
    siny       = math.sin(math.pi * rel_y * 0.5);
    sinx2siny2 = sinx * sinx + siny * siny;

    z = 0
    if sinx2siny2 < 1:
        z = math.sqrt(1 - sinx2siny2)

    pos3d = numpy.array([sinx, siny, z])

    return pos3d

#
# Scene examiner
#
class ExaminerWidget(QtOpenGL.QGLWidget):
    def __init__(self, parent=None):
        QtOpenGL.QGLWidget.__init__(self, parent)

        # cameras FIXME scenegraph should have the camera
        self.gl_camera   = Camera.GLCamera()
        # self.ifgi_camera = Camera.IFGICamera()

        # OpenGL scene graph
        self.gl_scenegraph = None

        # FIXME remove below...
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0
        self.lastPos = QtCore.QPoint()


        # mouse points
        self.lastPoint2D = QtCore.QPoint()
        self.lastPoint3D = numpy.array([0, 0, 0]) # z == 0, not hit to the trackball sphere

        # draw mode
        self.global_draw_mode = 0

        # action mode
        self.actionMode = ActionMode.ExamineMode
        self.isRotating = False

        # SceneGraph coordinate
        self.scene_cog = numpy.array([0,0,0])

        # window info
        self.width  = 1
        self.height = 1

        # some debug facility
        self.is_debug = False


    def xRotation(self):
        return self.xRot

    def yRotation(self):
        return self.yRot

    def zRotation(self):
        return self.zRot

    def minimumSizeHint(self):
        return QtCore.QSize(50, 50)

    def sizeHint(self):
        return QtCore.QSize(400, 400)

    def setXRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.xRot:
            self.xRot = angle
            # self.emit(QtCore.SIGNAL("xRotationChanged(int)"), angle)
            self.updateGL()

    def setYRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.yRot:
            self.yRot = angle
            # self.emit(QtCore.SIGNAL("yRotationChanged(int)"), angle)
            self.updateGL()

    def setZRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.zRot:
            self.zRot = angle
            # self.emit(QtCore.SIGNAL("zRotationChanged(int)"), angle)
            self.updateGL()

    # Window info: width
    def glWidth(self):
        return self.width

    # Window info: height
    def glHeight(self):
        return self.height


    # initialize open GL
    def initializeGL(self):
        bgblack = QtGui.QColor(0, 0, 0, 255)
        self.qglClearColor(bgblack)
        GL.glShadeModel(GL.GL_FLAT)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_CULL_FACE)

    # paint
    def paintGL(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        GL.glLoadIdentity()

        ep = self.gl_camera.eye_pos  # eye pos
        vd = self.gl_camera.view_dir # lookat point
        up = self.gl_camera.up_dir   # up vector
        GLU.gluLookAt(ep[0], ep[1], ep[2],
                      vd[0], vd[1], vd[2],
                      up[0], up[1], up[2])

        GL.glRotated(self.xRot / 16.0, 1.0, 0.0, 0.0)
        GL.glRotated(self.yRot / 16.0, 0.0, 1.0, 0.0)
        GL.glRotated(self.zRot / 16.0, 0.0, 0.0, 1.0)
        self.draw_scene()

    # resize
    def resizeGL(self, width, height):
        self.width  = width
        self.height = height

        side = min(width, height)

        GL.glViewport((width - side) / 2, (height - side) / 2, side, side)

        # perspective is for projection matrix
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()

        # DEBUG: self.gl_camera.print_obj()
        GLU.gluPerspective(self.gl_camera.get_fov() * 180 /math.pi,
                           self.gl_camera.get_aspect_ratio(),
                           self.gl_camera.get_z_near(),
                           self.gl_camera.get_z_far())
        GL.glMatrixMode(GL.GL_MODELVIEW)


    # translate the camera
    def translate(self, _trans):
        print 'NIN: translate(self, _trans):'
#         SceneGraph::Camera::Vec3 ex, ey, ez;
#         d_camera.coordinateSystem(ex,ey,ez);
#         SceneGraph::Camera::Vec3 t=ex*_trans[0]+ey*_trans[1]-ez*_trans[2];
#         d_camera.lock();
#         d_camera.eye(d_camera.eye()-t);
#         d_camera.unlock();


    # rotate the camera with an axis
    #
    # \param[in] _angle   degree
    # \param[in] _pn_axis rotate axis
    def rotate_camera(self, _angle, _pn_axis):
        cam_basis = self.gl_camera.getCoordinateSystem()
        rotation = numpy.identity(4)

        eyepos = self.gl_camera.get_eye_pos() - self.scene_cog
        # Here z is '-', since OpenGL is left hand side coordinates.
        print 'mat:'      + str(rotation)
        print 'CamBasis:' + str(cam_basis)
        print 'pn_axis:'  + str(_pn_axis)

        rmat = ifgimath.get_rotation_mat(-_angle,
                                          cam_basis[0] * _pn_axis[0] +
                                          cam_basis[1] * _pn_axis[1] -
                                          cam_basis[2] * _pn_axis[2]);
        

        # make 4d vector for homogeneous coordinate
        eyepos[3] = 1.0         # HEREHERE 2010-11-10(Wed)
        eyepos = rmat * eyepos + self.scene_cog

        # self.gl_camera.lock();
        self.gl_camera.set_eyepos(eyepos)
        self.gl_camera.set_viewdir(rotation.transformVector(d_camera.viewingDirection()),
                                   rotation.transformVector(d_camera.up()));
        # self.gl_camera.unlock();


    # mouse press event
    #   - right: popup menu
    #   - left:  camera move
    def mousePressEvent(self, _event):
        # press right button: popup menu
        if (_event.buttons() & QtCore.Qt.RightButton):
            #      // lazy update of menu
            #      d_availDrawModes.checkQtPopupMenu(d_popupMenu,d_curDrawMode);

            #      QtMenuData::Item* item;
            #      if ((item=d_popupMenu->item("functions"))!=0) {
            #          QtPopupMenu* functions=item->qtPopupMenu();

            #      if (functions!=0) {
            #          if ((item=functions->item("animation"))!=0)
            #              item->setChecked(d_animation);
            #          if ((item=functions->item("backface-culling"))!=0)
            #              item->setChecked(d_backFaceMode==BACK_CULL);
            #      }
            #  }

            #  d_popupMenu->exec(QCursor::pos().x(),QCursor::pos().y());
            print 'NIN: RightButtonPressed: popup menu'
        else:
            # left button & CTRL pressed and lasso interactive
            if ((_event.modifiers() & QtCore.Qt.ControlModifier) and
                (_event.button() == QtCore.Qt.LeftButton)        and
                (self.actionMode == Actionmode.ExamineMode)):
                # avoid control key being useless for other modes
                # self.startDrag()
                pass

            elif (self.actionMode == ActionMode.ExamineMode):
                # remember this point
                self.lastPoint2D = _event.pos()
                self.lastPoint3D = mapToSphere(self.lastPoint2D,
                                               self.glWidth(), self.glHeight())

                self.isRotating = True
                print 'DEBUG: mouse press at ' + str(self.lastPoint2D) +\
                    ', on spehere: ' + str(self.lastPoint3D)


            # elif (self.actionMode == Actionmode.FlyToMode):
            #       flyTo(_event->pos(), _event->button()==QtCore.Qt.MidButton);
            #   elif (self.actionMode == Actionmode.PickingMode):
            #       emit signalMouseEvent(_event);
            #       # same for SceneGraph
            #       SceneGraph::ObservableActor_Event arg(ArgumentType::MousePressed);
            #       arg.x=_event->x();
            #       arg.y=_event->y();
            #       buttonState(_event,arg.button,arg.stateBefore,arg.stateAfter);

            #       notify(arg)
            #       ioProcessDetachRequests();

            #   elif (self.actionMode == Actionmode.LassoMode):
            #       #  give event to built-in lasso
            #       d_lasso->slotDrawLasso(_event);

            #   elif (self.actionMode == Actionmode.QuestionMode):
            #       # give event to application
            #       emit signalMouseEventIdentify(_event);
            #       # // same for SceneGraph
            #       SceneGraph::ObservableActor_Event arg(ArgumentType::MousePressed);
            #       arg.x=_event->x();
            #       arg.y=_event->y();
            #       buttonState(_event,arg.button,arg.stateBefore,arg.stateAfter);

            #       notify(arg)
            #       ioProcessDetachRequests()



    # ExamineMode: move in z direction
    def examineModeMoveZdir(self):
        # move in z direction
        #   if (d_camera.projectionMode() == Camera.ProjectionMode.Perspective):
        #       value_y = d_radius * ((newPoint2D.y() - d_lastPoint2D.y()))
        #       * 3.0 / (float) glHeight();
        #       translate( base::Vec3f(0.0, 0.0, value_y) );
        #   elif (d_camera.projectionMode() == Camera.ProjectionMode.Orthographic):
        #       value_y = ((newPoint2D.y() - d_lastPoint2D.y()))
        #       * d_camera.orthoWidth() / (float) glHeight();
        #       d_camera.orthoWidth(d_camera.orthoWidth()-value_y);
        #   else:
        #       raise StandardError, ('no such projection mode')
        pass

    # ExamineMode: move in x,y direction
    def examineModeMoveXYdir(self):
        #        value_x = d_radius * ((newPoint2D.x() - d_lastPoint2D.x()))
        #            * 2.0 / (double) glWidth();
        #        value_y = d_radius * ((newPoint2D.y() - d_lastPoint2D.y()))
        #            * 2.0 / (double) glHeight();
        #        translate( base::Vec3f(value_x, -value_y, 0.0) );
        pass

    # ExamineMode: Pick
    def examineModePick(self):
        # case PickingMode:
        # if (inside) { // give event to application
        #     emit signalMouseEvent(_event);
        #     // same for SceneGraph
        #     SceneGraph::ObservableActor_Event arg(ArgumentType::MouseMoved);
        #     arg.x=_event.x();
        #     arg.y=_event.y();
        #     buttonState(_event,arg.button,arg.stateBefore,arg.stateAfter);
        #     notify(arg); ioProcessDetachRequests();
        # }
        pass

    # ExamineMode: Question
    def examineModeQuestion(self):
        # case QuestionMode:
        #    if (inside) { // give event to application
        #        emit signalMouseEventIdentify(_event);
        #        // same for SceneGraph
        #        SceneGraph::ObservableActor_Event arg(ArgumentType::MouseMoved);
        #        arg.x=_event.x();
        #        arg.y=_event.y();
        #        buttonState(_event,arg.button,arg.stateBefore,arg.stateAfter);
        
        #        notify(arg); ioProcessDetachRequests();
        #    }
        pass


    # ExamineMode: Rotate Trackball
    #
    # \param[in] _qpoint2D current mouse 2D point
    def examineModeRotateTrackball(self, _qpoint2D):
        if (self.lastPoint3D[2] != 0): # z == 0 ... not hit on sphere
            newPoint3D = mapToSphere(_qpoint2D, self.glWidth(), self.glHeight())
            if (newPoint3D[2] != 0): # point hits the sphere
                rot_axis  = numpy.outer(self.lastPoint3D, newPoint3D)
                cos_angle = numpy.inner(self.lastPoint3D, newPoint3D)
                if (math.fabs(cos_angle) < 1.0):
                    angle = math.acos(cos_angle); # radian
                    angle *= 2.0; # inventor rotation

                self.rotate_camera(angle, rot_axis)

            self.lastRotationAxis  = rot_axis;
            self.lastRotationAngle = angle;


    # mouse move event
    #  - Right drag: context menu
    #  - Left  drag: context menu
    def mouseMoveEvent(self, _event):
        if ((_event.button() != QtCore.Qt.RightButton) or
            ((self.actionMode == PickingMode))): # && !d_popupEnabled) ) {

            newPoint2D = _event.pos()
            isInside = ((newPoint2D.x() >=0 ) and (newPoint2D.x() <= self.glWidth()) and
                        (newPoint2D.y() >=0 ) and (newPoint2D.y() <= self.glHeight()))
            print 'is inside = ' + str(isInside)

            if  (self.actionMode == ActionMode.PickingMode):
                self.examineModePick()
            # elif (self.actionMode == ActionMode.LassoMode):
            #     pass
            # elif (self.actionMode == ActionMode.QuestionMode):
            #     pass
            elif (self.actionMode == ActionMode.ExamineMode):
                if (not isInside):
                    return      # do nothing if mouse is outside of the window

                newPoint3D = mapToSphere(newPoint2D, self.glWidth(), self.glHeight());
                # makeCurrent()?

                if ((_event.buttons() & QtCore.Qt.LeftButton) and
                    (_event.buttons() & QtCore.Qt.MidButton)):
                    self.examineModeMoveZdir()
                elif (_event.buttons() & QtCore.Qt.MidButton):
                    self.examineModeMoveXYdir()
                elif (_event.buttons() & QtCore.Qt.LeftButton):
                    self.examineModeRotateTrackball(newPoint2D)

                self.lastPoint2D = newPoint2D;
                self.lastPoint3D = newPoint3D;

            # updateGL();
            # d_lastMoveTime.restart();

        # original old code
        # dx = _event.x() - self.lastPos.x()
        # dy = _event.y() - self.lastPos.y()
        # if _event.buttons() & QtCore.Qt.LeftButton:
        #     self.setXRotation(self.xRot + 8 * dy)
        #     self.setYRotation(self.yRot + 8 * dx)
        # elif _event.buttons() & QtCore.Qt.RightButton:
        #     self.setXRotation(self.xRot + 8 * dy)
        #     self.setZRotation(self.zRot + 8 * dx)
        # self.lastPos = QtCore.QPoint(_event.pos())


    # draw the whole scene
    def draw_scene(self):
        # self.test_draw_one_triangle()
        if self.gl_scenegraph != None:
            self.gl_scenegraph.draw(self.global_draw_mode)
        else:
            self.debug_out('No OpenGL scenegraph is set.')

    def normalizeAngle(self, angle):
        while angle < 0:
            angle += 360 * 16
        while angle > 360 * 16:
            angle -= 360 * 16
        return angle


    # draw a triangle for test
    def test_draw_triangle(self, p1, p2, p3):
        red = QtGui.QColor(255, 0, 0, 255)
        self.qglColor(red)
        GL.glVertex3d(p1[0], p1[1], p1[2])
        GL.glVertex3d(p2[0], p2[1], p2[2])
        GL.glVertex3d(p3[0], p3[1], p3[2])

    # draw a triangle in the whole scene for test
    def test_draw_one_triangle(self):
        p1 = numpy.array([-1, 0, 0])
        p2 = numpy.array([ 1, 0, 0])
        p3 = numpy.array([ 0, 2 * math.sqrt(3), 0])

        GL.glBegin(GL.GL_TRIANGLES)
        self.test_draw_triangle(p1, p2, p3)
        GL.glEnd()

    # set debug mode
    # \param[in] _is_debug when true some debug message will show up.
    def set_debug_mode(self, _is_debug):
        self.is_debug = _is_debug

    # is debug mode?
    # \return true when debug mode is on
    def is_debug_mode(self):
        return self.is_debug

    # debug output
    # \param[in] _dbgmes debug message. when debug mode is on, this is visible.
    def debug_out(self, _dbgmes):
        if self.is_debug == True:
            print _dbgmes

    # scenegraph operation
    def attach_gl_scenegraph(self, _gl_scenegraph):
        self.gl_scenegraph = _gl_scenegraph


#
# MainWindow for Test
#
class TestExaminerWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.examinerWidget = ExaminerWidget()

        mainLayout = QtGui.QHBoxLayout()
        mainLayout.addWidget(self.examinerWidget)
        self.setLayout(mainLayout)
        self.setWindowTitle(self.tr("TestExaminerWindow"))

#
# main test
#
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = TestExaminerWindow()
    window.show()
    sys.exit(app.exec_())
