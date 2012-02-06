//----------------------------------------------------------------------
// ifgi c++ implementation: HitRecord.hh
// Copyright (C) 2010-2012 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief a hit record

#include "HitRecord.hh"

#include <sstream>

namespace ifgi
{
//----------------------------------------------------------------------
// get string representation
std::string HitRecord::to_string() const
{
    std::stringstream sstr;
    sstr << "HitRecord: dist: " << m_dist
         << ", pos: "           << m_intersect_pos
         << ", basis: "         << m_hit_onb.to_string()
         << ", matidx: "        << m_hit_material_index;
    return sstr.str();
}

//----------------------------------------------------------------------
} // namespace ifgi

