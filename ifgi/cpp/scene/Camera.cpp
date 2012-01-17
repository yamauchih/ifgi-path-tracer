//----------------------------------------------------------------------
// ifgi c++ implementation: Camera.hh
// Copyright (C) 2010-2012 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief ifgi Camera C++ implementation

#include "Camera.hh"
#include "ImageFilm.hh"

namespace ifgi
{
//----------------------------------------------------------------------
// default constructor
Camera::Camera()
    :
    m_eye_pos (0.0f, 0.0f,  5.0f),
    m_view_dir(0.0f, 0.0f, -1.0f),
    m_up_dir  (0.0f, 1.0f,  0.0f),
    m_fovy_rad(45.0 * M_PI / 180.0),
    m_aspect_ratio(1.0),
    m_z_near(0.1),
    m_z_far(1000.0),
    m_projection(Camera_Perspective),
    m_target_dist(1.0),    // target distance = |eye_pos - lookat_point|
    m_focal_length(1.0),
    m_lens_screen_dist(1.0),
    m_lens_film_dist(1.0),
    m_LB_corner(-1.0f, -1.0f,  0.0f),
    m_ex(1.0f, 0.0f,  0.0f),
    m_ey(0.0f, 1.0f,  0.0f),
    m_ortho_width(1.0)
    // films: framebuffer
    // m_film()
{
    this->compute_screen_parameter();
    // print "called Camara.__init__()"
}

//----------------------------------------------------------------------
// copy constructor
Camera::Camera(Camera const & rhs)
{
    this->deep_copy(rhs);
}

//----------------------------------------------------------------------
// destructor
Camera::~Camera()
{
    // delete owner memory on heap
    this->clear_film_map();
}

//----------------------------------------------------------------------
// operator=
Camera const & Camera::operator=(Camera const & rhs)
{
    if(this != &rhs){
        this->deep_copy(rhs);
    }
    return *this;
}

//----------------------------------------------------------------------
// get class name.
std::string Camera::get_classname() const
{
    return std::string("Camera");
}

//----------------------------------------------------------------------
// set eye position.
void Camera::set_eye_pos(Float32_3 const & eye_pos)
{
    m_eye_pos = eye_pos;
    this->compute_screen_parameter();
}

//----------------------------------------------------------------------
// get eye position.
Float32_3 const & Camera::get_eye_pos() const
{
    return m_eye_pos;
}

//----------------------------------------------------------------------
// set view direction.
void Camera::set_view_dir(Float32_3 const & view_dir)
{
    m_view_dir = view_dir;
    m_view_dir.normalize();
    this->compute_screen_parameter();
}

//----------------------------------------------------------------------
// get view direction.
Float32_3 const & Camera::get_view_dir() const
{
    return m_view_dir;
}

//----------------------------------------------------------------------
// set lookat position.
void Camera::set_eye_lookat_pos(Float32_3 const & eye_pos,
                                Float32_3 const & lookat_pos)
{
    m_eye_pos  = eye_pos;
    Float32_3 const lookat_vec = lookat_pos - eye_pos;
    Float32 const dist = lookat_vec.norm();
    assert(dist > 0);

    m_target_dist = dist;
    m_view_dir = lookat_vec * (1.0/dist);
    this->compute_screen_parameter();
}

//----------------------------------------------------------------------
// set up direction.
void Camera::set_up_dir(Float32_3 const & up_dir)
{
    m_up_dir = up_dir;
    m_up_dir.normalize();
    this->compute_screen_parameter();
}

//----------------------------------------------------------------------
// get up direction.
Float32_3 const & Camera::get_up_dir() const
{
    return m_up_dir;
}

//----------------------------------------------------------------------
// set fovy as radian.
void Camera::set_fovy_rad(Float32 fovy_rad)
{
    m_fovy_rad = fovy_rad;
}

//----------------------------------------------------------------------
// get fovy as radian.
Float32 Camera::get_fovy_rad() const
{
    return m_fovy_rad;
}

//----------------------------------------------------------------------
// set aspect ratio.
void Camera::set_aspect_ratio(Float32 aspect_ratio)
{
    m_aspect_ratio = aspect_ratio;
}

//----------------------------------------------------------------------
// get aspect ratio.
Float32 Camera::get_aspect_ratio() const
{
    return m_aspect_ratio;
}

//----------------------------------------------------------------------
// set z near plane distance.
void Camera::set_z_near(Float32 z_near)
{
    m_z_near = z_near;
}

//----------------------------------------------------------------------
// get z near plane distance.
Float32 Camera::get_z_near() const
{
    return m_z_near;
}

//----------------------------------------------------------------------
// set z far plane distance.
void Camera::set_z_far(Float32 z_far)
{
//----------------------------------------------------------------------
    /// print "set_z_far: ", z_far
    m_z_far = z_far;
}

//----------------------------------------------------------------------
// get z far plane distance.
Float32 Camera::get_z_far()const
{
    return m_z_far;
}

//----------------------------------------------------------------------
// get projection mode.
Uint32 Camera::get_projection() const
{
    return m_projection;
}

//----------------------------------------------------------------------
// set projection mode.
void Camera::set_projection(Uint32 projection)
{
    m_projection = projection;
}

//----------------------------------------------------------------------
// get gluLookAt() parameters.
// \param[in] eye_type eye position for stereo {EyeCenter,
// EyeLeft, EyeRight}, NIN Not implemented now.
// \return lookat parameters as 3x3 matrix
// Camera::get_lookat(Camera_eye_position_e eye_position)
// {
//     assert(_eye_type == EyePosition.EyeCenter);
//     assert(m_target_dist  != 0);
//     assert(m_focal_length != 0);
//     return [m_eye_pos,
//             m_eye_pos + m_target_dist * m_view_dir,
//             m_up_dir];
// }

//----------------------------------------------------------------------
// Get the camera coordinate system as OpenGL (left hand);
//
// Get orthonrmal basis for camera coordinate system {_ex,_ey,_ez}.
// \return [ex, ey, ez]  [right, up, viewingDriection()] system.
// def Camera::get_coordinate_system()
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

//----------------------------------------------------------------------
// get target (lookat point) distance.
Float32 Camera::get_target_distance() const
{
    return m_target_dist;
}

//----------------------------------------------------------------------
// set target (lookat point) distance.
void Camera::set_target_distance(Float32 target_dist)
{
    m_target_dist = target_dist;
}

//----------------------------------------------------------------------
// get lens to screen distance.
Float32 Camera::get_lens_to_screen_distance() const
{
    return m_lens_screen_dist;
}

//----------------------------------------------------------------------
// get focal length
Float32 Camera::get_focal_length() const
{
    return m_focal_length;
}

//----------------------------------------------------------------------
// set focal length.
void Camera::set_focal_length(Float32 focal_len)
{
    m_focal_length = focal_len;
}

//----------------------------------------------------------------------
// get lens to fim distance.
Float32 Camera::get_lens_to_film_distance() const
{
    return m_lens_film_dist;
}

//----------------------------------------------------------------------
// set lens to fim distance.
void Camera::set_lens_to_film_distance(Float32 l2f_dist)
{
    m_lens_film_dist = l2f_dist;
}

//----------------------------------------------------------------------
// get ray.
// \param[in] dx delta x normalized screen coordinate [0,1]
// \param[in] dy delta y normalized screen coordinate [0,1]
// \return a ray
// FIXME: don't new the Ray
// Ray get_ray(Float32 dx, Float32 dy)
// {
//     target =  m_LB_corner + dx * m_ex + dy * m_ey;
//     vdir   =  target - m_eye_pos;
//     vdir.normalize();
//     return Ray(m_eye_pos, vdir, m_z_near, m_z_far);
// }
// NIN

// set a film.
// \param[in] film_name the film name
// \param[in] film       film instance
// void set_film(_film_name, film)
// {
//     m_film[_film_name] = film;
// }

// get a film
// \return film, exception if no film_name exists.
// ImageFilm const & get_film(std::string const & film_name)
// {
//     return m_film[_film_name];
// }
// NIN

//----------------------------------------------------------------------
// set orthogonal projection width.
void Camera::set_ortho_width(Float32 ortho_width)
{
    m_ortho_width = ortho_width;
}

//----------------------------------------------------------------------
// get orthogonal projection width.
Float32 Camera::get_ortho_width() const
{
    return m_ortho_width;
}

//----------------------------------------------------------------------
// query glFrustum parameter to this camera.
// \return [left, right, bottom, top]
// def Camera::query_frustum(_eyeposition)
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

// set camera parameters.
// deep copy the camera parameters.
// \param[in] othercam other camera.
// NIN: operator=
// void Camera::set_camera_param(Camera const & othercam)
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

// for debug
// void Camera::print_obj() const
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

// get camera information as html format.
// \return camera information in html string.
// std::string Camera::get_html_info() const
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

// get camera parameter key list.
// For ordered access.
// \return ordered parameter key list
// def Camera::get_param_key() const
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

// get camera parameter type dictionary.
// \return parameter key, typename dictionary
// def Camera::get_typename_dict(){
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

// set camera parameter configuration dictionary.
void Camera::set_config_dict(Dictionary const & dict)
{
    if(dict.is_defined("eye_pos")){
        Float32_3 const ep = dict.get< Float32_3 > ("eye_pos");
        this->set_eye_pos(ep);
    }

    if(dict.is_defined("view_dir")){
        Float32_3 const vd = dict.get< Float32_3 >("view_dir");
        this->set_view_dir(vd);
    }

    if(dict.is_defined("up_dir")){
        Float32_3 const ud = dict.get< Float32_3 >("up_dir");
        this->set_up_dir(ud);
    }

    if(dict.is_defined("fovy_rad")){
        this->set_fovy_rad(dict.get< Float32 >("fovy_rad"));
    }

    if(dict.is_defined("aspect_ratio")){
        this->set_aspect_ratio(dict.get< Float32 >("aspect_ratio"));
    }

    if(dict.is_defined("z_near")){
        this->set_z_near(dict.get< Float32 >("z_near"));
        /// print "DEBUG: set z_near", float(_config["z_near"]);
    }

    if(dict.is_defined("z_far")){
        this->set_z_far(dict.get< Float32 >("z_far"));
        /// print "DEBUG: set z_far", dict.get< Float32 >("z_far");
    }

    if(dict.is_defined("projection")){
        this->set_projection(dict.get< Uint32 >("projection"));
    }

    if(dict.is_defined("target_dist")){
        this->set_target_distance(dict.get< Float32 >("target_dist"));
    }

    if(dict.is_defined("focal_length")){
        this->set_focal_length(dict.get< Float32 >("focal_length"));
    }

    // if(dict.is_defined("lens_screen_dist")){
    //     this->set_lens_to_screen_distance(dict.get< Float32 >("lens_screen_dist"));
    // }

    if(dict.is_defined("lens_film_dist")){
        this->set_lens_to_film_distance(dict.get< Float32 >("lens_film_dist"));
    }
}

//----------------------------------------------------------------------
// get camera parameter configurarion dictionary.
Dictionary Camera::get_config_dict() const
{
    Dictionary value_dict;

    value_dict.set("eye_pos",          this->get_eye_pos());
    value_dict.set("view_dir",         this->get_view_dir());
    value_dict.set("up_dir",           this->get_up_dir());
    value_dict.set("fovy_rad",         this->get_fovy_rad());
    value_dict.set("aspect_ratio",     this->get_aspect_ratio());
    value_dict.set("z_near",           this->get_z_near());
    value_dict.set("z_far",            this->get_z_far());
    value_dict.set("projection",       this->get_projection());
    value_dict.set("target_dist",      this->get_target_distance());
    value_dict.set("focal_length",     this->get_focal_length());
    value_dict.set("lens_screen_dist", this->get_lens_to_screen_distance());
    value_dict.set("lens_film_dist",   this->get_lens_to_film_distance());

    return value_dict;
}

//----------------------------------------------------------------------
// compute screen parameters.
void Camera::compute_screen_parameter()
{
    // // get center
    // Float32_3 const center = m_eye_pos + m_lens_screen_dist * m_view_dir;

    // // get left bottom corner
    // Float32 const halffovy   = 0.5 * m_fovy_rad;
    // Float32 const halfwidth  = m_lens_screen_dist * tan(halffovy);
    // Float32 const halfheight = m_lens_screen_dist * tan(halffovy * m_aspect_ratio);

    // // get basis
    // [m_ex, m_ey, m_view_dir] = this->get_coordinate_system();

    // m_LB_corner = (center - (halfwidth * m_ex + halfheight * m_ey));

    // // print "DEBUG: halfwidth  = " + str(halfwidth);
    // // print "DEBUG: halfheight = " + str(halfheight);

    // m_ex = 2.0 * halfwidth  * m_ex;
    // m_ey = 2.0 * halfheight * m_ey;

    // NIN
}

//----------------------------------------------------------------------
// clear film map
void Camera::clear_film_map()
{
    for(FilmMap::iterator fi = this->m_film_map.begin();
        fi != this->m_film_map.end(); ++fi)
    {
        if(fi->second != 0){
            delete fi->second;
            fi->second = 0;
        }
    }

    m_film_map.clear();
}

//----------------------------------------------------------------------
// deep copy function
void Camera::deep_copy(Camera const & rhs)
{
    m_eye_pos          = rhs.m_eye_pos;
    m_view_dir         = rhs.m_view_dir;
    m_up_dir           = rhs.m_up_dir;
    m_fovy_rad         = rhs.m_fovy_rad;
    m_aspect_ratio     = rhs.m_aspect_ratio;
    m_z_near           = rhs.m_z_near;
    m_z_far            = rhs.m_z_far;
    m_projection       = rhs.m_projection;
    m_target_dist      = rhs.m_target_dist;
    m_focal_length     = rhs.m_focal_length;
    m_lens_screen_dist = rhs.m_lens_screen_dist;
    m_lens_film_dist   = rhs.m_lens_film_dist;
    m_LB_corner        = rhs.m_LB_corner;
    m_ex               = rhs.m_ex;
    m_ey               = rhs.m_ey;
    m_ortho_width      = rhs.m_ortho_width;

    // delete own films
    this->clear_film_map();
    // copy with new
    for(FilmMap::const_iterator fi = rhs.m_film_map.begin();
        fi != rhs.m_film_map.end(); ++fi)
    {
        // deep copy relies on ImageFilm's copy constructor.
        ImageFilm * p_dup = new ImageFilm(*(fi->second));
        this->m_film_map[fi->first] = p_dup;
    }
}
//----------------------------------------------------------------------
} // namespace ifgi
