//----------------------------------------------------------------------
// ifgi c++ implementation: OrthonomalBasis.hh
// Copyright (C) 2010-2012 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief OrthonomalBasis
//
// Ref. Realistic Ray Tracing by Peter Shirley
//

#include "OrthonomalBasis.hh"

namespace ifgi
{
// standard basis 0 definition
// We can not do this in the class for non POD, we can only declare
// the static const member. 

/// standard basis 0
Scalar_3 const OrthonomalBasis::Vec3_N(1.0, 0.0, 0.0);
/// standard basis 1
Scalar_3 const OrthonomalBasis::Vec3_M(0.0, 1.0, 0.0);

} // namespace ifgi

