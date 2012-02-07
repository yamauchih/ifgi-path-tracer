//----------------------------------------------------------------------
// ifgi c++ implementation: Bbox.hh
// Copyright (C) 2010-2012 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief axis aligned bounding box

#include "BBox.hh"

#include <cassert>
#include <limits>
#include <sstream>

namespace ifgi
{
//----------------------------------------------------------------------
// default constructor
BBox32::BBox32()
    :
    IPrimitive()
{
    this->invalidate();
}

//----------------------------------------------------------------------
//  get class name (public).
std::string BBox32::get_classname() const
{
    return std::string("BBox32");
}

//----------------------------------------------------------------------
// get the bounding box
BBox32 const & BBox32::get_bbox() const
{
    return *this;
}

//----------------------------------------------------------------------
// can bbox primitive intersect with a ray?
bool BBox32::can_intersect() const
{
    return true;
}

//----------------------------------------------------------------------
// compute ray intersection. interface method.
bool BBox32::ray_intersect(Ray const & ray, HitRecord & hr) const
{
    std::cout << "NIN BBox32::ray_intersect" << std::endl;
    assert(false);
    return false;
}

//----------------------------------------------------------------------
// invalidate this bbox.
void BBox32::invalidate()
{
    m_min = Scalar_3(std::numeric_limits< Scalar >::max(),
                     std::numeric_limits< Scalar >::max(),
                     std::numeric_limits< Scalar >::max());
    m_max = Scalar_3(-std::numeric_limits< Scalar >::max(),
                     -std::numeric_limits< Scalar >::max(),
                     -std::numeric_limits< Scalar >::max());
}

//----------------------------------------------------------------------
// get rank of this bbox.
Sint32 BBox32::get_rank() const
{
    Scalar_3 const diff = m_max - m_min;
    Sint32 rank_count = 0;
    for(Sint32 i = 0; i < 3; ++i){
        if(diff[i] > 0.0f){
            rank_count += 1;
        }
    }
    return rank_count;
}

//----------------------------------------------------------------------
// has this bbox volume?.
bool BBox32::has_volume() const
{
    // for all max > min.
    Scalar_3 const diff = m_max - m_min;
    for(Sint32 i = 0; i < 3; ++i){
        if(diff[i] <= 0.0f){
            return false;
        }
    }
    return true;
}

//----------------------------------------------------------------------
// insert a point and grow the bbox. (public).
void BBox32::insert_point(Scalar_3 const & newpos)
{
    for(Sint32 i = 0; i < 3; ++i){
        if(m_min[i] > newpos[i]){
            m_min[i] = newpos[i];
        }
        // here else if(m_max[i] < newpos[i]) doesn"t work, when just
        // after invalidate() call when [max, max, max]-[-max, -max,
        // -max], insert [0,0,0], both min, max must be [0,0,0], if I
        // use else if, only min is updated. Therefore this must be
        // if:
        if (m_max[i] < newpos[i]){
            m_max[i] = newpos[i];
        }
        // print "DEBUG: " + str() + ", p" + str(_newpos);
    }
}

//----------------------------------------------------------------------
// insert a bbox and grow the bbox.
void BBox32::insert_bbox(BBox32 const & bbox)
{
    assert(bbox.get_rank() > 0); // handle line/plane case.
    this->insert_point(bbox.get_min());
    this->insert_point(bbox.get_max());
}

//----------------------------------------------------------------------
// get minimal point (public).
Scalar_3 const & BBox32::get_min() const
{
    return m_min;
}

//----------------------------------------------------------------------
// get maximal point (public).
Scalar_3 const & BBox32::get_max() const
{
    return m_max;
}

//----------------------------------------------------------------------
// equal?
bool BBox32::equal(BBox32 const & other) const
{
    if(this == &other){    // if the same object, true
        return true;
    }
    else if((m_min == other.get_min()) && (m_max == other.get_max())){
        return true;
    }
    return false;
}

//----------------------------------------------------------------------
// string representation (public).
std::string BBox32::to_string() const
{
    std::stringstream sstr;
    sstr << "BBox32[" << m_min << "]-[" << m_max << "]";
    return sstr.str();
}

//----------------------------------------------------------------------
} // namespace ifgi

