//----------------------------------------------------------------------
// ifgi c++ implementation: SamplerUnitDiskUniform.cpp
// Copyright (C) 2010-2012 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief SamplerUnitDiskUniform.cpp
#ifndef IFGI_PATH_TRACER_IFGI_CPP_BASE_SAMPLERUNITDISKUNIFORM_CPP
#define IFGI_PATH_TRACER_IFGI_CPP_BASE_SAMPLERUNITDISKUNIFORM_CPP
namespace ifgi
{

/// Generate uniform sampling on a unit disk.  Uniform respect to area.
class UnitDiskUniformSampler
{
public:
    /// constructor
    UnitDiskUniformSampler()
    {
        // empty
    }

    /// destructor
    virtual ~UnitDiskUniformSampler();

    /// get sample point on an unit disk
    ///
    /// \return (x,y)
    Float32_2 get_sample()
    {
        u1 = random.random();
        u2 = random.random();
        r  = math.sqrt(u1);
        t  = 2.0 * M_PI * u2
        x  = r * cos(t);
        y  = r * sin(t);

        return Float32_2(x, y);
    }

private:
  /// copy constructor, never used.
  UnitDiskUniformSampler(UnitDiskUniformSampler const & rhs);
  /// operator=, never used.
  UnitDiskUniformSampler const & operator=(UnitDiskUniformSampler const & rhs);
};

} // namespace ifgi
#endif // #ifndef IFGI_PATH_TRACER_IFGI_CPP_BASE_SAMPLERUNITDISKUNIFORM_CPP
