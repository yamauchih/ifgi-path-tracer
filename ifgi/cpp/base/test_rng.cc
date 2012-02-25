//----------------------------------------------------------------------
// ifgi c++ implementation: Date.hh
// Copyright (C) 2010-2012 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief pseudo-random generator unit test
#ifndef DOXYGEN_SKIP

#include "StopWatch.hh"
#include "IRNG.hh"
#include "RNGLinearCongANSIC.hh"

#include <gtest/gtest.h>

/// Tests pseudo-random number generator
/// TEST(test_case_name, test_name)
TEST(RNG, RNGLinearCongANSIC)
{
    ifgi::IRNG * p_rng = new ifgi::RNGLinearCongANSIC;
    p_rng->set_state(0);

    ifgi::Float32 sum = 0.0;
    int const max_loop = 1024 * 1024 * 16;

    ifgi::StopWatch sw;
    sw.run();
    for(int i = 0; i < max_loop; ++i){
        ifgi::Float32 const rval = p_rng->rand_float32();
        // std::cout << rval << std::endl;
        sum += rval;
    }
    sw.stop();

    ifgi::Float64 const gen_count_f = static_cast< ifgi::Float64 >(max_loop);
    std::cout << "ave (near 0.5) = " << (sum / gen_count_f)
              << ", gen/sec = " << (gen_count_f / sw.get_accumulated_time())
              << std::endl;
}

int main(int argc, char **argv)
{
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}

#endif // #ifndef DOXYGEN_SKIP
