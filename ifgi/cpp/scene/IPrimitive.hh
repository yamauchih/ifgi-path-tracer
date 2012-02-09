//----------------------------------------------------------------------
// ifgi c++ implementation: IPrimitive.hh
// Copyright (C) 2010-2012 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief scene element primitive interface
#ifndef IFGI_PATH_TRACER_IFGI_CPP_SCENE_IPRIMITIVE_HH
#define IFGI_PATH_TRACER_IFGI_CPP_SCENE_IPRIMITIVE_HH

#include <string>

#include <cpp/base/types.hh>
#include <cpp/base/Vector.hh>

namespace ifgi
{

// forward declarations
class BBoxScalar;
class Ray;
class HitRecord;

//===============================================================================

/// Primitive class. interface for a primitive.
class IPrimitive
{
public:
    /// default constructor
    IPrimitive()
    {
        // empty
    }

    /// get class name. interface method.
    /// \return class name
    virtual std::string get_classname() const = 0;

    /// set primitive associated name.
    /// \return primitive name
    // virtual void set_name(std::string const & name) = 0;

    /// get primitive associated name.
    /// \return primitive name


    /// set primitive's material name.
    /// \param[in] mat_name material name
    // virtual void set_material_name(std::string & mat_name) = 0;

    /// get primitive"s material name.
    /// \return material name
    // virtual std::string get_material_name() const = 0;

    /// set primitive"s material global index.
    /// material index is scene global index for fast material lookup.
    /// \param[in] mat_idx material index (for fast lookup);
    // virtual void set_material_global_index(Sint32 mat_idx) = 0;

    /// get primitive"s material global index.
    /// If -1, no material is indicated.
    /// \return global material index
    // virtual Sint32 get_material_global_index() const = 0;

    /// get the bounding box. interface method.
    /// \return bounding box of this primitive.
    virtual BBoxScalar const & get_bbox() const = 0;

    /// can this primitive intersect with a ray?
    ///
    /// Some of primitives can not directory intersect with a ray. For
    /// example, TriMesh. These primitives need refinement first.
    virtual bool can_intersect() const = 0;

    /// compute ray intersection. interface method.
    /// \param[in]  ray a ray
    /// \param[out] a HitRecord. Only valid when return true
    /// \return true when hit
    virtual bool ray_intersect(Ray const & ray, HitRecord & hr) const = 0;
};

} // namespace ifgi
#endif // #ifndef IFGI_PATH_TRACER_IFGI_CPP_SCENE_IPRIMITIVE_HH
