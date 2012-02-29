//----------------------------------------------------------------------
// ifgi c++ implementation: Date.hh
// Copyright (C) 2010-2012 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief pseudo-random generator unit test
#ifndef DOXYGEN_SKIP

#include "StopWatch.hh"

#include <cmath>
#include <gtest/gtest.h>

using namespace ifgi;

/// Tests OpenMP scaling
/// TEST(test_case_name, test_name)
TEST(OpenMP, SimpleLoop)
{
    ifgi::Float64 sum = 0.0;

    const int ONEMEGA = 1024 * 1024;
    const int thread_count = 8;
    const int inner_loop_count = ONEMEGA * 64;

    ifgi::StopWatch sw;
    sw.run();
    {
        // #pragma omp parallel for reduction (+: sum)
        // #pragma omp parallel for num_threads(1)
        // #pragma omp parallel for num_threads(1)
        // #pragma omp parallel for schedule(static, 128)
        // #pragma omp parallel for reduction (+: sum) num_threads(8) schedule(static, 128)
        // #pragma omp parallel for num_threads(8)
        // #pragma omp parallel for num_threads(2)
        // #pragma omp parallel for reduction (+: sum) num_threads(8)
        for(int i = 0; i < thread_count; ++i){
            ifgi::Float64 subsum = 0.0;
            for(int j = 0; j < inner_loop_count; ++j){
                Float64 const x = static_cast< Float64 >(j);
                Float64 const rval = sin(x) * cos(x);
                subsum += rval;
            }
            sum += subsum;
        }
    }
    sw.stop();

    std::cout << "sec = " << sw.get_accumulated_time() << ", sum = " << sum << std::endl;
}

int main(int argc, char **argv)
{
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}

#endif // #ifndef DOXYGEN_SKIP

#if 0

sin(x) * cos(x) なら伸びるのに，Linar Congruence ですら伸びない．

sec/8 = 3.74798, sum = 1.98151
sec/1 = 23.3503, sum = 1.98151

(/ 23.35 3.74798) 6.23x

#endif

















