//----------------------------------------------------------------------
// ifgi c++ implementation
// Copyright (C) 2010-2012 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief drand48/lrand48 pseudo-random number generator.

#ifndef IFGI_CPP_BASE_RNGDRAND48_HH
#define IFGI_CPP_BASE_RNGDRAND48_HH

#include "IRNG.hh"
#include "Exception.hh"

#include <stdlib.h>

namespace ifgi {

/// pseudo-random number generator implementation: drand48/lrand48
///
/// This is for a comparison. drand48/lrand48 lock the
/// state. Therefore, this doesn't scale with multithreading.
///
class RNGdrand48 : public IRNG
{
public:
    /// constructor
    RNGdrand48()
        :
        m_state(0)
    {
        // empty
    }
    /// destructor
    virtual ~RNGdrand48()
    {
        // empty
    }

    /// get class name. interface method.
    /// \return class name
    virtual std::string get_classname() const { return "RNGdrand48"; }

    /// set state (seed). maybe some of the generator needs more state
    /// information.
    ///
    /// \param[in] state_seed seed for random number generator
    virtual void set_state(Uint32 state_seed)
    {
        srand48(state_seed);
    }

    /// get current state (seed)
    /// For RNGdrand48, this method is meanless. Always returns 0.
    /// \return current state (this can be used as a seed.)
    virtual Uint32 get_state() const
    {
        return 0;
    }

    /// get pseudo-random floating number ranged in [0, 1)
    /// \return float pseudo-random number ranged in [0, 1)
    virtual Float32 rand_float32()
    {
        return static_cast< Float32 >(drand48());
    }

    /// get pseudo-random Uint32 number ranged in [0, rand_max_uint32()]
    /// \return Uint32 pseudo-random number ranged in [0, rand_max_uint32()]
    virtual Uint32 rand_uint32()
    {
        return lrand48();
    }

    /// get max Uint32 pseudo-random number
    /// \return max Uint32  pseudo-random number
    virtual Uint32  rand_max_uint32() const { return RAND_MAX; }


private:
    /// current state
    Uint32 m_state;

private:
  /// copy constructor, never used.
  RNGdrand48(const RNGdrand48& _rhs);
  /// operator=, never used.
  const RNGdrand48& operator=(const RNGdrand48& _rhs);
};


} // namespace ifgi
#endif // #ifndef IFGI_CPP_BASE_RNGDRAND48_HH
