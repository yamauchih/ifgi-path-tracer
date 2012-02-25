//----------------------------------------------------------------------
// ifgi c++ implementation: Date.hh
// Copyright (C) 2010-2012 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief pseudo-random generator unit test
#ifndef DOXYGEN_SKIP

#include "IRNG.hh"
#include "RNGLinearCongANSIC.hh"

#include <gtest/gtest.h>

/// Tests pseudo-random number generator
/// TEST(test_case_name, test_name)
TEST(RNG, RNGLinearCongANSIC)
{
    IRNG * p_rng = new RNGLinearCongANSIC;
    p_rng->set_state(0);

    Float32 sum = 0.0;
    for(int i = 0; i < 1024 * 1024 * 1024; ++i){
        sum += p_rng->rand_float32();
    }
}

int main(int argc, char **argv)
{
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}

#endif // #ifndef DOXYGEN_SKIP
