//----------------------------------------------------------------------
// ifgi c++ implementation: TriMesh.hh
// Copyright (C) 2010-2012 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief simple triangle mesh primitive

#include "TriMesh.hh"

#include "Triangle.hh"
#include "HitRecord.hh"

namespace ifgi
{
//----------------------------------------------------------------------
// default constructor
TriMesh::TriMesh()
    :
    IPrimitive(),
    // super(TriMesh, ).set_name(_mash_name),
    // super(TriMesh, ).set_material_name(_mat_name),
    /// geometry information
    // m_vertex_vec(),
    // m_face_idx_vec(),
    // m_texcoord_vec(),
    // m_texcoord_idx_vec(),
    // m_normal_vec(),
    // m_normal_idx_vec(),
    // m_bbox(),
    m_material_index(-1)
{
    // empty
}

//----------------------------------------------------------------------
// destructor
TriMesh::~TriMesh()
{
    m_vertex_vec.clear();
    m_face_idx_vec.clear();
    m_texcoord_vec.clear();
    m_texcoord_idx_vec.clear();
    m_normal_vec.clear();
    m_normal_idx_vec.clear();
    m_bbox.invalidate();
    m_material_index = -2;
}

//----------------------------------------------------------------------
// get class name. interface method.
std::string TriMesh::get_classname() const
{
    return std::string("TriMesh");
}

//----------------------------------------------------------------------
// get the bounding box. interface method.
BBoxScalar const & TriMesh::get_bbox() const
{
    return m_bbox;
}

//----------------------------------------------------------------------
// can TriMesh primitive intersect with a ray? no.
bool TriMesh::can_intersect() const
{
    return false;
}

//----------------------------------------------------------------------
// set geometry data
void TriMesh::set_data(
    std::vector< Scalar_3 > const & vlist,
    std::vector< Sint32_3 > const & fidxlist,
    std::vector< Scalar_3 > const & tclist,
    std::vector< Sint32_3 > const & tcidxlist,
    std::vector< Scalar_3 > const & nlist,
    std::vector< Sint32_3 > const & nidxlist)
{
    assert(!vlist.empty()); // at least, some points must be there.
    m_vertex_vec       = vlist;
    m_face_idx_vec     = fidxlist;
    m_texcoord_vec     = tclist;
    m_texcoord_idx_vec = tcidxlist;
    m_normal_vec       = nlist;
    m_normal_idx_vec   = nidxlist;
    this->update_bbox();
}

//----------------------------------------------------------------------
// get summary information
std::string TriMesh::get_info_summary() const
{
    std::stringstream sstr;
    sstr << "# vertices     = " << m_vertex_vec.size()       << "\n"
         << "# faces        = " << m_face_idx_vec.size()     << "\n"
         << "# texcoords    = " << m_texcoord_vec.size()     << "\n"
         << "# texcoord idx = " << m_texcoord_idx_vec.size() << "\n"
         << "# normal       = " << m_normal_vec.size()       << "\n"
         << "# normal idx   = " << m_normal_idx_vec.size()   << "\n"
        // NIN << "bbox           = " << this->get_bbox()          << "\n"
         << "material idx   = " << m_material_index;

    return sstr.str();
}

//----------------------------------------------------------------------
// update bounding box according to current vertex list.
void TriMesh::update_bbox()
{
    m_bbox.invalidate();  // reset the bbox
    for(std::vector< Scalar_3 >::const_iterator vi = m_vertex_vec.begin();
        vi != m_vertex_vec.end(); ++vi)
    {
        m_bbox.insert_point(*vi);
    }
}

//----------------------------------------------------------------------
// is this valid object?
bool TriMesh::is_valid() const
{
    if(!m_vertex_vec.empty()){
        return true;
    }
    return false;
}

//----------------------------------------------------------------------
// compute a ray and a trimesh intersection.
bool TriMesh::ray_intersect(Ray const & ray, HitRecord & trimesh_hr) const
{
    trimesh_hr.m_dist = std::numeric_limits< Scalar >::max();
    // DELETEME trimesh_hr.m_p_hit_primitive = 0;
    HitRecord tmp_hr;

    Triangle tri; // FIXME. This triangle is constructed every intersection test.

    for(std::vector< Sint32_3 >::const_iterator fi = m_face_idx_vec.begin();
        fi != m_face_idx_vec.end(); ++fi)
    {
        assert((*fi)[0] < static_cast< Sint32 >(m_vertex_vec.size()));
        assert((*fi)[1] < static_cast< Sint32 >(m_vertex_vec.size()));
        assert((*fi)[2] < static_cast< Sint32 >(m_vertex_vec.size()));

        tri.set_vertex(m_vertex_vec[(*fi)[0]],
                       m_vertex_vec[(*fi)[1]],
                       m_vertex_vec[(*fi)[2]]);
        if(!(tri.ray_intersect(ray, tmp_hr))){
            if(trimesh_hr.m_dist > tmp_hr.m_dist){
                trimesh_hr.m_dist          = tmp_hr.m_dist;
                trimesh_hr.m_intersect_pos = tmp_hr.m_intersect_pos;
                // FIXME should be a triangle? But here local created
                // one can not be kept in this design. How this
                // primitive is used?
                // trimesh_hr.m_p_hit_primitive = this; May not used
                trimesh_hr.m_hit_onb = tmp_hr.m_hit_onb;
                trimesh_hr.m_hit_material_index = this->get_material_index();
            }
        }
    }

    if(trimesh_hr.m_dist < std::numeric_limits< Scalar >::max()){
        std::cout << "Ray hit to TriMesh." << std::endl;
        return true;
    }
    return false;
}

//----------------------------------------------------------------------
} // namespace ifgi
