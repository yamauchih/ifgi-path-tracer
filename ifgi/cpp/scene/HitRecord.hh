//----------------------------------------------------------------------
// ifgi c++ implementation: HitRecord.hh
// Copyright (C) 2010-2012 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief a hit record
#ifndef IFGI_PATH_TRACER_IFGI_CPP_SCENE_HITRECORD_HH
#define IFGI_PATH_TRACER_IFGI_CPP_SCENE_HITRECORD_HH

#include <limits>
#include <string>

#include <cpp/base/types.hh>
#include <cpp/base/OrthonomalBasis.hh>

namespace ifgi
{
class Primitive;

/// HitRecord
/// hit record. members are public.
class HitRecord
{
public:
    /// default constructor
    HitRecord()
        :
        m_dist(std::numeric_limits< Scalar >::max()),
        m_p_hit_primitive(0),
        m_intersect_pos(Scalar(0.0), Scalar(0.0), Scalar(0.0)),
        m_hit_onb(),
        m_hit_material_index(-1)
    {
        // empty
    }

    /// initialize
    void initialize()
    {
        m_dist = std::numeric_limits< Scalar >::max();
        m_p_hit_primitive = 0;
        m_intersect_pos = Scalar_3(Scalar(0.0), Scalar(0.0), Scalar(0.0));
        // m_hit_on_basis()
        m_hit_material_index = -1;
    }

    /// get class name
    /// \return class name
    std::string get_classname() const
    {
        return "HitRecord";
    }

    /// get string representation
    /// \return string representation
    std::string to_string() const;

public:
    /// ray hit distance
    Scalar m_dist;
    /// hit primitive (currently primitive pointer. later a Tag)
    Primitive * m_p_hit_primitive;
    /// intersection point
    Scalar_3 m_intersect_pos;
    /// hit point orthogonal basis
    OrthonomalBasis m_hit_onb;
    /// hit material index
    Sint32 m_hit_material_index;
};


} // namespace ifgi
#endif // #ifndef IFGI_PATH_TRACER_IFGI_CPP_SCENE_HITRECORD_HH
