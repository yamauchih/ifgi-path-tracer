//----------------------------------------------------------------------
// ifgi c++ implementation: SamplerUnitHemisphereUniform.cpp
// Copyright (C) 2010-2012 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief SamplerUnitHemisphereUniform.cpp
#ifndef IFGI_PATH_TRACER_IFGI_CPP_BASE_SAMPLERUNITHEMISPHEREUNIFORM_CPP
#define IFGI_PATH_TRACER_IFGI_CPP_BASE_SAMPLERUNITHEMISPHEREUNIFORM_CPP
namespace ifgi
{

/// Generate uniform sampling on a hemisphere.
/// Using UnitDiskUniformSampler.
class UnitHemisphereUniformSampler
{
public:
    /// constructor
    UnitHemisphereUniformSampler(){
        m_udus = UnitDiskUniformSampler();
    }

    /// destructor
    virtual ~UnitHemisphereUniformSampler();

    /// get sample point on a unit hemisphere
    /// \return (x,y,z)
    Float32_3 get_sample()
    {
        // p = [-1,1]x[-1,1]
        p = m_udus.get_sample();

        x = p[0]
        y = p[1]
        z = math.sqrt(numpy.max([0, 1 - x * x - y * y]));
        v = numpy.array([x, y, z]);
        // v should be a normalized vector. see in the test.
        // r = ifgimath.normalize_vec(v);

        return v;
    }

private:
  /// copy constructor, never used.
  UnitHemisphereUniformSampler(UnitHemisphereUniformSampler const & rhs);
  /// operator=, never used.
  UnitHemisphereUniformSampler const & operator=(UnitHemisphereUniformSampler const & rhs);
};

} // namespace ifgi
#endif // #ifndef IFGI_PATH_TRACER_IFGI_CPP_BASE_SAMPLERUNITHEMISPHEREUNIFORM_CPP
