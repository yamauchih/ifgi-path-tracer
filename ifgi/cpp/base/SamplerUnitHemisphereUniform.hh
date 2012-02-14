//----------------------------------------------------------------------
// ifgi c++ implementation: SamplerUnitHemisphereUniform.cpp
// Copyright (C) 2010-2012 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief Sampler: unit hemi sphere uniform sampling
#ifndef IFGI_PATH_TRACER_IFGI_CPP_BASE_SAMPLERUNITHEMISPHEREUNIFORM_HH
#define IFGI_PATH_TRACER_IFGI_CPP_BASE_SAMPLERUNITHEMISPHEREUNIFORM_HH

#include "Vector.hh"
#include "SamplerUnitDiskUniform.hh"

namespace ifgi
{

/// Generate uniform sampling on a hemisphere.
/// Using UnitDiskUniformSampler.
class SamplerUnitHemisphereUniform
{
public:
    /// constructor
    SamplerUnitHemisphereUniform()
        :
        m_udus()
    {
        // empty
    }

    /// destructor
    virtual ~SamplerUnitHemisphereUniform()
    {
        // empty
    }

    /// get sample point on a unit hemisphere
    /// \return (x,y,z)
    Scalar_3 get_sample()
    {
        // p = [-1,1]x[-1,1]
        Scalar_2 const p = m_udus.get_sample();

        Scalar const x = p[0];
        Scalar const y = p[1];
        Scalar const z = sqrtf(std::max(0.0f, 1 - x * x - y * y));
        Scalar_3 const v(x, y, z);
        // v should be a normalized vector. see in the test.
        // r = ifgimath.normalize_vec(v);

        return v;
    }

private:
    /// unit disk uniform sampler
    SamplerUnitDiskUniform m_udus;

private:
    /// copy constructor, never used.
    SamplerUnitHemisphereUniform(SamplerUnitHemisphereUniform const & rhs);
    /// operator=, never used.
    SamplerUnitHemisphereUniform const & operator=(
      SamplerUnitHemisphereUniform const & rhs);
};

} // namespace ifgi
#endif // #ifndef IFGI_PATH_TRACER_IFGI_CPP_BASE_SAMPLERUNITHEMISPHEREUNIFORM_HH
