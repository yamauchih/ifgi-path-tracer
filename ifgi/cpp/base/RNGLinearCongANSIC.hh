//----------------------------------------------------------------------
// ifgi c++ implementation
// Copyright (C) 2010-2012 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief linear congruential pseudo-random number generator, ANSI C

#ifndef IFGI_CPP_BASE_RNGLINEARCONGANSIC_HH
#define IFGI_CPP_BASE_RNGLINEARCONGANSIC_HH

#include "IRNG.hh"

#include <stdlib.h>

namespace ifgi {

/// pseudo-random number generator implementation: Linear congruence ANSI C
///
/// Implementation assumes these are used thread locally, not over
/// multiple threads (thread non-safe)
class RNGLinearCongANSIC : public IRNG
{
public:
    /// constructor
    RNGLinearCongANSIC()
        :
        m_state(0)
    {
        // empty
    }
    /// destructor
    virtual ~RNGLinearCongANSIC()
    {
        // empty
        // std::cout << "~RNGLinearCongANSIC()" << std::endl;
    }

    /// get class name. interface method.
    /// \return class name
    virtual std::string get_classname() const { return "RNGLinearCongANSIC"; }

    /// set state (seed). maybe some of the generator needs more state
    /// information.
    ///
    /// \param[in] state_seed seed for random number generator
    virtual void set_state(Uint32 state_seed)
    {
        m_state = state_seed;
    }

    /// get current state (seed)
    /// \return current state (this can be used as a seed.)
    virtual Uint32 get_state() const
    {
        return m_state;
    }

    /// get pseudo-random floating number ranged in [0, 1)
    /// \return float pseudo-random number ranged in [0, 1)
    virtual Float32 rand_float32()
    {
        Float32 const rndf    = static_cast< Float32 >(this->rand_uint32());
        Float32 const maxrndf =
            static_cast< Float32 >((static_cast< Uint64 >(this->rand_max_uint32()) + 1ull));

        return rndf / maxrndf;
    }

    /// get pseudo-random Uint32 number ranged in [0, rand_max_uint32()]
    /// \return Uint32 pseudo-random number ranged in [0, rand_max_uint32()]
    virtual Uint32 rand_uint32()
    {
        // (aaX+cc)%mm
        Uint64 const aa = 1103515245llu;
        Uint64 const cc = 12345llu;
        Uint64 const mm = RAND_MAX;

        m_state = static_cast< Uint32 >((aa * static_cast< Uint64 >(m_state)) + cc) % mm;
        return m_state;
    }

    /// get max Uint32 pseudo-random number
    /// \return max Uint32  pseudo-random number
    virtual Uint32  rand_max_uint32() const { return RAND_MAX; }


    /// clone method. To enable IRNG * can clone the instance.
    ///
    /// \return cloned object. This class can not guarantee the same
    /// state.
    virtual IRNG * clone() const
    {
        RNGLinearCongANSIC * p_cloned   = new RNGLinearCongANSIC;
        p_cloned->m_state = this->m_state;

        return p_cloned;
    }


private:
    /// current state
    Uint32 m_state;

private:
  /// copy constructor, never used.
  RNGLinearCongANSIC(const RNGLinearCongANSIC& _rhs);
  /// operator=, never used.
  const RNGLinearCongANSIC& operator=(const RNGLinearCongANSIC& _rhs);
};


// glibc
// int rand_r (unsigned int *seed)
// {
//     unsigned int next = *seed;
//     int result;

//     next *= 1103515245;
//     next += 12345;
//     result = (unsigned int) (next / 65536) % 2048;

//     next *= 1103515245;
//     next += 12345;
//     result <<= 10;
//     result ^= (unsigned int) (next / 65536) % 1024;

//     next *= 1103515245;
//     next += 12345;
//     result <<= 10;
//     result ^= (unsigned int) (next / 65536) % 1024;

//     *seed = next;

//     return result;
// }

} // namespace ifgi
#endif // #ifndef IFGI_CPP_BASE_RNGLINEARCONGANSIC_HH
