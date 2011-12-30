//----------------------------------------------------------------------
// ifgi c++ implementation: IPrimitive.hh
// Copyright (C) 2010-2011 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief primitive triangle

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
// BBox32 const & Triangle::get_bbox() const
// {
//     if(m_bbox == None){
//         raise StandardError, ("Invalid triangle, no bounding box.");
//     }
//     return m_bbox;
// }

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
    // Cramer's rule based ray-triangle intersection

    // get s1
    // Float32_3 const e1  = m_vertex[1] - m_vertex[0];
    // Float32_3 const e2  = m_vertex[2] - m_vertex[0];
    // Float32_3 const s1  = cross(ray.get_dir(), e2);
    // Float32   const div = dot(s1, e1);
    // if(div == 0.0){
    //     return false;
    // }
    // Float32 const inv_div = 1.0f / div;

    // // get barycentric coord b1
    // Float32_3 const d  = ray.get_origin() - m_vertex[0];
    // Float32   const b1 = dot(d, s1) * inv_div;
    // if((b1 < 0.0) || (b1 > 1.0)){
    //     return false;
    // }

    // // get barycentric coord b2
    // Float32_3 const s2 = cross(d, e1);
    // Float32   const b2 = dot(_ray.get_dir(), s2) * inv_div;
    // if ((b2 < 0.0) || ((b1 + b2) > 1.0)){
    //     return false;
    // }

    // // get intersection point (distance t);
    // Float32 const t = dot(e2, s2) * inv_div;
    // if((t < ray.get_min_t()) || (t > ray.get_max_t())){
    //     return false;
    // }

    std::cout << "NIN HitRecord" << std::endl;
    assert(false);
    // // print "Hit: t = " + str(t) + ", b1 = " + str(b1) + ", b2 = " + str(b2);
    // hr.dist = t;
    // hr.intersect_pos = m_vertex[0] + b1 * e1 + b2 * e2;
    // hr.hit_primitive = this;
    // hr.hit_basis = OrthonomalBasis.OrthonomalBasis();
    // hr.hit_basis.init_from_uv(e1, e2); /// set normal
    return true;
}

//----------------------------------------------------------------------
// Set triangle vertices.
void Triangle::set_vertex(Float32_3 const & v0,
                          Float32_3 const & v1,
                          Float32_3 const & v2)

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
} // namespace ifgi
