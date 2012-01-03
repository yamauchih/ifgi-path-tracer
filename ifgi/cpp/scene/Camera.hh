//----------------------------------------------------------------------
// ifgi c++ implementation: Camera.hh
// Copyright (C) 2010-2011 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief ifgi Camera C++ implementation
#ifndef IFGI_PATH_TRACER_IFGI_CPP_SCENE_CAMERA_HH
#define IFGI_PATH_TRACER_IFGI_CPP_SCENE_CAMERA_HH

#include "cpp/base/Vector.hh"
#include <cassert>
#include <cmath>

namespace ifgi
{
//----------------------------------------------------------------------
// forward declaration
class Ray;
class Film;

//----------------------------------------------------------------------
/// a camera
class Camera
{
public:
    /// Projection Mode
    enum Camera_projection_mode_e {
        /// perspective mode
        Camera_Perspective,
        /// perspective orthographic mode
        Camera_Orthographic,
        /// camera projection sentinel
        CAMERA_PROJECTION_MODE_COUNT
    };

    /// Eye Position
    enum Camera_eye_position_e {
        /// eye center position
        Camera_Eye_Center,
        /// eye left position
        Camera_Eye_Left,
        /// eye right position
        Camera_Eye_Right,
        /// camera eye position sentinel
        CAMERA_EYE_POSITION_COUNT
    };

public:
    /// default constructor
    Camera()
        :
        m_eye_pos (0.0f, 0.0f,  5.0f),
        m_view_dir(0.0f, 0.0f, -1.0f),
        m_up_dir  (0.0f, 1.0f,  0.0f),
        m_fovy_rad(45.0 * M_PI / 180.0),
        m_aspect_ratio(1.0),
        m_z_near(0.1),
        m_z_far(1000.0),
        m_projection(Camera_Perspective),
        // target distance = |eye_pos - lookat_point|
        m_target_dist(1.0),
        m_focal_length(1.0),
        m_lens_screen_dist(1.0),
        m_lens_film_dist(1.0),
        // lower bottom corner
        m_LB_corner(-1.0f, -1.0f,  0.0f),
        // x direction base vector
        m_ex(1.0f, 0.0f,  0.0f),
        // y direction base vector
        m_ey(0.0f, 1.0f,  0.0f),
        // films: framebuffer
        // m_film(),
        m_ortho_width(1.0)
    {
        this->compute_screen_parameter();
        // print "called Camara.__init__()"
    }

    /// destructor
    ~Camera()
    {
        // empty
    }

    /// get class name.
    /// \return "Camera"
    std::string get_classname() const
    {
        return std::string("Camera");
    }

    /// set eye position.
    /// \param[in] eye_pos eye position
    void set_eye_pos(Float32_3 const & eye_pos)
    {
        m_eye_pos = eye_pos;
        this->compute_screen_parameter();
    }

    /// get eye position.
    /// \return eye position
    Float32_3 const & get_eye_pos() const
    {
        return m_eye_pos;
    }

    /// set view direction.
    /// \return view direction (normalized).
    void set_view_dir(Float32_3 const & view_dir)
    {
        m_view_dir = view_dir;
        m_view_dir.normalize();
        this->compute_screen_parameter();
    }

    /// get view direction.
    /// \return view direction
    Float32_3 const & get_view_dir() const
    {
        return m_view_dir;
    }

    /// set lookat position.
    /// \param[in] eye_pos    eye position
    /// \param[in] lookat_pos lookat position
    void set_eye_lookat_pos(Float32_3 const & eye_pos, Float32_3 const & lookat_pos)
    {
        m_eye_pos  = eye_pos;
        lookat_vec = lookat_pos - eye_pos;
        dist = lookat_vec.norm();
        assert(dist > 0);

        m_target_dist = dist;
        m_view_dir = lookat_vec / dist;
        this->compute_screen_parameter();
    }

    /// set up direction.
    /// \param[in] up direction
    void set_up_dir(Float32_3 const & up_dir)
    {
        m_up_dir = up_dir;
        m_up_dir.normalize();
        this->compute_screen_parameter();
    }

    /// get up direction.
    /// \return up direction
    Float32_3 const & get_up_dir() const
    {
        return m_up_dir;
    }

    /// set fovy as radian.
    /// \param[in] fovy_rad field of view in radian.
    void set_fovy_rad(Float32 fovy_rad)
    {
        m_fovy_rad = fovy_rad;
    }

    /// get fovy as radian.
    /// \return field of view Y. (radian)
    Float32 get_fovy_rad() const
    {
        return m_fovy_rad;
    }

    /// set aspect ratio.
    /// \param[in] aspect_ratio aspect ratio.
    void set_aspect_ratio(Float32 aspect_ratio)
    {
        m_aspect_ratio = aspect_ratio;
    }

    /// get aspect ratio.
    /// \return aspect ratio.
    Float32 get_aspect_ratio() const
    {
        return m_aspect_ratio;
    }

    /// set z near plane distance.
    /// \param[in] z_near z near plane distance.
    void set_z_near(Float32 z_near)
    {
        m_z_near = z_near;
    }

    /// get z near plane distance.
    /// \return z near plane distance.
    Float32 get_z_near() const
    {
        return m_z_near;
    }

    /// set z far plane distance.
    /// \param[in] z_far z far plane distance.
    void set_z_far(Float32 z_far)
    {
        /// print "set_z_far: ", z_far
        m_z_far = z_far;
    }

    /// get z far plane distance.
    /// \return z far plane distance.
    Float32 get_z_far()const
    {
        return m_z_far;
    }

    /// get projection mode.
    /// \return projection mode
    Camera_projection_mode_e get_projection() const
    {
        return m_projection;
    }

    /// set projection mode.
    /// \param[in] projection projection mode
    void set_projection(Camera_projection_mode_e projection)
    {
        m_projection = projection;
    }

    /// get gluLookAt() parameters.
    /// \param[in] eye_type eye position for stereo {EyeCenter,
    /// EyeLeft, EyeRight}, NIN Not implemented now.
    /// \return lookat parameters as 3x3 matrix
    // get_lookat(Camera_eye_position_e eye_position)
    // {
    //     assert(_eye_type == EyePosition.EyeCenter);
    //     assert(m_target_dist  != 0);
    //     assert(m_focal_length != 0);
    //     return [m_eye_pos,
    //             m_eye_pos + m_target_dist * m_view_dir,
    //             m_up_dir];
    // }

    /// Get the camera coordinate system as OpenGL (left hand);
    ///
    /// Get orthonrmal basis for camera coordinate system {_ex,_ey,_ez}.
    /// \return [ex, ey, ez]  [right, up, viewingDriection()] system.
    // def get_coordinate_system()
    // {
    //     ex  = cross(m_view_dir, m_up_dir);
    //     ex /= numpy.linalg.norm(ex);
    //     ey  = cross(ex, m_view_dir);
    //     ey /= numpy.linalg.norm(ey);
    //     assert(abs(numpy.linalg.norm(m_view_dir) - 1) < 0.000001);

    //     /// print "ex = " + str(ex);
    //     /// print "ey = " + str(ey);
    //     /// print "ez = " + str(m_view_dir);

    //     return [ex, ey, m_view_dir];
    // }

    /// get target (lookat point) distance.
    /// \return eye to lookat point (target) distance.
    Float32 get_target_distance() const
    {
        return m_target_dist;
    }

    /// set target (lookat point) distance.
    /// \param[in] target_dist target distance.
    void set_target_distance(Float32 target_dist)
    {
        m_target_dist = target_dist;
    }

    /// get lens to screen distance.
    /// \return lens to screen distance.
    Float32 get_lens_to_screen_distance() const
    {
        return m_lens_screen_dist;
    }

    /// get focal length
    /// \return focal length.
    Float32 get_focal_length() const
    {
        return m_focal_length;
    }

    /// set focal length.
    /// \param[in] focal_len focal length.
    void set_focal_length(Float32 focal_len)
    {
        m_focal_length = focal_len;
    }

    /// get get lens to screen distance.
    /// \return lens to screen distance.
    Float32 get_lens_to_screen_distance() const
    {
        return m_lens_screen_dist;
    }

    /// set get lens to screen distance.
    /// \param[in] l2s_dist lens to screen distance.
    void set_lens_to_screen_distance(Float32 l2s_dist)
    {
        this->__lens_screen_dist = l2s_dist;
    }

    /// get lens to fim distance.
    /// \return lens to screen distance.
    /// NIN
    Float32 get_lens_to_film_distance() const
    {
        return m_lens_film_dist;
    }

    /// set lens to fim distance.
    /// \param[in] lens to film distance.
    void set_lens_to_film_distance(Float32 l2f_dist)
    {
        m_lens_film_dist = l2f_dist;
    }

    /// get ray.
    /// \param[in] dx delta x normalized screen coordinate [0,1]
    /// \param[in] dy delta y normalized screen coordinate [0,1]
    /// \return a ray
    /// FIXME: don't new the Ray
    Ray get_ray(Float32 dx, Float32 dy)
    {
        target =  m_LB_corner + dx * m_ex + dy * m_ey;
        vdir   =  target - m_eye_pos;
        vdir.normalize();
        return Ray(m_eye_pos, vdir, m_z_near, m_z_far);
    }

    /// set a film.
    /// \param[in] film_name the film name
    /// \param[in] film       film instance
    // void set_film(_film_name, film)
    // {
    //     m_film[_film_name] = film;
    // }

    /// get a film
    /// \return film, exception if no film_name exists.
    Film const & get_film(std::string const & film_name)
    {
        return m_film[_film_name];
    }

    /// set orthogonal projection width.
    /// \param[in] ortho_width orthogonal projection width size.
    void set_ortho_width(Float32 ortho_width)
    {
        m_ortho_width = ortho_width;
    }

    /// get orthogonal projection width.
    /// \return ortho_width
    Float32 get_ortho_width() const
    {
        return m_ortho_width;
    }

    /// query glFrustum parameter to this camera.
    /// \return [left, right, bottom, top]
    // def query_frustum(_eyeposition)
    // {
    //     left   = 0.0
    //     right  = 0.0
    //     top    = 0.0
    //     bottom = 0.0

    //     /// FIXME
    //     NIN_eye_separation = 1.0

    //     if(m_projection == ProjectionMode.Perspective){
    //         half_fovy_rad = m_fovy_rad * 0.5; /// cf. Paul Bourke, 3D Stereo ...
    //         wd2  = m_z_near * tan(half_fovy_rad);
    //         ndfl = m_z_near / m_focal_length;

    //         if(_eyeposition == EyePosition.EyeCenter){
    //             left  = - m_aspect_ratio * wd2;
    //             right = - left;
    //             top   =   wd2;
    //             bottom= - wd2;
    //         }
    //         else if(_eyeposition == EyePosition.EyeLeft){
    //             left  = - m_aspect_ratio * wd2 + 0.5 * NIN_eye_separation * ndfl
    //             right =   m_aspect_ratio * wd2 + 0.5 * NIN_eye_separation * ndfl;
    //             top   =   wd2;
    //             bottom= - wd2;
    //         }
    //         else if(_eyeposition == EyePosition.EyeRight){
    //             left  = -m_aspect_ratio * wd2 -0.5 * NIN_eye_separation * ndfl;
    //             right =  m_aspect_ratio * wd2 - 0.5 * NIN_eye_separation * ndfl;
    //             top   =  wd2;
    //             bottom= -wd2;
    //         }
    //         else{
    //             wd2   = m_ortho_width * 0.5;
    //             left  = -m_aspect_ratio * wd2;
    //             right = -left;
    //             top   =  wd2;
    //             bottom= -wd2;
    //         }
    //     }
    //     return [left, right, top, bottom];
    // }

    /// set camera parameters.
    /// deep copy the camera parameters.
    /// \param[in] othercam other camera.
    /// NIN: operator=
    // void set_camera_param(Camera const & othercam)
    // {
    //     /// deep copy
    //     m_eye_pos      = othercam.get_eye_pos(). copy();
    //     m_view_dir     = othercam.get_view_dir().copy();
    //     m_up_dir       = othercam.get_up_dir().  copy();
    //     m_fovy_rad     = othercam.get_fovy_rad();
    //     m_aspect_ratio = othercam.get_aspect_ratio();
    //     m_z_near       = othercam.get_z_near();
    //     m_z_far        = othercam.get_z_far();
    //     m_projection   = othercam.get_projection();
    //     m_target_dist  = othercam.get_target_distance();
    //     m_focal_length = othercam.get_focal_length();
    //     m_lens_screen_dist = othercam.get_lens_to_screen_distance();
    //     m_lens_film_dist = othercam.get_lens_to_film_distance();
    //     m_LB_corner    = othercam.__LB_corner
    //     m_ex           = othercam.__ex
    //     m_ey           = othercam.__ey
    //         }

    /// for debug
    // void print_obj() const
    // {
    //     /// print this object for debug.
    //     cname = this->get_classname();
    //     print "#" + cname + "::eye_pos = "  + str(m_eye_pos);
    //     print "#" + cname + "::view_dir = " + str(m_view_dir);
    //     print "#" + cname + "::up_dir = "   + str(m_up_dir);
    //     print "#" + cname + "::fovy_rad = " + str(m_fovy_rad);
    //     print "#" + cname + "::aspect_ratio = " + str(m_aspect_ratio);
    //     print "#" + cname + "::z_near = "   + str(m_z_near);
    //     print "#" + cname + "::z_far = "    + str(m_z_far);
    //     print "#" + cname + "::projection = " + str(m_projection);
    //     print "#" + cname + "::target_dist = " + str(m_target_dist);
    //     print "#" + cname + "::focal_length = " + str(m_focal_length);

    //     print "#" + cname + "::lens_screen_dist = " +\
    //         str(m_lens_screen_dist);
    //     print "#" + cname + "::lens_film_dist = " + str(m_lens_film_dist);
    //     print "#" + cname + "::LB_corner = " + str(m_LB_corner);
    //     print "#" + cname + "::ex = "      + str(m_ex);
    //     print "#" + cname + "::ey = "      + str(m_ey);
    //     print "#" + cname + "::film = "    + str(m_film);
    // }

    /// get camera information as html format.
    /// \return camera information in html string.
    // std::string get_html_info() const
    // {
    //     ret_s = "<h2>Camera information</h2>\n"                       +
    //         "<ul>\n"                                                  +
    //         "  <li><b>Class name:</b> " + this->get_classname() + "\n" +
    //         "  <li>eye_pos: "      + str(m_eye_pos)       + "\n" +
    //         "  <li>view_dir: "     + str(m_view_dir)      + "\n" +
    //         "  <li>up_dir: "       + str(m_up_dir)        + "\n" +
    //         "  <li>fovy_rad: "     + str(m_fovy_rad)      + "\n" +
    //         "  <li>aspect_ratio: " + str(m_aspect_ratio)  + "\n" +
    //         "  <li>z_near: "       + str(m_z_near)        + "\n" +
    //         "  <li>z_far: "        + str(m_z_far)         + "\n" +
    //         "  <li>projection: "   + str(m_projection)    + "\n" +
    //         "  <li>target_dist: "  + str(m_target_dist)   + "\n" +
    //         "  <li>focal_length: " + str(m_focal_length)  + "\n" +
    //         "  <li>lens to screen distance: " +
    //         str(m_lens_screen_dist)  + "\n" +
    //         "  <li>lens to film distance: " +
    //         str(m_lens_film_dist)  + "\n" +
    //         "  <li>Left bottom corner: " + str(m_LB_corner)  + "\n" +
    //         "  <li>ex (film x dir){ " + str(m_ex)   + "\n" +
    //         "  <li>ey (film y dir){ " + str(m_ey)   + "\n" +
    //         "  <li>ey (films){ "      + str(m_film) + "\n" +
    //         "</ul>\n"
    //     return ret_s;
    // }

    /// get camera parameter key list.
    /// For ordered access.
    /// \return ordered parameter key list
    // def get_param_key() const
    // {
    //     param_list = [
    //         "eye_pos",
    //         "view_dir",
    //         "up_dir",
    //         "fovy_rad",
    //         "aspect_ratio",
    //         "z_near",
    //         "z_far",
    //         "projection",
    //         "target_dist",
    //         "focal_length",
    //         "lens_screen_dist",
    //         "lens_film_dist"
    //         ];
    //     return param_list;
    // }

    /// get camera parameter type dictionary.
    /// \return parameter key, typename dictionary
    // def get_typename_dict(){
    //     typename_dict = {
    //         "eye_pos":          "float_3",
    //         "view_dir":         "float_3",
    //         "up_dir":           "float_3",
    //         "fovy_rad":         "float",
    //         "aspect_ratio":     "float",
    //         "z_near":           "float",
    //         "z_far":            "float",
    //         "projection":       "enum_ProjectionMode",
    //         "target_dist":      "float",
    //         "focal_length":     "float",
    //         "lens_screen_dist": "float",
    //         "lens_film_dist":   "float"
    //     };
    //     return typename_dict;
    // }

    //------------------------------------------------------------
    // configurable
    //------------------------------------------------------------

    // void set_config_dict(_config){
    //     /// set camera parameter configuration dictionary.
    //     This is configurable.
    //     /// \param[in] config configuration dictionary.

    //     if "eye_pos" in config:
    //         /// Note: config["eye_pos"] is QString, conevrt to str
    //         ep = numpy_util.str2array(str(_config["eye_pos"]));
    //         print ep
    //         if len(ep) != 3:
    //             raise StandardError("eye_pos must be a float_3, but " +\
    //                                     str(_config["eye_pos"]));
    //         this->set_eye_pos(ep);

    //     if "view_dir" in config:
    //         vd = numpy_util.str2array(str(_config["view_dir"]));
    //         print vd
    //         if len(vd) != 3:
    //             raise StandardError("view_dir must be a float_3.");

    //         this->set_view_dir(vd);

    //     if "up_dir" in config:
    //         ud = numpy_util.str2array(str(_config["up_dir"]));
    //         print ud
    //         if len(ud) != 3:
    //             raise StandardError("up_dir must be a float_3.");
    //         this->set_up_dir(ud);

    //     if "fovy_rad" in config:
    //         this->set_fovy_rad(float(_config["fovy_rad"]));

    //     if "aspect_ratio" in config:
    //         this->set_aspect_ratio(float(_config["aspect_ratio"]));

    //     if "z_near" in config:
    //         this->set_z_near(float(_config["z_near"]));
    //         /// print "DEBUG: set z_near", float(_config["z_near"]);

    //     if "z_far" in config:
    //         this->set_z_far(float(_config["z_far"]));
    //         /// print "DEBUG: set z_far", float(_config["z_far"]);

    //     if "projection" in config:
    //         this->set_projection(str(_config["projection"]));

    //     if "target_dist" in config:
    //         this->set_target_distance(float(_config["target_dist"]));

    //     if "focal_length" in config:
    //         this->set_focal_length(float(_config["focal_length"]));

    //     if "lens_screen_dist" in config:
    //         this->set_lens_to_screen_distance(float(_config["lens_screen_dist"]));

    //     if "lens_film_dist" in config:
    //         this->set_lens_to_film_distance(float(_config["lens_film_dist"]));
    // }

    // def get_config_dict(){
    //     /// get camera parameter configurarion dictionary.
    //     This is configuable.
    //     /// \return parameter key, value dictionary

    //     new_cam = copy.deepcopy();
    //     value_dict = {
    //         "eye_pos":          numpy_util.array2str(new_cam.get_eye_pos()),
    //         "view_dir":         numpy_util.array2str(new_cam.get_view_dir()),
    //         "up_dir":           numpy_util.array2str(new_cam.get_up_dir()),
    //         "fovy_rad":         str(new_cam.get_fovy_rad()),
    //         "aspect_ratio":     str(new_cam.get_aspect_ratio()),
    //         "z_near":           str(new_cam.get_z_near()),
    //         "z_far":            str(new_cam.get_z_far()),
    //         "projection":       str(new_cam.get_projection()),
    //         "target_dist":      str(new_cam.get_target_distance()),
    //         "focal_length":     str(new_cam.get_focal_length()),
    //         "lens_screen_dist": str(new_cam.get_lens_to_screen_distance()),
    //         "lens_film_dist":   str(new_cam.get_lens_to_film_distance());
    //         }
    //     return value_dict;
    // }

private:
    /// compute screen parameters.
    /// _LB_corner, _ex, _ey  are computed.
    ///
    ///   +-----------+--
    ///   |           | ^
    ///   |           | |
    ///   |           | _ey
    ///   |           | |
    /// LB+-----------+--
    ///   |-- _ex -->|
    void compute_screen_parameter()
    {
        // get center
        Float32_3 const center = m_eye_pos + m_lens_screen_dist * m_view_dir;

        // get left bottom corner
        Float32 const halffovy   = 0.5 * m_fovy_rad;
        Float32 const halfwidth  = m_lens_screen_dist * tan(halffovy);
        Float32 const halfheight = m_lens_screen_dist * tan(halffovy * m_aspect_ratio);

        // get basis
        [m_ex, m_ey, m_view_dir] = this->get_coordinate_system();

        m_LB_corner = (center - (halfwidth * m_ex + halfheight * m_ey));

        // print "DEBUG: halfwidth  = " + str(halfwidth);
        // print "DEBUG: halfheight = " + str(halfheight);

        m_ex = 2.0 * halfwidth  * m_ex;
        m_ey = 2.0 * halfheight * m_ey;
    }

private:
    /// eye position
    Float32_3 m_eye_pos;
    /// viewing direction
    Float32_3 m_view_dir;
    /// up vector
    Float32_3 m_up_dir;
    /// Y field of view in radian
    Float32 m_fovy_rad;
    /// aspect ratio
    Float32 m_aspect_ratio;
    /// z plane near distance
    Float32 m_z_near;
    /// z plane far distance
    Float32 m_z_far;
    /// camera projection mode
    Camera_projection_mode_e m_projection;
    /// target distance = |eye_pos - lookat_point|
    Float32 m_target_dist;
    /// focul length
    Float32 m_focal_length;
    /// lens to screen distance
    Float32 m_lens_screen_dist;
    /// lens to film distance
    Float32 m_lens_film_dist;
    /// lower bottom corner position of the screen
    Float32_3 m_LB_corner;
    /// x direction base vector
    Float32_3 m_ex;
    /// y direction base vector
    Float32_3 m_ey;
    /// films map: framebuffer map
    std::map< std::string, Film * > m_film_map;
    /// orthogonal projection width
    Float32 m_ortho_width;
};


/// main test

/// if _name__ == "__main__":
///     gl_cam   = GLCamera();
///     gl_cam.print_obj();

///     ifgi_cam = IFGICamera();
///     ifgi_cam.print_obj();

} // namespace ifgi

#endif // #ifndef IFGI_PATH_TRACER_IFGI_CPP_SCENE_CAMERA_HH
