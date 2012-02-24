//----------------------------------------------------------------------
// ifgi c++ implementation
// Copyright (C) 2010-2012 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief pseudo-random number generator interface

#ifndef IFGI_CPP_BASE_IRNG_HH
#define IFGI_CPP_BASE_IRNG_HH

#include "types.hh"

namespace ifgi {

/// pseudo-random number generator interface
///
/// Implementation assumes these are used thread locally, not over
/// multiple threads (thread non-safe)
class IRNG
{
public:
    /// constructor
    IRNG();
    /// destructor
    virtual ~IRNG();

    /// set state (seed). maybe some of the generator needs more state
    /// information.
    ///
    /// \param[in] state_seed seed for random number generator
    virtual void set_state(Uint32 state_seed) = 0;

    /// get current state (seed)
    /// \return current state (this can be used as a seed.)
    virtual Uint32 get_state() const = 0;

    /// get pseudo-random floating number ranged in [0, 1)
    /// \return float pseudo-random number ranged in [0, 1)
    virtual Float32 rand_float32() const = 0;

    /// get pseudo-random Uint32 number ranged in [0, rand_max_uint32()]
    /// \return Uint32 pseudo-random number ranged in [0, rand_max_uint32()]
    virtual Uint32  rand_uint32() const = 0;

    /// get max Uint32 pseudo-random number
    /// \return max Uint32  pseudo-random number
    virtual Uint32  rand_max_uint32() const = 0;

private:
  /// copy constructor, never used.
  IRNG(const IRNG& _rhs);
  /// operator=, never used.
  const IRNG& operator=(const IRNG& _rhs);
};

} // namespace ifgi
#endif // #ifndef IFGI_CPP_BASE_IRNG_HH
