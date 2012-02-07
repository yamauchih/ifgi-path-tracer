//----------------------------------------------------------------------
// ifgi c++ implementation: Ray.hh
// Copyright (C) 2010-2012 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief a ray
#ifndef IFGI_PATH_TRACER_IFGI_CPP_SCENE_RAY_HH
#define IFGI_PATH_TRACER_IFGI_CPP_SCENE_RAY_HH

#include <limits>
#include <sstream>

#include <cpp/base/types.hh>

namespace ifgi
{
/// Ray class
class Ray
{
public:
    /// default constructor.
    Ray()
        :
        m_origin(Scalar_3(0.0, 0.0, 0.0)),
        m_dir(   Scalar_3(0.0, 0.0, 1.0)),
        m_min_t(std::numeric_limits< Scalar >::min()),
        m_max_t(std::numeric_limits< Scalar >::max()),
        m_path_length(0),
        m_reflectance(Scalar(1.0), Scalar(1.0), Scalar(1.0), Scalar(1.0)),
        m_intensity(  Scalar(0.0), Scalar(0.0), Scalar(0.0), Scalar(1.0))
    {
        // empty
    }


    /// constructor.
    /// \param[in] origin ray origin
    /// \param[in] dir    ray direction
    /// \param[in] min_t ray minimal distance (less than this
    /// distance doesn't intersect);
    /// \param[in] max_t ray maximal distance (more than this
    /// distance doesn't intersect);
    Ray(Scalar_3 const & origin,
        Scalar_3 const & dir,
        Scalar min_t,
        Scalar max_t)
        :
        m_origin(origin),
        m_dir(dir),
        m_min_t(min_t),
        m_max_t(max_t),
        m_path_length(0),
        m_reflectance(Scalar(1.0), Scalar(1.0), Scalar(1.0), Scalar(1.0)),
        m_intensity(  Scalar(0.0), Scalar(0.0), Scalar(0.0), Scalar(1.0))
    {
        // empty
    }

    /// get class name
    /// \return class name
    std::string get_classname() const {
        return "Ray";
    }

    /// initialize
    ///
    /// \param[in] origin ray origin
    /// \param[in] dir    ray direction
    /// \param[in] min_t ray minimal distance (less than this
    /// distance doesn't intersect);
    /// \param[in] max_t ray maximal distance (more than this
    /// distance doesn't intersect);
    void initialize(Scalar_3 const & origin,
                    Scalar_3 const & dir,
                    Scalar min_t,
                    Scalar max_t)
    {
        m_origin = origin;
        m_dir    = dir;
        m_min_t  = min_t;
        m_max_t  = max_t;
        m_path_length = 0;
        m_reflectance = Scalar_4(Scalar(1.0), Scalar(1.0),
                                 Scalar(1.0), Scalar(1.0));
        m_intensity   = Scalar_4(Scalar(0.0), Scalar(0.0),
                                 Scalar(0.0), Scalar(1.0));
    }


    /// set the ray origin.
    /// \param[in] origin ray origin.
    ///
    void set_origin(Scalar_3 const & origin)
    {
        m_origin = origin;
    }

    /// get the ray origin.
    /// \return ray origin.
    Scalar_3 const & get_origin() const
    {
        return m_origin;
    }

    /// set the ray direction vector.
    /// \param[in] dir ray direction
    void set_dir(Scalar_3 const & dir)
    {
        m_dir = dir;
    }

    /// get the ray direction vector.
    /// \return ray dir.
    Scalar_3 const & get_dir() const
    {
        return m_dir;
    }

    /// get minimal ray distance.
    /// \return ray min_t.
    Scalar get_min_t() const
    {
        return m_min_t;
    }

    /// get maximal ray distance.
    /// \return ray max_t.
    Scalar get_max_t() const
    {
        return m_max_t;
    }

    /// set path length
    /// \param[in] path_length path length to set
    void set_path_length(Sint32 path_length)
    {
        m_path_length = path_length;
    }

    /// get path length
    Sint32 get_path_length() const 
    {
        return m_path_length;
    }

    /// string representation of this object
    /// \return string representation of this object
    std::string to_string() const
    {
        std::stringstream sstr;
        sstr << "orig: " << m_origin << " dir: " << m_dir
             << " range: [" << m_min_t << " " << m_max_t << "], path_len: "
             << m_path_length;
        return sstr.str();
    }

private:
    /// ray origin
    Scalar_3 m_origin;
    /// ray direction
    Scalar_3 m_dir;
    /// ray minimal dist
    Scalar   m_min_t;
    /// ray maximal dist
    Scalar   m_max_t;
    /// current path length
    Sint32 m_path_length;
    /// reflectance
    Scalar_4 m_reflectance;
    /// intensity
    Scalar_4 m_intensity;
};

} // namespace ifgi
#endif // #ifndef IFGI_PATH_TRACER_IFGI_CPP_SCENE_RAY_HH
