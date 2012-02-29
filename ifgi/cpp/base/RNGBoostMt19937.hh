//----------------------------------------------------------------------
// ifgi c++ implementation
// Copyright (C) 2010-2012 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief boost mersenne twister pseudo-random number generator

#ifndef IFGI_CPP_BASE_RNGBOOSTMT19937_HH
#define IFGI_CPP_BASE_RNGBOOSTMT19937_HH

#include "IRNG.hh"

#include <stdlib.h>
#include <boost/random.hpp>
#include <boost/random/uniform_01.hpp>

namespace ifgi {

/// pseudo-random number generator implementation: mersenne twister, boost
///
/// In Boost 1.46, boost/random/mersenne_twister.hpp, the state is in
/// the member UIntType x[2*n]; and int i; Therefore, I think I can
/// generate these generator for each thread (but seed must be different.)
class RNGBoostMt19937 : public IRNG
{
public:
    /// random number generator type
    typedef boost::mt19937 RandomNumberGeneratorType;

public:
    /// constructor
    RNGBoostMt19937()
        :
        m_rng(),
        m_uniform_01_dist(),
        m_p_gen(0)
    {
        m_p_gen = new boost::variate_generator<
            RandomNumberGeneratorType,
            boost::uniform_01< Float32 > >(m_rng, m_uniform_01_dist);
    }

    /// for cloning constructor
    RNGBoostMt19937(RandomNumberGeneratorType const & rng,
                    boost::uniform_01< Float32 > const & uniform_01_dist)
        :
        m_rng(rng),
        m_uniform_01_dist(uniform_01_dist),
        m_p_gen(0)
    {
        m_p_gen = new boost::variate_generator<
            RandomNumberGeneratorType,
            boost::uniform_01< Float32 > >(m_rng, m_uniform_01_dist);
    }

    /// destructor
    virtual ~RNGBoostMt19937()
    {
        assert(m_p_gen != 0);
        delete m_p_gen;
        // std::cout << "~RNGBoostMt19937()" << std::endl;
    }

    /// get class name. interface method.
    /// \return class name
    virtual std::string get_classname() const { return "RNGBoostMt19937"; }

    /// set state (seed). maybe some of the generator needs more state
    /// information.
    ///
    /// \param[in] state_seed seed for random number generator
    virtual void set_state(Uint32 state_seed)
    {
        m_rng.seed(state_seed);
    }

    /// get current state (seed)
    /// \return current state (this can be used as a seed.)
    virtual Uint32 get_state() const
    {
        // can not use this
        abort();
        return 0;
    }

    /// get pseudo-random floating number ranged in [0, 1)
    /// \return float pseudo-random number ranged in [0, 1)
    virtual Float32 rand_float32()
    {
        return (*m_p_gen)();
    }

    /// get pseudo-random Uint32 number ranged in [0, rand_max_uint32()]
    /// \return Uint32 pseudo-random number ranged in [0, rand_max_uint32()]
    virtual Uint32 rand_uint32()
    {
        // not use this method.
        abort();
        return 0;
    }

    /// get max Uint32 pseudo-random number
    /// \return max Uint32  pseudo-random number
    virtual Uint32  rand_max_uint32() const
    {
        // not used this method
        abort();
        return RAND_MAX;
    }

    /// clone method. To enable IRNG * can clone the instance.
    ///
    /// \return cloned object.
    virtual IRNG * clone() const
    {
        RNGBoostMt19937 * p_cloned =
            new RNGBoostMt19937(this->m_rng, this->m_uniform_01_dist);

        return p_cloned;
    }


private:
    /// pseudo-random number generator
    RandomNumberGeneratorType m_rng;
    /// distribution [0,1)
    boost::uniform_01< Float32 > m_uniform_01_dist;
    ///
    boost::variate_generator< RandomNumberGeneratorType, boost::uniform_01< Float32 > > *
    m_p_gen;

    /// padding more than 4k
    char * m_p_pad[4096];

private:
  /// copy constructor, never used.
  RNGBoostMt19937(const RNGBoostMt19937& _rhs);
  /// operator=, never used.
  const RNGBoostMt19937& operator=(const RNGBoostMt19937& _rhs);
};


} // namespace ifgi
#endif // #ifndef IFGI_CPP_BASE_RNGBOOSTMT19937_HH
