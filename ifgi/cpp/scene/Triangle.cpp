//----------------------------------------------------------------------
// ifgi c++ implementation: IPrimitive.hh
// Copyright (C) 2010-2012 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief primitive triangle

#include <cpp/base/Exception.hh>

#include "HitRecord.hh"
#include "Ray.hh"
#include "Triangle.hh"

namespace ifgi
{
//----------------------------------------------------------------------

// default constructor.
Triangle::Triangle()
    :
    IPrimitive()
    // m_vertex()
    // m_bbox()
{
    // empty
}

//----------------------------------------------------------------------
// destructor.
Triangle::~Triangle()
{
    // NIN
}

//----------------------------------------------------------------------
// get class name. interface method.
std::string Triangle::get_classname() const
{
    return std::string("Triangle");
}

//----------------------------------------------------------------------
// get the bounding box. interface method.
BBoxScalar const & Triangle::get_bbox() const
{
    if(m_bbox.get_rank() < 2){
        throw Exception("Invalid triangle, no bounding box.");
    }
    return m_bbox;
}

//----------------------------------------------------------------------
// can a triangle intersect with a ray? Yes.
bool Triangle::can_intersect() const
{
    return true;
}

//----------------------------------------------------------------------
// compute ray intersection. interface method.
bool Triangle::ray_intersect(Ray const & ray, HitRecord & hr) const
{
    // std::cout << "Triangle::ray_intersect" << std::endl;
    // Cramer's rule based ray-triangle intersection

    // get s1
    Scalar_3 const e1  = m_vertex[1] - m_vertex[0];
    Scalar_3 const e2  = m_vertex[2] - m_vertex[0];
    Scalar_3 const s1  = cross(ray.get_dir(), e2);
    Scalar   const div = s1.dot(e1);
    if(div == 0.0){
        // DELETEME std::cout << "nohit: dotprod" << std::endl;
        return false;
    }
    Scalar const inv_div = Scalar(1.0) / div;

    // get barycentric coord b1
    Scalar_3 const d  = ray.get_origin() - m_vertex[0];
    Scalar   const b1 = d.dot(s1) * inv_div;
    if((b1 < 0.0) || (b1 > 1.0)){
        // std::cout << "nohit: b1" << std::endl;
        return false;
    }

    // get barycentric coord b2
    Scalar_3 const s2 = cross(d, e1);
    Scalar   const b2 = ray.get_dir().dot(s2) * inv_div;
    if((b2 < 0.0) || ((b1 + b2) > 1.0)){
        // DELETEME std::cout << "nohit: b1" << std::endl;
        return false;
    }

    // get intersection point (distance t);
    Scalar const t = e2.dot(s2) * inv_div;
    if((t < ray.get_min_t()) || (t > ray.get_max_t())){
        // DELETEME std::cout << "nohit: backside" << std::endl;
        return false;
    }

    // std::cout << "Hit: t = " << t << ", b1 = " << b1 << ", b2 = " << b2 << std::endl;
    hr.m_dist = t;
    hr.m_intersect_pos = m_vertex[0] + b1 * e1 + b2 * e2;
    // hr.m_p_hit_primitive = this;
    hr.m_hit_onb.init_from_uv(e1, e2); // set the normal of hit object

    return true;
}

//----------------------------------------------------------------------
// Set triangle vertices.
void Triangle::set_vertex(Scalar_3 const & v0,
                          Scalar_3 const & v1,
                          Scalar_3 const & v2)

{
    m_vertex[0] = v0;
    m_vertex[1] = v1;
    m_vertex[2] = v2;

    this->update_bbox();
}

//----------------------------------------------------------------------
// update bounding box
void Triangle::update_bbox()
{
    m_bbox.invalidate();
    m_bbox.insert_point(m_vertex[0]);
    m_bbox.insert_point(m_vertex[1]);
    m_bbox.insert_point(m_vertex[2]);
}

//----------------------------------------------------------------------
// get string representation
std::string Triangle::to_string() const
{
    std::stringstream sstr;
    sstr << "[" << m_vertex[0] << "]["
         << m_vertex[1] << "]["
         << m_vertex[2] << "]";
    return sstr.str();
}

//----------------------------------------------------------------------
} // namespace ifgi
