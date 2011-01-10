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
# Eye Position
#
EyePosition = enum.Enum(['EyeCenter', 'EyeLeft', 'EyeRight'])


#
# camera base class
#
class Camera(object):
    # default constructor
    def __init__(self):
        self.eye_pos      = numpy.array([0, 0,  5])
        self.view_dir     = numpy.array([0, 0, -1])
        self.up_dir       = numpy.array([0, 1,  0])
        self.fovy_rad     = 45.0 * math.pi / 180.0
        self.aspect_ratio = 1.0
        self.z_near       = 0.1
        self.z_far        = 1000
        self.projection   = ProjectionMode.Perspective
        self.focal_length = 1.0
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

    # get fovy as radian
    def get_fovy_rad(self):
        return self.fovy_rad

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
    def get_projection(self):
        return self.projection

    # get gluLookAt() parameters
    #
    # \param[in] _eye_position eye position for stereo {EyeCenter,
    # EyeLeft, EyeRight}, NIN Not implemented now.
    def get_lookat(self, _eye_position):
        assert(_eye_position == EyePosition.EyeCenter)
        assert(self.focal_length != 0)
        return [self.eye_pos,
                self.eye_pos + self.focal_length * self.view_dir,
                self.up_dir]

    # Get the camera coordinate system as OpenGL (left hand)
    #
    # Get orthonrmal basis for camera coordinate system {_ex,_ey,_ez}.
    # \return [ex, ey, ez]  ["right", "up", viewingDriection()] system
    def get_coordinate_system(self):
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
        print '#' + cname + '::fovy_rad = ' + str(self.fovy_rad)
        print '#' + cname + '::aspect_ratio = ' + str(self.aspect_ratio)
        print '#' + cname + '::z_near = '   + str(self.z_near)
        print '#' + cname + '::z_far = '    + str(self.z_far)
        print '#' + cname + '::projection = ' + str(self.projection)
        print '#' + cname + '::focal_length = ' + str(self.focal_length)


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
