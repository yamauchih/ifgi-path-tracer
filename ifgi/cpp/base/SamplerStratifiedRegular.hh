//----------------------------------------------------------------------
// ifgi c++ implementation: SamplerStratifiedRegular.cpp
// Copyright (C) 2010-2012 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief samplers: stratified sampler, QMC (maybe), ...
#ifndef IFGI_PATH_TRACER_IFGI_CPP_BASE_SAMPLERSTRATIFIEDREGULAR_HH
#define IFGI_PATH_TRACER_IFGI_CPP_BASE_SAMPLERSTRATIFIEDREGULAR_HH

#include "ILog.hh"
#include "Vector.hh"
#include "Array3D.hh"

namespace ifgi
{

/// a simple stratified regular sampler.
class SamplerStratifiedRegular
{
public:
    /// default constructor
    SamplerStratifiedRegular()
        :
        m_xstart(0),
        m_xend(-1),
        m_ystart(0),
        m_yend(-1),
        m_xsize(0),
        m_ysize(0),
        m_sample_loc()
    {
        // empty
    }

    /// destructor
    ~SamplerStratifiedRegular()
    {
        // empty
    }

    /// compute samples. Allocate memory.
    ///
    /// we can access pixel index [_xstart, xend], [_ystart, yend]
    ///
    /// \param[in] xstart start of pixel x
    /// \param[in] xend   end   of pixel x (inclusive);
    /// \param[in] ystart start of pixel y
    /// \param[in] yend   end   of pixel y (inclusive);
    void compute_sample(Sint32 xstart, Sint32 xend, Sint32 ystart, Sint32 yend)
    {
        assert(xstart <= xend);
        assert(ystart <= yend);

        m_xstart = xstart;
        m_xend   = xend;
        m_ystart = ystart;
        m_yend   = yend;
        m_xsize  = m_xend - m_xstart + 1;
        m_ysize  = m_yend - m_ystart + 1;
        Sint32_3 const new_dim(m_xsize, m_ysize, 2);
        if(m_sample_loc.getDimension() != new_dim){
            // resize the buffer
            std::stringstream sstr;
            sstr << "resize the sample location from " << m_sample_loc.getDimension()
                 << " to " << new_dim;
            ILog::instance()->debug(sstr.str());
            m_sample_loc.resizeBuffer(new_dim);
        }
        for(Sint32 y = 0; y < m_ysize; ++y){
            for(Sint32 x = 0; x < m_xsize; ++x){
                m_sample_loc.set(x, y, 0, (static_cast< Float32 >(x) + 0.5f)); // x
                m_sample_loc.set(x, y, 1, (static_cast< Float32 >(y) + 0.5f)); // y
            }
        }
    }

    /// get the sample location x from the pixel index.
    Scalar get_sample(Sint32 xidx, Sint32 yidx, Sint32 depth) const {
        return m_sample_loc.get(xidx, yidx, depth);
    }

private:
    /// stratified regular sample xstart
    Sint32 m_xstart;
    /// stratified regular sample xend
    Sint32 m_xend;
    /// stratified regular sample ystart
    Sint32 m_ystart;
    /// stratified regular sample yend
    Sint32 m_yend;
    /// stratified regular sample x size
    Sint32 m_xsize;
    /// stratified regular sample y size
    Sint32 m_ysize;
    /// sample x value (pos_x, pos_y, depth = 2 for x and y)
    Array3D_Float32 m_sample_loc;

private:
  /// copy constructor, never used.
  SamplerStratifiedRegular(SamplerStratifiedRegular const & rhs);
  /// operator=, never used.
  SamplerStratifiedRegular const & operator=(SamplerStratifiedRegular const & rhs);
};


} // namespace ifgi
#endif // #ifndef IFGI_PATH_TRACER_IFGI_CPP_BASE_SAMPLERSTRATIFIEDREGULAR_HH
