#!/usr/bin/env python
#
# Copyright (C) 2010-2011 Yamauchi, Hitoshi
#

"""Camera module
\file
\brief camera"""

import math, copy
import numpy
from ifgi.base import enum, numpy_util, ifgimath

import Film, Ray

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
        # target distance = |eye_pos - lookat_point|
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
        self.__resolution_x = 128
        self.__resolution_y = 64
        # films: framebuffer
        self.__film = {}

        self.__ortho_width = 1.0

        self.__compute_screen_parameter()

        # print 'called Camara.__init__()'


    def get_classname(self):
        """get class name.
        This must be reimplemented in the inherited class.
        \return None"""
        assert 0, "get_classname must be implemented in a derived class."
        return None


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


    def set_eye_pos(self, _eye_pos):
        """set eye position.
        \param[in] _eye_pos eye position"""
        self.__eye_pos = _eye_pos
        self.__compute_screen_parameter()


    def get_eye_pos(self):
        """get eye position.
        \return eye position float_3"""
        return self.__eye_pos


    def set_view_dir(self, _view_dir):
        """set view direction.
        \return view direction (normalized)."""
        self.__view_dir = ifgimath.normalize_vec(_view_dir)
        self.__compute_screen_parameter()


    def get_view_dir(self):
        """get view direction.
        \return view direction"""
        return self.__view_dir


    def set_eye_lookat_pos(self, _eye_pos, _lookat_pos):
        """set lookat position.
        \param[in] _eye_pos    eye position
        \param[in] _lookat_pos lookat position
        """
        self.__eye_pos  = _eye_pos
        lookat_vec      = _lookat_pos - _eye_pos
        dist = numpy.linalg.norm(lookat_vec)
        assert(dist > 0)
        self.__target_dist = dist
        self.__view_dir = lookat_vec / dist
        self.__compute_screen_parameter()


    def set_up_dir(self, _up_dir):
        """set up direction.
        \return up direction float_3."""
        self.__up_dir = ifgimath.normalize_vec(_up_dir)
        self.__compute_screen_parameter()

    def get_up_dir(self):
        """get up direction.
        \return up direction"""
        return self.__up_dir


    def set_fovy_rad(self, _fovy_rad):
        """set fovy as radian.
        \param[in] _fovy_rad field of view in radian."""
        self.__fovy_rad = _fovy_rad


    def get_fovy_rad(self):
        """get fovy as radian.
        \return field of view Y. (radian)"""
        return self.__fovy_rad


    def set_aspect_ratio(self, _aspect_ratio):
        """set aspect ratio.
        \param[in] _aspect_ratio aspect ratio. """
        self.__aspect_ratio = _aspect_ratio


    def get_aspect_ratio(self):
        """get aspect ratio.
        \return aspect ratio."""
        return self.__aspect_ratio


    def set_z_near(self, _z_near):
        """set z near plane distance.
        \param[in] _z_near z near plane distance."""
        self.__z_near = _z_near


    def get_z_near(self):
        """get z near plane distance.
        \return z near plane distance."""
        return self.__z_near


    def set_z_far(self, _z_far):
        """set z far plane distance.
        \param[in] _z_far z far plane distance."""
        # print 'set_z_far: ', _z_far
        self.__z_far = _z_far


    def get_z_far(self):
        """get z far plane distance.
        \return z far plane distance."""
        return self.__z_far


    def get_projection(self):
        """get projection mode.
        \return projection mode ('Perspective', 'Orthographic')"""
        return self.__projection

    def set_projection(self, _projection):
        """set projection mode.
        \param[in] _projection projection mode"""
        self.__projection = _projection

    # get gluLookAt() parameters
    def get_lookat(self, _eye_type):
        """get gluLookAt() parameters.
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
        """Get the camera coordinate system as OpenGL

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


    def set_resolution_x(self, _res_x):
        """set resolution x.
        \param[in] _res_x resolution x
        """
        assert(_res_x > 0)
        self.__resolution_x = _res_x


    def get_resolution_x(self):
        """get resolution x.
        \return get resolution x
        """
        return self.__resolution_x


    def set_resolution_y(self, _res_y):
        """set resolution y.
        \param[in] _res_y resolution y
        """
        assert(_res_y > 0)
        self.__resolution_y = _res_y


    def get_resolution_y(self):
        """get resolution y.
        \return get resolution y
        """
        return self.__resolution_y


    # get target (lookat point) distance
    def get_target_distance(self):
        """get target (lookat point) distance.
        \return eye to lookat point (target) distance."""

        return self.__target_dist


    def set_target_distance(self, _target_dist):
        """set target (lookat point) distance.
        \param[in] _target_dist target distance."""
        self.__target_dist = _target_dist

    # get focal length
    def get_focal_length(self):
        """get focal length.
        \return focal length."""

        return self.__focal_length

    def set_focal_length(self, _focal_len):
        """set focal length.
        \param[in] _focal_len focal length."""
        self.__focal_length = _focal_len

    def get_lens_to_screen_distance(self):
        """get get lens to screen distance.
        \return lens to screen distance."""

        return self.__lens_screen_dist

    def set_lens_to_screen_distance(self, _l2s_dist):
        """set get lens to screen distance.
        \param[in] _l2s_dist lens to screen distance."""
        self.__lens_screen_dist = _l2s_dist

    # get lens to film distance
    def get_lens_to_film_distance(self):
        """get lens to fim distance.
        \return lens to screen distance."""
        # NIN
        return self.__lens_film_dist

    def set_lens_to_film_distance(self, _l2f_dist):
        """set lens to fim distance.
        \param[in] lens to film distance."""
        self.__lens_film_dist = _l2f_dist

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

    # set a film
    def set_film(self, _film_name, _film):
        """set a film.
        \param[in] _film_name the film name
        \param[in] _film       film instance
        """
        self.__film[_film_name] = _film

    # get a film
    def get_film(self, _film_name):
        """get film.
        \return film, exception if no _film_name exists."""
        return self.__film[_film_name]

    def set_ortho_width(self, _ortho_width):
        """set orthogonal projection width.
        \param[in] _ortho_width orthogonal projection width size."""
        self.__ortho_width = _ortho_width

    def get_ortho_width(self):
        """get orthogonal projection width.
        \return _ortho_width"""
        return self.__ortho_width


    def query_frustum(self, _eyeposition):
        """query glFrustum parameter to this camera.
        \return [left, right, bottom, top]
        """
        left   = 0.0
        right  = 0.0
        top    = 0.0
        bottom = 0.0

        # FIXME
        NIN_eye_separation = 1.0

        if(self.__projection == ProjectionMode.Perspective):
            half_fovy_rad = self.__fovy_rad * 0.5 # cf. Paul Bourke, 3D Stereo ...
            wd2  = self.__z_near * math.tan(half_fovy_rad)
            ndfl = self.__z_near / self.__focal_length

            if(_eyeposition == EyePosition.EyeCenter):
                left  = - self.__aspect_ratio * wd2
                right = - left
                top   =   wd2
                bottom= - wd2
            elif(_eyeposition == EyePosition.EyeLeft):
                left  = - self.__aspect_ratio * wd2 + 0.5 * NIN_eye_separation * ndfl
                right =   self.__aspect_ratio * wd2 + 0.5 * NIN_eye_separation * ndfl;
                top   =   wd2
                bottom= - wd2
            elif(_eyeposition == EyePosition.EyeRight):
                left  = -self.__aspect_ratio * wd2 -0.5 * NIN_eye_separation * ndfl;
                right =  self.__aspect_ratio * wd2 - 0.5 * NIN_eye_separation * ndfl;
                top   =  wd2;
                bottom= -wd2;
        else:
            wd2   = self.__ortho_width * 0.5;
            left  = -self.__aspect_ratio * wd2;
            right = -left;
            top   =  wd2;
            bottom= -wd2;

        return [left, right, top, bottom]




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
        self.__resolution_x = _othercam.__resolution_x
        self.__resolution_y = _othercam.__resolution_y



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
        print '#' + cname + '::resolution_x = ' + str(self.__resolution_x)
        print '#' + cname + '::resolution_y = ' + str(self.__resolution_y)
        print '#' + cname + '::film = '    + str(self.__film)

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
            '  <li>ex (film x dir): ' + str(self.__ex)   + '\n' +\
            '  <li>ey (film y dir): ' + str(self.__ey)   + '\n' +\
            '  <li>resolution x: '    + str(self.__resolution_x) + '\n' +\
            '  <li>resolution y: '    + str(self.__resolution_y) + '\n' +\
            '  <li>films: '           + str(self.__film) + '\n' +\
            '</ul>\n'
        return ret_s

    def get_param_key(self):
        """get camera parameter key list.
        For ordered access.
        \return ordered parameter key list
        """
        param_list = [
            'eye_pos',
            'view_dir',
            'up_dir',
            'fovy_rad',
            'aspect_ratio',
            'z_near',
            'z_far',
            'projection',
            'target_dist',
            'focal_length',
            'lens_screen_dist',
            'lens_film_dist',
            'resolution_x',
            'resolution_y'
            ]
        return param_list

    def get_typename_dict(self):
        """get camera parameter type dictionary.
        \return parameter key, typename dictionary
        """
        typename_dict = {
            'eye_pos':          'float_3',
            'view_dir':         'float_3',
            'up_dir':           'float_3',
            'fovy_rad':         'float',
            'aspect_ratio':     'float',
            'z_near':           'float',
            'z_far':            'float',
            'projection':       'enum_ProjectionMode',
            'target_dist':      'float',
            'focal_length':     'float',
            'lens_screen_dist': 'float',
            'lens_film_dist':   'float',
            'resolution_x':     'int',
            'resolution_y':     'int'
            }
        return typename_dict

    #  ------------------------------------------------------------
    #  configurable
    #  ------------------------------------------------------------

    def set_config_dict(self, _config):
        """set camera parameter configuration dictionary.
        This is configurable.
        \param[in] _config configuration dictionary.
        """
        if 'eye_pos' in _config:
            # Note: _config['eye_pos'] is QString, conevrt to str
            ep = numpy_util.str2array(str(_config['eye_pos']))
            print ep
            if len(ep) != 3:
                raise StandardError('eye_pos must be a float_3, but ' +\
                                        str(_config['eye_pos']))
            self.set_eye_pos(ep)

        if 'view_dir' in _config:
            vd = numpy_util.str2array(str(_config['view_dir']))
            print vd
            if len(vd) != 3:
                raise StandardError('view_dir must be a float_3.')

            self.set_view_dir(vd)

        if 'up_dir' in _config:
            ud = numpy_util.str2array(str(_config['up_dir']))
            print ud
            if len(ud) != 3:
                raise StandardError('up_dir must be a float_3.')
            self.set_up_dir(ud)

        if 'fovy_rad' in _config:
            self.set_fovy_rad(float(_config['fovy_rad']))

        if 'aspect_ratio' in _config:
            self.set_aspect_ratio(float(_config['aspect_ratio']))

        if 'z_near' in _config:
            self.set_z_near(float(_config['z_near']))
            # print 'DEBUG: set z_near', float(_config['z_near'])

        if 'z_far' in _config:
            self.set_z_far(float(_config['z_far']))
            # print 'DEBUG: set z_far', float(_config['z_far'])

        if 'projection' in _config:
            self.set_projection(str(_config['projection']))

        if 'target_dist' in _config:
            self.set_target_distance(float(_config['target_dist']))

        if 'focal_length' in _config:
            self.set_focal_length(float(_config['focal_length']))

        if 'lens_screen_dist' in _config:
            self.set_lens_to_screen_distance(float(_config['lens_screen_dist']))

        if 'lens_film_dist' in _config:
            self.set_lens_to_film_distance(float(_config['lens_film_dist']))


    def get_config_dict(self):
        """get camera parameter configurarion dictionary.
        This is configuable.
        \return parameter key, value dictionary
        """
        new_cam = copy.deepcopy(self)
        value_dict = {
            'eye_pos':          numpy_util.array2str(new_cam.get_eye_pos()),
            'view_dir':         numpy_util.array2str(new_cam.get_view_dir()),
            'up_dir':           numpy_util.array2str(new_cam.get_up_dir()),
            'fovy_rad':         str(new_cam.get_fovy_rad()),
            'aspect_ratio':     str(new_cam.get_aspect_ratio()),
            'z_near':           str(new_cam.get_z_near()),
            'z_far':            str(new_cam.get_z_far()),
            'projection':       str(new_cam.get_projection()),
            'target_dist':      str(new_cam.get_target_distance()),
            'focal_length':     str(new_cam.get_focal_length()),
            'lens_screen_dist': str(new_cam.get_lens_to_screen_distance()),
            'lens_film_dist':   str(new_cam.get_lens_to_film_distance()),
            'resolution_x':     str(new_cam.get_resolution_x()),
            'resolution_y':     str(new_cam.get_resolution_y())
            }
        return value_dict




# OpenGL camera
class GLCamera(Camera):
    """OpenGL camera
    """
    # default constructor
    def __init__(self):
        """default constructor."""
        super(GLCamera, self).__init__()

    # get class name
    def get_classname(self):
        """get class name.
        \return 'GLCamera'
        """
        return 'GLCamera'



# IFGI camera
class IFGICamera(Camera):
    """IFGI camera"""

    # default constructor
    def __init__(self):
        """default constructor."""
        super(IFGICamera, self).__init__()

    # class name
    def get_classname(self):
        """get class name.
        \return 'IFGICamera'"""
        return 'IFGICamera'

#
# main test
#
# if __name__ == '__main__':
#     gl_cam   = GLCamera()
#     gl_cam.print_obj()
#
#     ifgi_cam = IFGICamera()
#     ifgi_cam.print_obj()
