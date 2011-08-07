#!/usr/bin/env python
#
# Copyright (C) 2010-2011 Yamauchi, Hitoshi
#

"""
QtExaminer widget version 0.0.0

\file
\brief QtExaminerWidget
"""

import sys
import math
import OpenGL
import numpy

from PyQt4  import QtCore, QtGui, QtOpenGL
from OpenGL import GL
from OpenGL import GLU

from ifgi.base  import enum, ifgimath
from ifgi.scene import Camera

import QtUtil


## QtExaminer's action mode
ActionMode = enum.Enum(['ExamineMode', 'PickingMode'])


# Scene examiner
class QtExaminerWidget(QtOpenGL.QGLWidget):
    """Scene examiner
    """

    def __init__(self, _parent):
        """constructor (public).
        \param[in] parent parent widget.
        """
        QtOpenGL.QGLWidget.__init__(self, _parent)

        # camera. This is the default camera, the scenegraph has
        # cameras.
        self.__gl_camera   = Camera.GLCamera()

        # OpenGL scene graph
        self.__gl_scenegraph = None

        # mouse points
        self.__lastpoint_2d = numpy.array([0, 0])
        # z == 0, not hit to the trackball sphere
        self.__lastpoint_3d = numpy.array([0, 0, 0])

        # popupmenu
        self.__popupmenu      = None
        self.__drawmode_group = None # for radio button
        self.__drawmode_bitmap2action = {} # drawmode bitmap to action dictionary

        # draw mode
        self.__global_drawmode = 0x0020 # 0x0020: Solid Flat as the default draw mode
        self.__drawmode_list   = None

        # action mode
        self.__action_mode = ActionMode.ExamineMode
        self.__is_rotating = False

        # SceneGraph coordinate
        self.__scene_cog    = numpy.array([0,0,0])
        self.__scene_radius = 1.0

        # window info
        self.__width  = 1
        self.__height = 1

        # some debug facility
        self.__is_debug = False


    def minimumSizeHint(self):
        """reimplemented: minimum size hint (public)."""
        return QtCore.QSize(50, 50)

    def sizeHint(self):
        """reimplemented: size hint (public)."""
        return QtCore.QSize(400, 400)

    # Window info: width
    def glWidth(self):
        """OpenGL Window info: width (public).
        \return gl window width
        """
        return self.__width

    # Window info: height
    def glHeight(self):
        """OpenGL Window info: height. (public).
        \return gl window width
        """
        return self.__height


    # initialize open GL
    def initializeGL(self):
        """initialize open GL. (public).
        """
        bgblack = QtGui.QColor(0, 0, 0, 255)
        self.qglClearColor(bgblack)
        GL.glShadeModel(GL.GL_FLAT)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_CULL_FACE)

    # paint
    def paintGL(self):
        """reimplemented: paint (public).
        """
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        self.__gl_frustum(Camera.EyePosition.EyeCenter)
        self.__glu_lookat(Camera.EyePosition.EyeCenter)

        # own computer gluLookAt matrix test
        # self.test_gluLookAt_matrix()
        self.draw_scene()

    # resize
    def resizeGL(self, _width, _height):
        """reimplemented: resize
        \param[in] _width  new width
        \param[in] _height new height
        """
        self.__width  = _width
        self.__height = _height

        side = min(_width, _height)

        GL.glViewport((_width - side) / 2, (_height - side) / 2, side, side)

        # perspective is for projection matrix
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()

        # DEBUG: self.__gl_camera.print_obj()
        GLU.gluPerspective(self.__gl_camera.get_fovy_rad() * 180 /math.pi,
                           self.__gl_camera.get_aspect_ratio(),
                           self.__gl_camera.get_z_near(),
                           self.__gl_camera.get_z_far())
        GL.glMatrixMode(GL.GL_MODELVIEW)


    #----------------------------------------------------------------------
    # View related methods
    #----------------------------------------------------------------------
    # view -- restoreHome
    def view_restorehome(self):
        print 'NIN: QtExaminerWidget viewRestoreHome()'

    # view -- setHome
    def view_sethome(self):
        print 'NIN: QtExaminerWidget viewSetHome()'

    # view -- all
    def view_all(self):
        """view all the scene."""
        cam_basis = self.__gl_camera.get_coordinate_system()
        eyepos = self.get_scene_cog()
        if (self.__gl_camera.get_projection() == Camera.ProjectionMode.Perspective):
            halfrad = 0.5 * self.__gl_camera.get_fovy_rad()
            dist    = self.get_scene_radius()/math.tan(halfrad)
            mag     = 1.2       # slack
            dist    = mag * max(dist, dist/self.__gl_camera.get_aspect_ratio())
            eyepos = eyepos - dist * cam_basis[2]
        else:
            eyepos = eyepos = (2.0 * self.get_scene_radius()) * cam_basis[2]

        self.__gl_camera.set_eye_pos(eyepos)
        self.__gl_camera.set_ortho_width(2.0 * self.get_scene_radius())

        self.updateGL()


    def set_scene_cog_radius(self, _cog_pos, _radius):
        """set scene (cog) position and radius.
        Affect to the z_near and z_far plane.
        \param[in] _cog_pos scene center of gravity position
        \param[in] _radius  scene radius.
        """
        self.__scene_cog    = _cog_pos
        self.__scene_radius = _radius
        self.__update_clipping_plane()
        self.updateGL()


    def set_radius(self, _radius):
        """set scene radius. (only set the radius change)
        Affect to the z_near and z_far plane.
        \param[in] _radius  scene radius.
        """
        self.__scene_radius = _radius
        self.__update_clipping_plane()
        self.updateGL()


    def __update_clipping_plane(self):
        """update the clipping plane according to the scene cog,
        radius, and camera eye position.
        """
        # This is huristic. e.g. slack_factor is a magic number.
        slack_factor = 10.0
        dist = numpy.linalg.norm(self.get_scene_cog() - self.__gl_camera.get_eye_pos())

        z_near = dist - (slack_factor * self.get_scene_radius())
        if(z_near < 0.01):
            z_near = 0.01

        z_far = dist + slack_factor * self.get_scene_radius()
        self.__gl_camera.set_z_near(z_near)
        self.__gl_camera.set_z_far(z_far)
        self.__gl_camera.set_focal_length(self.get_scene_radius())
        self.__gl_camera.set_ortho_width(2.0 * self.get_scene_radius())


    def get_scene_cog(self):
        """get scene center of gravity
        \return scene center opf gravity"""
        return self.__scene_cog


    def get_scene_radius(self):
        """get scene radius. The center is scene_cog.
        \return scene radius"""
        return self.__scene_radius


    # translate the camera
    def translate(self, _trans):
        """translate the camera. (public).
        \param[in] _trans translation
        """
        cam_basis = self.__gl_camera.get_coordinate_system()
        # Zdir '-' comes from the OpenGL coordinate system.
        cam_trans = (cam_basis[0] * _trans[0] +
                     cam_basis[1] * _trans[1] -
                     cam_basis[2] * _trans[2])
        eyepos = self.__gl_camera.get_eye_pos();
        eyepos = eyepos - cam_trans
        self.__gl_camera.set_eye_pos(eyepos);
        # print 'DEBUG: result: ' + str(self.__gl_camera.get_eye_pos())


    # rotate the camera with an axis
    def rotate_camera(self, _angle, _pn_axis):
        """rotate the camera with an axis.

        \param[in] _angle   degree
        \param[in] _pn_axis rotate axis
        """

        cam_basis = self.__gl_camera.get_coordinate_system()
        rotation = numpy.identity(4)

        eyepos = self.__gl_camera.get_eye_pos() - self.get_scene_cog()
        # Here z is '-', since OpenGL is left hand side coordinates.
        # print 'mat:'      + str(rotation)
        # print 'CamBasis:' + str(cam_basis)
        # print 'pn_axis:'  + str(_pn_axis)

        rmat = ifgimath.getRotationMat(-_angle,
                                        cam_basis[0] * _pn_axis[0] +
                                        cam_basis[1] * _pn_axis[1] -
                                        cam_basis[2] * _pn_axis[2]);

        # make 4d vector for homogeneous coordinate
        eyepos = ifgimath.transformPoint(rmat, eyepos) + self.get_scene_cog()


        # self.__gl_camera.lock();
        self.__gl_camera.set_eye_pos(eyepos)
        self.__gl_camera.set_view_dir(
            ifgimath.transformVector(rmat, self.__gl_camera.get_view_dir()))
        self.__gl_camera.set_up_dir(
            ifgimath.transformVector(rmat, self.__gl_camera.get_up_dir()))
        # self.__gl_camera.unlock();


    #----------------------------------------------------------------------
    # popup/context menu implementation
    #----------------------------------------------------------------------

    # popup -- function -- bgcolor implementation
    def popup_function_bgcolor(self):
        print 'NIN: bgcolor implementation'

    # popup -- function -- preference implementation
    def popup_function_preference(self):
        print 'NIN: preference implementation'

    #----------------------------------------------------------------------
    # popup/context menu GUI
    #----------------------------------------------------------------------

    # create popup menu: function submenu
    def create_popup_menu_function_menu(self):
        """create popup menu: function submenu.
        """
        assert(self.__popupmenu != None)
        self.popup_function_menu = self.__popupmenu.addMenu('Function')
        self.popup_function_bgcolor_act = \
            QtGui.QAction("Backgroundcolor", self,
                          statusTip="Set background color",
                          triggered=self.popup_function_bgcolor)
        self.popup_function_menu.addAction(self.popup_function_bgcolor_act)

    # create popup menu: draw mode
    def create_popup_menu_drawmode(self):
        """create popup menu: draw mode.
        """
        if self.__drawmode_list != None:
            # radio button group
            self.__drawmode_group = QtGui.QActionGroup(self)

            # self.__drawmode_list.print_obj()
            for dmi in self.__drawmode_list.get_mode_item_list():
                if (dmi.is_avairable() == True):
                    # Using a closure. mode_closure make a closure
                    # function that holds self (through this) and
                    # drawmode bitmap.
                    def mode_closure(this, drawmode_bitmap):
                        return (lambda: this.popupmenu_set_drawmode(drawmode_bitmap))

                    modclosure = mode_closure(self, dmi.get_bitmap())
                    drawmode_act = QtGui.QAction(dmi.get_name(), self,
                                                 statusTip="DrawMode: " +
                                                 dmi.get_name(),
                                                 triggered=modclosure,
                                                 checkable=True)
                    self.__drawmode_bitmap2action[dmi.get_bitmap()] = drawmode_act
                    self.__popupmenu.addAction(drawmode_act)
                    self.__drawmode_group.addAction(drawmode_act)

            if (self.__drawmode_list.find_drawmode_bitmap(self.__global_drawmode) == None):
                # no such draw mode in the list, turn off
                print 'no such draw mode in the list, turn off' +\
                      str(self.__global_drawmode)
                self.__global_drawmode = 0;
            self.popupmenu_set_drawmode(self.__global_drawmode)


    # create popup menu: main
    def create_popup_menu(self):
        """create popup menu: main.
        """
        if (self.__popupmenu == None):
            # print 'DEBUG: create_popup_menu'
            self.__popupmenu = QtGui.QMenu(self)
            self.create_popup_menu_function_menu()
            popup_preference_act = \
                QtGui.QAction("Preference", self,
                              statusTip="Popup preference dialog",
                              triggered=self.popup_function_preference)
            self.__popupmenu.addAction(popup_preference_act)
            self.__popupmenu.addSeparator()

            # add drawmode if exists
            self.create_popup_menu_drawmode()

        else:
            # print 'DEBUG: reuse popup menu'
            pass

        return self.__popupmenu


    # popup context menu
    def popup_context_menu(self, _global_mouse_pos):
        """popup context menu.
        """
        self.create_popup_menu()
        self.__popupmenu.exec_(_global_mouse_pos)

    # popupmenu implementation
    def popupmenu_function(self):
        """popupmenu implementation.
        """
        print 'NIN: popupmenu_function is called.'

    # popupmenu implementation: set drawmode and change the global drawmode
    def popupmenu_set_drawmode(self, _drawmode_bitmap):
        """popupmenu implementation: set drawmode and change the
        global drawmode.

        \param[in] _drawmode_bitmap global drawmode bitmap to set if
        exists in the menu actions
        """
        # print 'DEBUG: popupmenu_set_drawmode: ' + str(_drawmode_bitmap)
        assert(_drawmode_bitmap in self.__drawmode_bitmap2action)

        mitem = self.__drawmode_bitmap2action[_drawmode_bitmap]
        assert(mitem != None)

        mitem.setChecked(True)
        self.__global_drawmode = _drawmode_bitmap

        self.updateGL()


    # mouse press event
    #   - right: popup menu
    #   - left:  camera move
    def mousePressEvent(self, _event):
        """mouse press event.

          - right: popup menu
          - left:  camera move
          """

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
            self.popup_context_menu(_event.globalPos())

        else:
            # left button & CTRL pressed and lasso interactive
            if ((QtUtil.in_key_modifier(_event.modifiers(),
                                        QtCore.Qt.ControlModifier)) and
                (_event.button() == QtCore.Qt.LeftButton)           and
                (self.__action_mode == Actionmode.ExamineMode)):
                # avoid control key being useless for other modes
                # self.startDrag()
                pass

            elif (self.__action_mode == ActionMode.ExamineMode):
                # remember this point
                self.__lastpoint_2d = QtUtil.QPoint2numpy(_event.pos())
                self.__lastpoint_3d = ifgimath.mapToSphere(self.__lastpoint_2d,
                                                           self.glWidth(),
                                                           self.glHeight())

                self.__is_rotating = True
                # DELETEME
                # print 'DEBUG: mouse press at ' + str(self.__lastpoint_2d) +\
                # ', on spehere: ' + str(self.__lastpoint_3d)


            # elif (self.__action_mode == Actionmode.FlyToMode):
            #       flyTo(_event->pos(), _event->button()==QtCore.Qt.MidButton);
            #   elif (self.__action_mode == Actionmode.PickingMode):
            #       emit signalMouseEvent(_event);
            #       # same for SceneGraph
            #       SceneGraph::ObservableActor_Event arg(ArgumentType::MousePressed);
            #       arg.x=_event->x();
            #       arg.y=_event->y();
            #       buttonState(_event,arg.button,arg.stateBefore,arg.stateAfter);

            #       notify(arg)
            #       ioProcessDetachRequests();

            #   elif (self.__action_mode == Actionmode.LassoMode):
            #       #  give event to built-in lasso
            #       d_lasso->slotDrawLasso(_event);

            #   elif (self.__action_mode == Actionmode.QuestionMode):
            #       # give event to application
            #       emit signalMouseEventIdentify(_event);
            #       # // same for SceneGraph
            #       SceneGraph::ObservableActor_Event arg(ArgumentType::MousePressed);
            #       arg.x=_event->x();
            #       arg.y=_event->y();
            #       buttonState(_event,arg.button,arg.stateBefore,arg.stateAfter);

            #       notify(arg)
            #       ioProcessDetachRequests()


    # mouse wheel event
    def wheelEvent(self, _event):
        """mouse wheel event.
        \param[in] _event mouse event.
        """
        # print 'Mouse wheel event: ' +  str(_event)
        if (self.__action_mode == ActionMode.PickingMode):
            print 'NIN: wheel event: no PickingMode'
            # QPoint newPoint2D = _event->pos();
            # bool inside=((newPoint2D.x()>=0) && (newPoint2D.x()<=glWidth()) &&
            #              (newPoint2D.y()>=0) && (newPoint2D.y()<=glHeight()));
            # if (inside) {
            #     # give event to the application. Notice wheel event is not a MouseEvent.
            #     emit signalMouseWheelEvent(_event);

            #     # for SceneGraph
            #     SceneGraph::ObservableActor_Event arg(ArgumentType::MouseWheelMoved);
            #     arg.x=_event->x();
            #     arg.y=_event->y();
            #     arg.button=0;
            #     arg.stateAfter=arg.stateBefore=buttonState(_event);
            #     # _event->orientation() may be not necessary, but in the future?
            #     arg.wheelDelta=_event->delta();
            #     notify(arg); ioProcessDetachRequests();
        # elif (self.__action_mode == ActionMode.LassoMode):
        elif (self.__action_mode == ActionMode.ExamineMode):
            if (self.__gl_camera.get_projection() == Camera.ProjectionMode.Perspective):
                # wheel only return +-120
                zmove = - (float(_event.delta()) / 120.0) * 0.2 * self.get_scene_radius()
                self.translate([0.0, 0.0, zmove])
            else:
                print 'NIN: wheel movement with Orthographic projectionmode'
                assert(self.__gl_camera.get_projection() ==
                       Camera.ProjectionMode.Orthographic)
                # ow = self.__gl_camera.get_ortho_width()
                # zmove = (float)_event->delta() / 120.0 * 0.2 * ow;
                # self.__gl_camera.set_ortho_width(ow + zmove)
        else:
            raise StandardError, ('No such examiner mode')

        # emit signalSetView(&d_camera);
        # SceneGraph::ObservableActor_Event arg(ArgumentType::ViewChanged);
        # notify(arg); ioProcessDetachRequests();
        self.updateGL()
        _event.accept()         # no more wheel event action



    # ExamineMode: move in z direction
    #
    # \param[in] _newPoint2D mouse position on screen
    def examineModeMoveZdir(self, _newPoint2D):
        """ExamineMode: move in z direction.

        \param[in] _newPoint2D mouse position on screen
        """
        # move in z direction
        if (self.__gl_camera.get_projection() == Camera.ProjectionMode.Perspective):
            zmove = self.get_scene_radius() * ((_newPoint2D[1] - self.__lastpoint_2d[1])
                                               * 3.0 / float(self.glHeight()))
            self.translate(numpy.array([0, 0, zmove]))
        elif (self.__gl_camera.get_projection() == Camera.ProjectionMode.Orthographic):
            print 'NIN: examineModeMoveZdir: in Orthographic projection'
            # ow    = self.__gl_camera.get_ortho_width()
            # zmove = ((_newPoint2D[1] - self.__lastpoint_2d[1]) * ow / float(self.glHeight()))
            # self.__gl_camera.set_orthowidth(ow - zmove)
        else:
            raise StandardError, ('no such projection mode')


    # ExamineMode: move in x,y direction
    # \param[in] _newPoint2D mouse position on screen
    def examineModeMoveXYdir(self, _newPoint2D):
        """ExamineMode: move in x,y direction.

        \param[in] _newPoint2D mouse position on screen
        """
        value_x = (self.get_scene_radius() * (_newPoint2D[0] - self.__lastpoint_2d[0]) *
                   2.0 / float(self.glWidth()))
        value_y = (self.get_scene_radius() * (_newPoint2D[1] - self.__lastpoint_2d[1]) *
                   2.0 / float(self.glHeight()))
        self.translate(numpy.array([value_x, -value_y, 0.0]));


    # ExamineMode: Pick
    def examineModePick(self):
        """ExamineMode: Pick.
        """
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
        """ExamineMode: Question.
        """
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
    # \param[in] _numpoint2D current mouse 2D point
    def examineModeRotateTrackball(self, _numpoint2D):
        """ExamineMode: Rotate Trackball.

        \param[in] _numpoint2D current mouse 2D point
        """

        if (self.__lastpoint_3d[2] != 0): # z == 0 ... not hit on sphere
            newPoint3D = ifgimath.mapToSphere(_numpoint2D,
                                              self.glWidth(), self.glHeight())
            if (newPoint3D[2] != 0): # point hits the sphere
                angle = 0
                rot_axis  = numpy.cross(self.__lastpoint_3d, newPoint3D)
                cos_angle = numpy.inner(self.__lastpoint_3d, newPoint3D)
                if (math.fabs(cos_angle) < 1.0):
                    angle = math.acos(cos_angle); # radian
                    angle *= 2.0; # inventor rotation

                self.rotate_camera(angle, rot_axis)


    # mouse move event
    #  - Right drag: context menu
    #  - Left  drag: context menu
    def mouseMoveEvent(self, _event):
        """mouse move event.

        - Right drag: context menu
        - Left  drag: context menu
        """
        if ((_event.button() != QtCore.Qt.RightButton) or
            ((self.__action_mode == PickingMode))): # && !d_popupEnabled) ) {

            newPoint2D = QtUtil.QPoint2numpy(_event.pos())
            isInside = ((newPoint2D[0] >=0 ) and (newPoint2D[0] <= self.glWidth()) and
                        (newPoint2D[1] >=0 ) and (newPoint2D[1] <= self.glHeight()))

            if  (self.__action_mode == ActionMode.PickingMode):
                self.examineModePick()
            # elif (self.__action_mode == ActionMode.LassoMode):
            #     pass
            # elif (self.__action_mode == ActionMode.QuestionMode):
            #     pass
            elif (self.__action_mode == ActionMode.ExamineMode):
                if (not isInside):
                    return      # do nothing if mouse is outside of the window

                newPoint3D = ifgimath.mapToSphere(newPoint2D,
                                                  self.glWidth(), self.glHeight());
                # makeCurrent()?

                if ((_event.buttons() & QtCore.Qt.LeftButton) and
                    (_event.buttons() & QtCore.Qt.MidButton)):
                    self.examineModeMoveZdir(newPoint2D)
                elif (_event.buttons() & QtCore.Qt.MidButton):
                    self.examineModeMoveXYdir(newPoint2D)
                elif (_event.buttons() & QtCore.Qt.LeftButton):
                    self.examineModeRotateTrackball(newPoint2D)

                self.__lastpoint_2d = newPoint2D;
                self.__lastpoint_3d = newPoint3D;

            self.updateGL();
            # d_lastMoveTime.restart();

            # DELETEME
            # print 'DEBUG: mouse press at ' + str(self.__lastpoint_2d) +\
            #     ', on spehere: ' + str(self.__lastpoint_3d)


    # draw the whole scene
    def draw_scene(self):
        """draw the whole scene.
        """
        # self.test_draw_one_triangle()
        if self.__gl_scenegraph != None:
            self.__gl_scenegraph.draw(self.__global_drawmode)
        else:
            self.debug_out('No OpenGL scenegraph is set.')

    # draw a triangle for test
    def test_draw_triangle(self, p1, p2, p3):
        """draw a triangle for test."""
        red = QtGui.QColor(255, 0, 0, 255)
        self.qglColor(red)
        GL.glVertex3d(p1[0], p1[1], p1[2])
        GL.glVertex3d(p2[0], p2[1], p2[2])
        GL.glVertex3d(p3[0], p3[1], p3[2])

    # draw a triangle in the whole scene for test
    def test_draw_one_triangle(self):
        """draw a triangle in the whole scene for test.
        """
        p1 = numpy.array([-1, 0, 0])
        p2 = numpy.array([ 1, 0, 0])
        p3 = numpy.array([ 0, 2 * math.sqrt(3), 0])

        GL.glBegin(GL.GL_TRIANGLES)
        self.test_draw_triangle(p1, p2, p3)
        GL.glEnd()

    # set debug mode
    def set_debug_mode(self, _is_debug):
        """set debug mode.
        \param[in] _is_debug when true some debug message will show up.
        """
        self.__is_debug = _is_debug

    # is debug mode?
    # \return true when debug mode is on
    def is_debug_mode(self):
        """is debug mode?
        \return true when debug mode is on
        """
        return self.__is_debug

    # debug output
    def debug_out(self, _dbgmes):
        """debug output.
        \param[in] _dbgmes debug message. when debug mode is on, this
        is visible.
        """
        if self.__is_debug == True:
            print _dbgmes


    # set current gl camera
    def set_current_gl_camera(self, _cur_gl_camera):
        """set current gl camera.
        \param[in] _cur_gl_camera current gl camera"""

        assert(_cur_gl_camera != None)
        assert(_cur_gl_camera.get_classname() == 'GLCamera')
        self.__gl_camera = _cur_gl_camera



    # scenegraph operation
    def attach_gl_scenegraph(self, _gl_scenegraph):
        """scenegraph operation.
        """
        self.__gl_scenegraph = _gl_scenegraph

        # get GLCamera from the gl scenegraph
        self.set_current_gl_camera(self.__gl_scenegraph.get_current_gl_camera())

        # get draw mode information
        self.__drawmode_list = self.__gl_scenegraph.collect_drawmode_list()
        # if self.__drawmode_list != None:
            # print 'DEBUG: found draw mode in the scene'
            # self.__drawmode_list.print_obj()
            # popup menu will refer this drawmode_list

        # set scene size information
        bb = self.__gl_scenegraph.get_scenegraph().get_root_node().get_bbox()
        cog    = 0.5 * (bb.get_min() + bb.get_max())

        # bb.get_max() - bb.get_min() overflows when no objects.
        # Warning: overflow encountered in subtract
        radius = 0.5 * numpy.linalg.norm(bb.get_max() - bb.get_min())
        self.set_scene_cog_radius(cog, radius)

        # print 'DEBUG:scene_cog: ' + str(self.get_scene_cog()) + ', scene_radius: '\
        #     + str(self.get_scene_radius())
        if self.get_scene_radius() < 1e-6:
            # nothing seems in there
            self.set_scene_radius(1.0)
            print 'DEBUG:empty scene: adjust radius = 1.0'

    # peek gl scenegraph
    def peek_gl_scenegraph(self):
        """peek the gl scenegraph reference.
        \return attached gl scenegraph, may None."""
        return self.__gl_scenegraph


    #----------------------------------------------------------------------
    # camera related OpenGL utility functions
    #----------------------------------------------------------------------

    def __glu_lookat(self, _eyeposition):
        """gluLookat call with setup.
        \param[in] _eyeposition stereo eye position
        """
        [ep, at, up] = self.__gl_camera.get_lookat(_eyeposition)

        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()

        # print 'DEBUG: ep = ' + str(ep)
        # print 'DEBUG: at = ' + str(at)
        # print 'DEBUG: up = ' + str(up)
        GLU.gluLookAt(ep[0], ep[1], ep[2],
                      at[0], at[1], at[2],
                      up[0], up[1], up[2])

        # opengl matrix access
        # glmat = GL.glGetDoublev(GL.GL_MODELVIEW_MATRIX)


    def __gl_frustum(self, _eyeposition):
        """call glFrustum to setup the projection matrix.
        \param[in] _eyeposition stereo eye position
        """
        [left, right, top, bottom] = self.__gl_camera.query_frustum(_eyeposition)
        z_near = self.__gl_camera.get_z_near()
        z_far  = self.__gl_camera.get_z_far()

        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()

        if (self.__gl_camera.get_projection() == Camera.ProjectionMode.Perspective):
            # print 'Projection: z_far = ',  z_far
            GL.glFrustum(left, right, bottom, top, z_near, z_far)
        else:
            GL.glOrtho(left, right, bottom, top, z_near, z_far)

        # glmat[_position][Projection] = GL.glGetDoublev(GL.GL_PROJECTION_MATRIX)

        GL.glMatrixMode(GL.GL_MODELVIEW);


    #----------------------------------------------------------------------
    # test
    #----------------------------------------------------------------------

    def test_gluLookAt_matrix(self):
        """test getLookAtMatrix routine.

        generate two matrices, glmat by gluLookAt, mat by
        getLookAtMatrix.  Then compare them. (To run this test, You
        need OpenGL bindings and also your Camera implementation that
        provides eye, lookat, up.)
        """
        GL.glLoadIdentity()

        # This is your camera. It tells eye, lookat, up.
        [ep, at, up] = self.__gl_camera.get_lookat(Camera.EyePosition.EyeCenter)
        GLU.gluLookAt(ep[0], ep[1], ep[2],
                      at[0], at[1], at[2],
                      up[0], up[1], up[2])

        # OpenGL gluLookAt matrix
        glmat = None
        glmat = GL.glGetDoublev(GL.GL_MODELVIEW_MATRIX)

        # my matrix
        mat   = ifgimath.getLookAtMatrix(ep, at, up)

        # debug output
        print 'glmat'
        print glmat
        print 'mat'
        print mat

        # compare glmat and mat
        for i in range(4):
            for j in range(4):
                if(math.fabs(glmat[i][j] - mat[i][j]) > 1.0e-5):
                    raise StandardError ('matrix does not match.')


# MainWindow for Test
class TestQtExaminerWindow(QtGui.QWidget):
    """MainWindow for Test"""

    def __init__(self, _parent=None):
        """constructor"""
        QtGui.QWidget.__init__(self, _parent)

        self.examinerWidget = QtExaminerWidget()

        mainLayout = QtGui.QHBoxLayout()
        mainLayout.addWidget(self.examinerWidget)
        self.setLayout(mainLayout)
        self.setWindowTitle(self.tr("TestQtExaminerWindow"))


# main test
if __name__ == '__main__':
    """main test.
    """
    app = QtGui.QApplication(sys.argv)
    window = TestQtExaminerWindow()
    window.show()
    sys.exit(app.exec_())
