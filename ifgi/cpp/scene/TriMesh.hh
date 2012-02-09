//----------------------------------------------------------------------
// ifgi c++ implementation: TriMesh.hh
// Copyright (C) 2010-2012 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief simple triangle mesh primitive
#ifndef IFGI_PATH_TRACER_IFGI_CPP_SCENE_TRIMESH_HH
#define IFGI_PATH_TRACER_IFGI_CPP_SCENE_TRIMESH_HH

#include <cassert>
#include <sstream>
#include <vector>

#include "IPrimitive.hh"
#include "BBox.hh"

namespace ifgi
{
//----------------------------------------------------------------------

// forward declarations
class Ray;
class HitRecord;

//----------------------------------------------------------------------

/// TriMesh: simple triangle mesh primitive
class TriMesh : public IPrimitive
{
public:
    /// default constructor
    TriMesh();
    /// destructor
    virtual ~TriMesh();

    /// get class name. interface method.
    // \return class name
    virtual std::string get_classname() const;

    /// get the bounding box. interface method.
    /// \return bounding box of this primitive.
    virtual BBoxScalar const & get_bbox() const;

    /// can TriMesh primitive intersect with a ray? no.
    /// This object needs refinement.
    virtual bool can_intersect() const;

    /// set geometry data
    /// \param[in]  vlist     vertex list (len(_vlist) must be > 0);
    /// \param[in]  fidxlist  face index list
    /// \param[in]  tclist    texture coordinate list
    /// \param[in]  tcidxlist texture coordinate index list
    /// \param[in]  nlist     normal list
    /// \param[in]  nidxlist  normal index list
    void set_data(std::vector< Scalar_3 > const & vlist,
                  std::vector< Sint32_3 > const & fidxlist,
                  std::vector< Scalar_3 > const & tclist,
                  std::vector< Sint32_3 > const & tcidxlist,
                  std::vector< Scalar_3 > const & nlist,
                  std::vector< Sint32_3 > const & nidxlist);

    /// set global material index.
    ///
    /// \param[in] mat_idx global material index.
    ///
    /// FIXME: shall I push this information to each triangles?
    void set_material_index(Sint32 mat_idx)
    {
        m_material_index = mat_idx;
    }

    /// get global material index.
    ///
    /// \return global material index.
    Sint32 get_material_index() const
    {
        return m_material_index;
    }

    /// get summary information
    ///
    /// \return summary information
    std::string get_info_summary() const;

    /// update bounding box according to current vertex list.
    void update_bbox();

    /// is this valid object?
    /// At least !vertex_vec.empty().
    /// \return true when valid
    bool is_valid() const;

    /// compute a ray and a trimesh intersection.
    /// \param[in]  ray a ray
    /// \param[out] a HitRecord. Only valid when return true
    /// \return true when hit
    /// NIN: bounding box test?
    bool ray_intersect(Ray const & ray, HitRecord & hr) const;

private:
    /// vertex position vector
    std::vector< Scalar_3 > m_vertex_vec;
    /// triangle face index vector
    std::vector< Sint32_3 > m_face_idx_vec;
    /// texture coordinate vector.
    std::vector< Scalar_3 > m_texcoord_vec;
    /// texture coordinate index vector
    std::vector< Sint32_3 > m_texcoord_idx_vec;
    /// normal vector
    std::vector< Scalar_3 > m_normal_vec;
    /// normal index vector
    std::vector< Sint32_3 > m_normal_idx_vec;
    /// bounding box of this triangle mesh
    BBoxScalar m_bbox;
    /// global material index of this geometry (valid after
    /// preprocessing);
    Sint32 m_material_index;
};

} // namespace ifgi
#endif // #ifndef IFGI_PATH_TRACER_IFGI_CPP_SCENE_TRIMESH_HH
