#!/usr/bin/env python
#
# camera
#

"""IFGI Camera"""

import math
import numpy
import enum

#
# Projection Mode
#
ProjectionMode = enum.Enum(['Perspective', 'Orthographic'])


#
# camera base class
#
class Camera(object):
    # default constructor
    def __init__(self):
        self.eye_pos      = numpy.array([0, 0,  5])
        self.view_dir     = numpy.array([0, 0, -1])
        self.up_dir       = numpy.array([0, 1,  0])
        self.fov          = 45.0 * math.pi / 180.0
        self.aspect_ratio = 1.0
        self.z_near       = 0.1
        self.z_far        = 1000
        self.projection   = ProjectionMode.Perspective
        # print 'called Camara.__init__()'

    # get eye position
    def get_eye_pos(self):
        return self.eye_pos
    # set eye position
    def set_eye_pos(self, _eye_pos):
        self.eye_pos = _eye_pos

    # get view direction
    def get_view_dir(self):
        return self.view_dir
    # set view direction
    def set_view_dir(self, _view_dir):
        self.view_dir = _view_dir

    # get up direction
    def get_up_dir(self):
        return self.up_dir
    # set up direction
    def set_up_dir(self, _up_dir):
        self.up_dir = _up_dir

    # get fov as radian
    def get_fov(self):
        return self.fov

    # get aspect ratio
    def get_aspect_ratio(self):
        return self.aspect_ratio

    # get z near plane distance
    def get_z_near(self):
        return self.z_near

    # get z far plane distance
    def get_z_far(self):
        return self.z_far

    # class name
    def get_classname(self):
        assert 0, "get_classname must be implemented in a derived class."
        return None

    # get projection mode
    def getProjection(self):
        return self.projection

    # Get the camera coordinate system
    #
    # Get orthonrmal basis for camera coordinate system {_ex,_ey,_ez}.
    # \return [ex, ey, ez]  ["right", "up", viewingDriection()] system
    def getCoordinateSystem(self):
        ex  = numpy.cross(self.view_dir, self.up_dir)
        ex /= numpy.linalg.norm(ex)
        ey  = numpy.cross(ex, self.view_dir)
        ey /= numpy.linalg.norm(ey)
        assert(abs(numpy.linalg.norm(self.view_dir) - 1) < 0.000001)

        # print 'ex = ' + str(ex)
        # print 'ey = ' + str(ey)
        # print 'ez = ' + str(self.view_dir)

        return [ex, ey, self.view_dir]

    # for debug
    def print_obj(self):
        cname = self.get_classname()
        print '#' + cname + '::eye_pos = '  + str(self.eye_pos)
        print '#' + cname + '::view_dir = ' + str(self.view_dir)
        print '#' + cname + '::up_dir = '   + str(self.up_dir)
        print '#' + cname + '::fov = '      + str(self.fov)
        print '#' + cname + '::aspect_ratio = ' + str(self.aspect_ratio)
        print '#' + cname + '::z_near = '   + str(self.z_near)
        print '#' + cname + '::z_far = '    + str(self.z_far)
        print '#' + cname + '::projection = ' + str(self.projection)


#
# OpenGL camera
#
class GLCamera(Camera):
    # default constructor
    def __init__(self):
        super(GLCamera, self).__init__()

    # class name
    def get_classname(self):
        return 'GLCamera'



#
# IFGI camera
#
class IFGICamera(Camera):
    # default constructor
    def __init__(self):
        super(IFGICamera, self).__init__()

    # class name
    def get_classname(self):
        return 'IFGICamera'




#
# main test
#
if __name__ == '__main__':
    gl_cam   = GLCamera()
    gl_cam.print_obj()

    ifgi_cam = IFGICamera()
    ifgi_cam.print_obj()
