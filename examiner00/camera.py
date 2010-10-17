#!/usr/bin/env python
#
# camera
#

"""IFGI Camera"""

import math
import numpy

#
# camera base class
#
class Camera(object):
    # default constructor
    def __init__(self):
        self.eye_pos      = numpy.array([0, 0,    5])
        self.view_dir     = numpy.array([0, 1.7,  0])
        self.up_dir       = numpy.array([0, 1,  0])
        self.fov          = 45.0 * math.pi / 180.0
        self.aspect_ratio = 1.0
        self.z_near       = 0.1
        self.z_far        = 1000
        # print 'called Camara.__init__()'

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
