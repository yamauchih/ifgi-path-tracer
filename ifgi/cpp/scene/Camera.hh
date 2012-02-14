//----------------------------------------------------------------------
// ifgi c++ implementation: Camera.hh
// Copyright (C) 2010-2012 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief ifgi Camera C++ implementation
#ifndef IFGI_PATH_TRACER_IFGI_CPP_SCENE_CAMERA_HH
#define IFGI_PATH_TRACER_IFGI_CPP_SCENE_CAMERA_HH

#include <cpp/base/Vector.hh>
#include <cpp/base/Dictionary.hh>

#include <cassert>
#include <cmath>
#include <map>

#include "Ray.hh"

namespace ifgi
{
//----------------------------------------------------------------------
// forward declaration
class ImageFilm;

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

    /// the film map type
    typedef std::map< std::string, ImageFilm * > FilmMap;

public:
    /// default constructor
    Camera();

    /// copy constructor. deep copy
    /// \param[in] rhs right hand side (copy source)
    Camera(Camera const & rhs);

    /// destructor
    ~Camera();

    /// operator=. deep copy
    /// \param[in] rhs right hand side (copy source)
    const Camera& operator=(Camera const & rhs);

    /// get class name.
    /// \return "Camera"
    std::string get_classname() const;

    /// set camera name.
    /// \param[in] cam_name camera name
    void set_camera_name(std::string const & cam_name);

    /// get camera name.
    /// \return this camera's name
    std::string get_camera_name() const;

    /// set eye position.
    /// \param[in] eye_pos eye position
    void set_eye_pos(Scalar_3 const & eye_pos);

    /// get eye position.
    /// \return eye position
    Scalar_3 const & get_eye_pos() const;

    /// set view direction.
    /// \return view direction (normalized).
    void set_view_dir(Scalar_3 const & view_dir);

    /// get view direction.
    /// \return view direction
    Scalar_3 const & get_view_dir() const;

    /// set lookat position.
    /// \param[in] eye_pos    eye position
    /// \param[in] lookat_pos lookat position
    void set_eye_lookat_pos(Scalar_3 const & eye_pos,
                            Scalar_3 const & lookat_pos);

    /// set up direction.
    /// \param[in] up direction
    void set_up_dir(Scalar_3 const & up_dir);

    /// get up direction.
    /// \return up direction
    Scalar_3 const & get_up_dir() const;

    /// set fovy as radian.
    /// \param[in] fovy_rad field of view in radian.
    void set_fovy_rad(Scalar fovy_rad);

    /// get fovy as radian.
    /// \return field of view Y. (radian)
    Scalar get_fovy_rad() const;

    /// set aspect ratio.
    /// \param[in] aspect_ratio aspect ratio.
    void set_aspect_ratio(Scalar aspect_ratio);

    /// get aspect ratio.
    /// \return aspect ratio.
    Scalar get_aspect_ratio() const;

    /// set z near plane distance.
    /// \param[in] z_near z near plane distance.
    void set_z_near(Scalar z_near);

    /// get z near plane distance.
    /// \return z near plane distance.
    Scalar get_z_near() const;

    /// set z far plane distance.
    /// \param[in] z_far z far plane distance.
    void set_z_far(Scalar z_far);

    /// get z far plane distance.
    /// \return z far plane distance.
    Scalar get_z_far()const;

    /// get projection mode.
    /// \return projection mode
    Uint32 get_projection() const;

    /// set projection mode.
    /// \param[in] projection projection mode
    void set_projection(Uint32 projection);

    /// get gluLookAt() parameters.
    /// \param[in] eye_type eye position for stereo {EyeCenter,
    /// EyeLeft, EyeRight}, NIN Not implemented now.
    /// \return lookat parameters as 3x3 matrix
    // get_lookat(Camera_eye_position_e eye_position)

    /// Get the camera coordinate system as OpenGL (left hand);
    ///
    /// Get orthonrmal basis for camera coordinate system {ex,ey,ez}.
    ///
    /// \param[out] rightvec right direction vector
    /// \param[out] upvec    up direction vector
    /// \param[out] viewvec  view direction vector
    // void get_coordinate_system(Scalar_3 & rightvec,
    //                            Scalar_3 & upvec,
    //                            Scalar_3 & viewvec) const;
    static inline void get_coordinate_system(Scalar_3 const & view_dir,
                                             Scalar_3 const & up_dir,
                                             Scalar_3 & ex,
                                             Scalar_3 & ey,
                                             Scalar_3 & ez)
    {
        ex = cross(view_dir, up_dir);
        ex.normalize();
        ey = cross(ex, view_dir);
        ey.normalize();
        // assumed view dir is normalized
        assert(fabs(view_dir.norm() - 1.0) < 0.000001);
        ez = view_dir;

        // ex  = numpy.cross(self.__view_dir, self.__up_dir)
        // ex /= numpy.linalg.norm(ex);
        // ey  = cross(ex, m_view_dir);
        // ey /= numpy.linalg.norm(ey);
        // assert(abs(numpy.linalg.norm(m_view_dir) - 1) < 0.000001);
        // print "ex = " + str(ex);
        // print "ey = " + str(ey);
        // print "ez = " + str(m_view_dir);
        // return [ex, ey, m_view_dir];
    }

    /// get target (lookat point) distance.
    /// \return eye to lookat point (target) distance.
    Scalar get_target_distance() const;

    /// set target (lookat point) distance.
    /// \param[in] target_dist target distance.
    void set_target_distance(Scalar target_dist);

    /// get lens to screen distance.
    /// \return lens to screen distance.
    Scalar get_lens_to_screen_distance() const;

    /// get focal length
    /// \return focal length.
    Scalar get_focal_length() const;

    /// set focal length.
    /// \param[in] focal_len focal length.
    void set_focal_length(Scalar focal_len);

    /// get lens to fim distance.
    /// \return lens to screen distance.
    /// NIN
    Scalar get_lens_to_film_distance() const;

    /// set lens to fim distance.
    /// \param[in] lens to film distance.
    void set_lens_to_film_distance(Scalar l2f_dist);

    /// get ray.
    /// \param[in] dx delta x normalized screen coordinate [0,1]
    /// \param[in] dy delta y normalized screen coordinate [0,1]
    /// \param[out] a ray initialized for (dx, dy)
    void get_ray(Scalar dx, Scalar dy, Ray & out_ray)
    {
        assert((dx >= Scalar(0.0)) && (dx <= Scalar(1.0)));
        assert((dy >= Scalar(0.0)) && (dy <= Scalar(1.0)));

        Scalar_3 const target =  m_LB_corner + dx * m_ex + dy * m_ey;
        Scalar_3 vdir   =  target - m_eye_pos;
        vdir.normalize();

        out_ray.initialize(m_eye_pos, vdir, m_z_near, m_z_far);
    }

    /// set orthogonal projection width.
    /// \param[in] ortho_width orthogonal projection width size.
    void set_ortho_width(Scalar ortho_width);

    /// get orthogonal projection width.
    /// \return ortho_width
    Scalar get_ortho_width() const;

    /// set image resolution x
    /// \param[in] res_x image resolution x
    void set_resolution_x(Sint32 res_x);

    /// get image resolution x
    /// \return image resolution x
    Sint32 get_resolution_x() const;

    /// get image resolution y
    /// \param[in] res_y image resolution y
    void set_resolution_y(Sint32 res_y);

    /// get image resolution y
    /// \return image resolution y
    Sint32 get_resolution_y() const;

    /// set a film. The film is owned by this instance.
    ///
    /// When set the same name film twice, casts exception.
    ///
    /// \param[in] p_img_film film instance
    void set_film(ImageFilm * p_img_film);

    /// peek a film
    /// \param[in] film_name the film name
    /// \return reference to the film, exception if no film_name exists.
    ImageFilm * peek_film(std::string const & film_name);

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

    //     print "#" + cname + "::lens_screen_dist = " +
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

    /// set camera parameter configuration dictionary.
    /// This is configurable.
    /// \param[in] config configuration dictionary.
    void set_config_dict(Dictionary const & config);

    /// get camera parameter configurarion dictionary.
    /// This is configuable.
    /// \return parameter key, value dictionary
    Dictionary get_config_dict() const;

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
    void compute_screen_parameter();

    /// clear film map
    void clear_film_map();

    /// deep copy function
    /// \param[in] rhs copy origin
    void deep_copy(Camera const & rhs);

private:
    /// camera name
    std::string m_camera_name;
    /// eye position
    Scalar_3 m_eye_pos;
    /// viewing direction
    Scalar_3 m_view_dir;
    /// up vector
    Scalar_3 m_up_dir;
    /// Y field of view in radian
    Scalar m_fovy_rad;
    /// aspect ratio
    Scalar m_aspect_ratio;
    /// z plane near distance
    Scalar m_z_near;
    /// z plane far distance
    Scalar m_z_far;
    /// camera projection mode: This type is Camera_projection_mode_e,
    /// but for Dictionary conversion Uint32
    Uint32 m_projection;
    /// target distance = |eye_pos - lookat_point|
    Scalar m_target_dist;
    /// focul length
    Scalar m_focal_length;
    /// lens to screen distance
    Scalar m_lens_screen_dist;
    /// lens to film distance
    Scalar m_lens_film_dist;
    /// lower bottom corner position of the screen
    Scalar_3 m_LB_corner;
    /// x direction base vector
    Scalar_3 m_ex;
    /// y direction base vector
    Scalar_3 m_ey;
    /// orthogonal projection width
    Scalar m_ortho_width;
    /// image resolution x
    Sint32 m_resolution_x;
    /// image resolution y
    Sint32 m_resolution_y;
    /// films map: framebuffer map
    FilmMap m_film_map;
};

} // namespace ifgi
#endif // #ifndef IFGI_PATH_TRACER_IFGI_CPP_SCENE_CAMERA_HH
