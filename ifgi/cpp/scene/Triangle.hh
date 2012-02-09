//----------------------------------------------------------------------
// ifgi c++ implementation: Triangle.hh
// Copyright (C) 2010-2012 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief primitive triangle
#ifndef IFGI_PATH_TRACER_IFGI_CPP_SCENE_TRIANGLE_HH
#define IFGI_PATH_TRACER_IFGI_CPP_SCENE_TRIANGLE_HH

#include "IPrimitive.hh"
#include "BBox.hh"

namespace ifgi
{
//----------------------------------------------------------------------
// forward declarations
class Ray;
class HitRecord;

//----------------------------------------------------------------------
/// A triangle primitive
class Triangle : public IPrimitive
{
public:
    /// default constructor.
    Triangle();
    /// destructor.
    virtual ~Triangle();

    /// get class name. interface method.
    /// \return class name
    virtual std::string get_classname() const;

    /// get the bounding box. interface method.
    /// \return bounding box of this primitive.
    virtual BBoxScalar const & get_bbox() const;

    /// can a triangle intersect with a ray? Yes.
    virtual bool can_intersect() const;

    /// compute ray intersection. interface method.
    /// \param[in]  ray a ray
    /// \param[out] a HitRecord. Only valid when return true
    /// \return true when hit
    virtual bool ray_intersect(Ray const & ray, HitRecord & hr) const;

public:
    /// Set triangle vertices.
    /// \param[in] v0 vertex 0
    /// \param[in] v1 vertex 1
    /// \param[in] v2 vertex 2
    void set_vertex(Scalar_3 const & v0,
                    Scalar_3 const & v1,
                    Scalar_3 const & v2);

    /// update bounding box
    void update_bbox();

private:
    /// triangle vertices
    Scalar_3 m_vertex[3];
    /// bounding box of this triangle
    BBoxScalar m_bbox;
};

} // namespace ifgi
#endif // #ifndef IFGI_PATH_TRACER_IFGI_CPP_SCENE_TRIANGLE_HH
