//----------------------------------------------------------------------
// ifgi c++ implementation: Date.hh
// Copyright (C) 2010-2012 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief pseudo-random generator unit test
#ifndef DOXYGEN_SKIP

#include "StopWatch.hh"
#include "IRNG.hh"
#include "RNGdrand48.hh"
#include "RNGLinearCongANSIC.hh"

#include <gtest/gtest.h>

using namespace ifgi;

/// test one pseudo-random number generator
/// \param[in] p_rng pseudo-random number generator
/// \param[in] num_gen number of sample generation
void test_one_rng(IRNG * p_rng, int num_gen)
{
    ifgi::Float64 sum = 0.0;
    p_rng->set_state(0);

    ifgi::StopWatch sw;
    sw.run();
    {
// #pragma omp parallel for
        for(int i = 0; i < num_gen; ++i){
            ifgi::Float32 const rval = p_rng->rand_float32();
            // std::cout << rval << std::endl;
            sum += rval;
        }
    }
    sw.stop();

    ifgi::Float64 const gen_count_f = static_cast< ifgi::Float64 >(num_gen);
    std::cout << "ave (near 0.5) = " << (sum / gen_count_f)
        // << ", gen/sec = " << (gen_count_f / sw.get_accumulated_time())
              << ", sec = " << sw.get_accumulated_time()
              << " by " << p_rng->get_classname() << std::endl;
}

/// Tests pseudo-random number generator
/// TEST(test_case_name, test_name)
TEST(RNG, RNGLinearCongANSIC)
{
    int const num_gen = 1024 * 1024 * 64;
    ifgi::RNGdrand48 rng_drand48;
    test_one_rng(&rng_drand48, num_gen);
    // core 1: sec = 1.21457 by RNGdrand48
    // core 2: sec = 2.18083 by RNGdrand48 (/ 2.18083 1.21457) 1.8x

    ifgi::RNGLinearCongANSIC rng_lc_ansi;
    test_one_rng(&rng_lc_ansi, num_gen);
    // core 1: sec = 0.725752 by RNGLinearCongANSIC
    // core 2: sec = 1.47866  by RNGLinearCongANSIC (/ 1.47866 0.725752) 2.03x

}

int main(int argc, char **argv)
{
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}

#endif // #ifndef DOXYGEN_SKIP
