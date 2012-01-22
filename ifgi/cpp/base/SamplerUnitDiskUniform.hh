//----------------------------------------------------------------------
// ifgi c++ implementation: SamplerUnitDiskUniform.hh
// Copyright (C) 2010-2012 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief Sampler: uniformly sample on a unit disk
#ifndef IFGI_PATH_TRACER_IFGI_CPP_BASE_SAMPLERUNITDISKUNIFORM_CPP
#define IFGI_PATH_TRACER_IFGI_CPP_BASE_SAMPLERUNITDISKUNIFORM_CPP

#include "Vector.hh"

namespace ifgi
{

/// Generate uniform sampling on a unit disk.  Uniformality respects
/// to area.
class SamplerUnitDiskUniform
{
public:
    /// constructor
    SamplerUnitDiskUniform()
    {
        // empty
    }

    /// destructor
    virtual ~SamplerUnitDiskUniform()
    {
        // empty
    }

    /// get sample point on an unit disk
    ///
    /// \return (x,y)
    Float32_2 get_sample()
    {
        double u1 = drand48();
        double u2 = drand48();
        double r  = sqrt(u1);
        double t  = 2.0 * M_PI * u2;
        double x  = r * cos(t);
        double y  = r * sin(t);

        return Float32_2(static_cast< float >(x), static_cast< float >(y));
    }

private:
  /// copy constructor, never used.
  SamplerUnitDiskUniform(SamplerUnitDiskUniform const & rhs);
  /// operator=, never used.
  SamplerUnitDiskUniform const & operator=(SamplerUnitDiskUniform const & rhs);
};

} // namespace ifgi
#endif // #ifndef IFGI_PATH_TRACER_IFGI_CPP_BASE_SAMPLERUNITDISKUNIFORM_CPP
