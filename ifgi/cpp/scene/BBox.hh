//----------------------------------------------------------------------
// ifgi c++ implementation: Bbox.hh
// Copyright (C) 2010-2012 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief primitive axis aligned bounding box
#ifndef IFGI_PATH_TRACER_IFGI_CPP_SCENE_BBOX_HH
#define IFGI_PATH_TRACER_IFGI_CPP_SCENE_BBOX_HH

#include <string>
#include <cpp/base/Vector.hh>

#include "IPrimitive.hh"

namespace ifgi
{
// forward declaration
class Ray;
class HiiRecord;

//----------------------------------------------------------------------
/// BBox. axis aligned 3D bounding box. Scalar. FIXME This should be
/// BBoxScalar.
class BBox32 : public IPrimitive
{
public:
    /// default constructor
    BBox32();
    /// destructor
    virtual ~BBox32()
    {
        // empty
    }

    ///  get class name (public).
    /// \return class name
    virtual std::string get_classname() const;

    /// get the bounding box
    /// \return this
    virtual BBox32 const & get_bbox() const;

    /// can bbox primitive intersect with a ray?
    /// \return true
    virtual bool can_intersect() const;

    /// compute ray intersection. interface method.
    /// \param[in]  ray a ray
    /// \param[out] a HitRecord
    /// \return true when hit
    virtual bool ray_intersect(Ray const & ray, HitRecord & hr) const;

public:
    /// invalidate this bbox.
    /// The bbox has no volume after invalidate().
    void invalidate();

    /// get rank of this bbox.
    /// The number of m_max > m_min satisfied axis.
    /// \return True when this bbox has area.
    Sint32 get_rank() const;

    /// has this bbox volume?.
    /// After invalidate(), bbox has no volume.
    /// \return True when this bbox has volume.
    bool has_volume() const;

    /// insert a point and grow the bbox. (public).
    /// \param[in] newpos newly inserted point
    void insert_point(Scalar_3 const & newpos);

    /// insert a bbox and grow the bbox.
    /// \param[in] bbox bounding box to be inserted.
    void insert_bbox(BBox32 const & bbox);

    /// get minimal point (public).
    /// \return minimal point (numpy.array[3]);
    Scalar_3 const & get_min() const
    {
        return m_min;
    }

    /// get maximal point (public).
    /// \return maximal point (numpy.array[3]);
    Scalar_3 const & get_max() const
    {
        return m_max;
    }

    /// equal?
    /// comparison  with other. If exact the same, return True
    /// otherwise False.
    /// \param[in] other other bounding box to compare
    /// \return true when equal
    bool equal(BBox32 const & other) const;

    /// string representation (public).
    /// \return string representation of this object.
    std::string to_string() const;

private:
    /// min point of this bounding box
    Scalar_3 m_min;
    /// max point of this bounding box
    Scalar_3 m_max;
};

} // namespace ifgi
#endif // #ifndef IFGI_PATH_TRACER_IFGI_CPP_SCENE_BBOX_HH
