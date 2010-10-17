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

import camera

#
# Scene examiner
#
class ExaminerWidget(QtOpenGL.QGLWidget):
    def __init__(self, parent=None):
        QtOpenGL.QGLWidget.__init__(self, parent)

        # cameras
        self.gl_camera   = camera.GLCamera()
        # self.ifgi_camera = camera.IFGICamera()

        # FIXME remove below...
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0
        self.lastPos = QtCore.QPoint()


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

    def mousePressEvent(self, event):
        self.lastPos = QtCore.QPoint(event.pos())

    def mouseMoveEvent(self, event):
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()

        if event.buttons() & QtCore.Qt.LeftButton:
            self.setXRotation(self.xRot + 8 * dy)
            self.setYRotation(self.yRot + 8 * dx)
        elif event.buttons() & QtCore.Qt.RightButton:
            self.setXRotation(self.xRot + 8 * dy)
            self.setZRotation(self.zRot + 8 * dx)

        self.lastPos = QtCore.QPoint(event.pos())


    # draw a triangle
    def draw_triangle(self, p1, p2, p3):
        red = QtGui.QColor(255, 0, 0, 255)
        self.qglColor(red)
        GL.glVertex3d(p1[0], p1[1], p1[2])
        GL.glVertex3d(p2[0], p2[1], p2[2])
        GL.glVertex3d(p3[0], p3[1], p3[2])


    # draw the whole scene
    def draw_scene(self):
        p1 = numpy.array([-1, 0, 0])
        p2 = numpy.array([ 1, 0, 0])
        p3 = numpy.array([ 0, 2 * math.sqrt(3), 0])

        GL.glBegin(GL.GL_TRIANGLES)
        self.draw_triangle(p1, p2, p3)
        GL.glEnd()


    def normalizeAngle(self, angle):
        while angle < 0:
            angle += 360 * 16
        while angle > 360 * 16:
            angle -= 360 * 16
        return angle

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
