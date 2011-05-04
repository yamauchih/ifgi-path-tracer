#!/usr/bin/env python
#
# Copyright (C) 2010-2011 Yamauchi, Hitoshi
#

"""Camera module
\file
\brief camera"""

import math
import numpy
from ifgi.base import enum

## Projection Mode
ProjectionMode = enum.Enum(['Perspective', 'Orthographic'])

## Eye Position
EyePosition = enum.Enum(['EyeCenter', 'EyeLeft', 'EyeRight'])


# camera base class
class Camera(object):
    """camera base class"""

    # default constructor
    def __init__(self):
        """default constructor"""
        self.__eye_pos      = numpy.array([0, 0,  5])
        self.__view_dir     = numpy.array([0, 0, -1])
        self.__up_dir       = numpy.array([0, 1,  0])
        self.__fovy_rad     = 45.0 * math.pi / 180.0
        self.__aspect_ratio = 1.0
        self.__z_near       = 0.1
        self.__z_far        = 1000
        self.__projection   = ProjectionMode.Perspective
        self.__target_dist  = 1.0
        self.__focal_length = 1.0
        self.__lens_screen_dist = 1.0
        self.__lens_film_dist = 1.0
        # lower bottom corner
        self.__LB_corner    = numpy.array([-1, -1,  0])
        # x direction base vector
        self.__ex    = numpy.array([1, 0,  0])
        # y direction base vector
        self.__ey    = numpy.array([0, 1,  0])

        self.__compute_screen_parameter()

        # print 'called Camara.__init__()'

    # compute screen parameters
    def __compute_screen_parameter(self):
        """compute screen parameters.
        __LB_corner, __ex, __ey  are computed.

          +-----------+--
          |           | ^
          |           | |
          |           | __ey
          |           | |
        LB+-----------+--
          |-- __ex -->|
          """

        # get center
        center = self.__eye_pos + self.__lens_screen_dist * self.__view_dir

        # get left bottom corner
        halffovy   = 0.5 * self.__fovy_rad
        halfwidth  = self.__lens_screen_dist * math.tan(halffovy)
        halfheight = self.__lens_screen_dist * math.tan(halffovy * self.__aspect_ratio)

        # get basis
        [self.__ex, self.__ey, self.__view_dir] = self.get_coordinate_system()

        self.__LB_corner = (
            center - (halfwidth * self.__ex + halfheight * self.__ey))

        # print 'DEBUG: halfwidth  = ' + str(halfwidth)
        # print 'DEBUG: halfheight = ' + str(halfheight)

        self.__ex = 2.0 * halfwidth  * self.__ex
        self.__ey = 2.0 * halfheight * self.__ey


    # get eye position
    def get_eye_pos(self):
        """get eye position. (public)
        \return eye position vector3"""
        return self.__eye_pos

    # set eye position
    def set_eye_pos(self, _eye_pos):
        """set eye position. (public)
        \param[in] _eye_pos eye position"""
        self.__eye_pos = _eye_pos
        self.__compute_screen_parameter()

    # get view direction
    def get_view_dir(self):
        """get view direction. (public)
        \return view direction"""
        return self.__view_dir

    # set view direction
    def set_view_dir(self, _view_dir):
        """set view direction. (public)
        \return view direction (normalized)."""
        self.__view_dir = _view_dir
        self.__compute_screen_parameter()

    # get up direction
    def get_up_dir(self):
        """get up direction. (public)
        \return up direction"""
        return self.__up_dir

    # set up direction
    def set_up_dir(self, _up_dir):
        """set up direction. (public)
        \return up direction vector."""
        self.__up_dir = _up_dir
        self.__compute_screen_parameter()

    # get fovy as radian
    def get_fovy_rad(self):
        """get fovy as radian. (public)
        \return field of view Y. (radian)"""
        return self.__fovy_rad

    # get aspect ratio
    def get_aspect_ratio(self):
        """get aspect ratio. (public)
        \return aspect ratio."""
        return self.__aspect_ratio

    # get z near plane distance
    def get_z_near(self):
        """get z near plane distance. (public)
        \return z near plane distance."""
        return self.__z_near

    # get z far plane distance
    def get_z_far(self):
        """get z far plane distance. (public)
        \return z far plane distance."""
        return self.__z_far

    # get class name
    def get_classname(self):
        """get class name. (public)
        This must be reimplemented in the inherited class.
        \return None"""
        assert 0, "get_classname must be implemented in a derived class."
        return None

    # get projection mode
    def get_projection(self):
        """get projection mode. (public)
        \return projection mode ('Perspective', 'Orthographic')"""
        return self.__projection

    # get gluLookAt() parameters
    def get_lookat(self, _eye_type):
        """get gluLookAt() parameters. (public)
        \param[in] _eye_type eye position for stereo {EyeCenter,
        EyeLeft, EyeRight}, NIN Not implemented now."""
        assert(_eye_type == EyePosition.EyeCenter)
        assert(self.__target_dist  != 0)
        assert(self.__focal_length != 0)
        return [self.__eye_pos,
                self.__eye_pos + self.__target_dist * self.__view_dir,
                self.__up_dir]

    # Get the camera coordinate system as OpenGL (left hand)
    def get_coordinate_system(self):
        """Get the camera coordinate system as OpenGL (public)

        Get orthonrmal basis for camera coordinate system {_ex,_ey,_ez}.
        \return [ex, ey, ez]  [right, up, viewingDriection()] system.
        Left hand system.
        """

        ex  = numpy.cross(self.__view_dir, self.__up_dir)
        ex /= numpy.linalg.norm(ex)
        ey  = numpy.cross(ex, self.__view_dir)
        ey /= numpy.linalg.norm(ey)
        assert(abs(numpy.linalg.norm(self.__view_dir) - 1) < 0.000001)

        # print 'ex = ' + str(ex)
        # print 'ey = ' + str(ey)
        # print 'ez = ' + str(self.__view_dir)

        return [ex, ey, self.__view_dir]

    # get target (lookat point) distance
    def get_target_distance(self):
        """get target (lookat point) distance.
        \return eye to lookat point (target) distance."""

        return self.__target_dist

    # get lens to screen distance
    def get_lens_to_screen_distance(self):
        """get lens to screen distance.
        \return lens to screen distance."""

        return self.__lens_screen_dist

    # get focal length
    def get_focal_length(self):
        """get focal length.
        \return focal length."""

        return self.__focal_length

    # get lens to screen distance
    def get_lens_to_screen_distance(self):
        """get get lens to screen distance.
        \return lens to screen distance."""

        return self.__lens_screen_dist

    # get lens to film distance
    def get_lens_to_film_distance(self):
        """get get lens to fim distance.
        \return lens to screen distance."""

        # NIN
        return self.__lens_film_dist

    # get ray
    def get_ray(self, _dx, _dy):
        """get ray.
        \param[in] _dx delta x normalized screen coordinate [0,1]
        \param[in] _dy delta y normalized screen coordinate [0,1]
        \return a ray
        """
        target =  self.__LB_corner + _dx * self.__ex + _dy * self.__ey
        vdir   =  target - self.__eye_pos
        vdir   /= numpy.linalg.norm(vdir)

        r = Ray.Ray(self.__eye_pos, vdir, self.__z_near, self.__z_far)
        return r

    # set camera parameters
    def set_camera_param(self, _othercam):
        """set camera parameters.
        deep copy the camera parameters.
        \param[in] _othercam other camera."""

        # deep copy
        self.__eye_pos      = _othercam.get_eye_pos(). copy()
        self.__view_dir     = _othercam.get_view_dir().copy()
        self.__up_dir       = _othercam.get_up_dir().  copy()
        self.__fovy_rad     = _othercam.get_fovy_rad()
        self.__aspect_ratio = _othercam.get_aspect_ratio()
        self.__z_near       = _othercam.get_z_near()
        self.__z_far        = _othercam.get_z_far()
        self.__projection   = _othercam.get_projection()
        self.__target_dist  = _othercam.get_target_distance()
        self.__focal_length = _othercam.get_focal_length()
        self.__lens_screen_dist = _othercam.get_lens_to_screen_distance()
        self.__lens_film_dist = _othercam.get_lens_to_film_distance()
        self.__LB_corner    = _othercam.__LB_corner
        self.__ex           = _othercam.__ex
        self.__ey           = _othercam.__ey


    # for debug
    def print_obj(self):
        """print this object for debug."""
        cname = self.get_classname()
        print '#' + cname + '::eye_pos = '  + str(self.__eye_pos)
        print '#' + cname + '::view_dir = ' + str(self.__view_dir)
        print '#' + cname + '::up_dir = '   + str(self.__up_dir)
        print '#' + cname + '::fovy_rad = ' + str(self.__fovy_rad)
        print '#' + cname + '::aspect_ratio = ' + str(self.__aspect_ratio)
        print '#' + cname + '::z_near = '   + str(self.__z_near)
        print '#' + cname + '::z_far = '    + str(self.__z_far)
        print '#' + cname + '::projection = ' + str(self.__projection)
        print '#' + cname + '::target_dist = ' + str(self.__target_dist)
        print '#' + cname + '::focal_length = ' + str(self.__focal_length)

        print '#' + cname + '::lens_screen_dist = ' +\
            str(self.__lens_screen_dist)
        print '#' + cname + '::lens_film_dist = ' + str(self.__lens_film_dist)
        print '#' + cname + '::LB_corner = ' + str(self.__LB_corner)
        print '#' + cname + '::ex = '      + str(self.__ex)
        print '#' + cname + '::ey = '      + str(self.__ey)


    # get html info
    def get_html_info(self):
        """get camera information as html format.
        \return camera information in html string."""

        ret_s = '<h2>Camera information</h2>\n'                       +\
            '<ul>\n'                                                  +\
            '  <li><b>Class name:</b> ' + self.get_classname() + '\n' +\
            '  <li>eye_pos: '      + str(self.__eye_pos)       + '\n' +\
            '  <li>view_dir: '     + str(self.__view_dir)      + '\n' +\
            '  <li>up_dir: '       + str(self.__up_dir)        + '\n' +\
            '  <li>fovy_rad: '     + str(self.__fovy_rad)      + '\n' +\
            '  <li>aspect_ratio: ' + str(self.__aspect_ratio)  + '\n' +\
            '  <li>z_near: '       + str(self.__z_near)        + '\n' +\
            '  <li>z_far: '        + str(self.__z_far)         + '\n' +\
            '  <li>projection: '   + str(self.__projection)    + '\n' +\
            '  <li>target_dist: '  + str(self.__target_dist)   + '\n' +\
            '  <li>focal_length: ' + str(self.__focal_length)  + '\n' +\
            '  <li>lens to screen distance: ' +\
            str(self.__lens_screen_dist)  + '\n' +\
            '  <li>lens to film distance: ' +\
            str(self.__lens_film_dist)  + '\n' +\
            '  <li>Left bottom corner: ' + str(self.__LB_corner)  + '\n' +\
            '  <li>ex (film x dir): ' + str(self.__ex)  + '\n' +\
            '  <li>ey (film y dir): ' + str(self.__ey)  + '\n' +\
            '</ul>\n'
        return ret_s


# OpenGL camera
class GLCamera(Camera):
    """OpenGL camera
    """
    # default constructor
    def __init__(self):
        """default constructor. (public)"""
        super(GLCamera, self).__init__()

    # get class name
    def get_classname(self):
        """get class name. (public)
        \return 'GLCamera'
        """
        return 'GLCamera'



# IFGI camera
class IFGICamera(Camera):
    """IFGI camera"""

    # default constructor
    def __init__(self):
        """default constructor. (public)"""
        super(IFGICamera, self).__init__()

    # class name
    def get_classname(self):
        """get class name. (public)
        \return 'IFGICamera'"""
        return 'IFGICamera'

#
# main test
#
if __name__ == '__main__':
    gl_cam   = GLCamera()
    gl_cam.print_obj()

    ifgi_cam = IFGICamera()
    ifgi_cam.print_obj()
