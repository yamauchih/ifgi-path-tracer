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
#include "RNGBoostMt19937.hh"

#include <gtest/gtest.h>

using namespace ifgi;

/// test one pseudo-random number generator
/// \param[in] p_rng pseudo-random number generator
void test_one_rng(IRNG * p_rng)
{
    ifgi::Float64 sum = 0.0;
    p_rng->set_state(0);
    const int ONEMEGA = 1024 * 1024;
    const int thread_count = 8;
    const int inner_loop_count = ONEMEGA * 128;

    ifgi::StopWatch sw;
    sw.run();
    {
        // #pragma omp parallel for reduction (+: sum)
        // #pragma omp parallel for num_threads(1)
        // #pragma omp parallel for num_threads(1)
        // #pragma omp parallel for schedule(static, 128)
        // #pragma omp parallel for reduction (+: sum) num_threads(8) schedule(static, 128)
        // #pragma omp parallel for num_threads(8)
        // #pragma omp parallel for reduction (+: sum) num_threads(8)
        for(int i = 0; i < thread_count; ++i){
            IRNG * p_local_rng = p_rng->clone();
            p_local_rng->set_state(static_cast< Uint32 >(i)); // loop local seed
            ifgi::Float64 subsum = 0.0;

            for(int j = 0; j < inner_loop_count; ++j){
                ifgi::Float32 const rval = p_local_rng->rand_float32();
                // std::cout << rval << std::endl;
                subsum += rval;
            }

            sum += subsum;
            delete p_local_rng;
            // std::cout << i << std::endl;
        }
    }
    sw.stop();

    ifgi::Float64 const gen_count_f =
        static_cast< ifgi::Float64 >(thread_count * inner_loop_count);
    std::cout << "ave (near 0.5) = " << (sum / gen_count_f)
              << ", sec = " << sw.get_accumulated_time()
              << " by " << p_rng->get_classname() << std::endl;
}

/// Tests pseudo-random number generator
/// TEST(test_case_name, test_name)
TEST(RNG, RNGLinearCongANSIC)
{
    // int const num_gen = 64;
    // int const num_gen = 1024; // for parallel test
    ifgi::RNGdrand48 rng_drand48;
    test_one_rng(&rng_drand48);

    ifgi::RNGLinearCongANSIC rng_lc_ansi;
    test_one_rng(&rng_lc_ansi);

    ifgi::RNGBoostMt19937 rng_boost_mt;
    test_one_rng(&rng_boost_mt);
}

int main(int argc, char **argv)
{
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}

#endif // #ifndef DOXYGEN_SKIP

#if 0
RNGdrand48
generate only
sec/1 = (/ (+ 13.3975 13.4007 13.3978) 3.0) 13.40
sec/8 = (/ (+ 19.6363 19.6363 19.9412) 3.0) 19.74  (/ 13.40 19.74) 0.68x

reduction sum
sec/1 = (/ (+ 10.8703 10.8703 10.908 ) 3.0) 10.88  (/ 10.88 19.83) 0.55x
sec/8 = (/ (+ 19.9776 19.8513 19.6677 ) 3.0) 19.83


RNGLinearCongANSIC
generate only
sec/1 = (/ (+ 6.86185 6.88404 6.84343) 3.0) 6.863
sec/8 = (/ (+ 4.96344 4.96344 4.34758) 3.0) 4.76  (/ 6.83 4.76) 1.43x

reduction sum
sec/1 = (/ (+ 7.33411 7.33411 7.38451) 3.0) 7.35
sec/8 = (/ (+ 4.49677 3.36367 3.47537) 3.0) 3.78   (/ 7.35 3.78) 1.94x


RNGBoostMt19937
generate only
sec/1 = (/ (+ 6.66189 6.66942 6.67134) 3.0) 6.67
sec/8 = (/ (+ 2.90426 2.90426 2.92496) 3.0) 2.91 (/ 6.67 2.91) 2.29x

reduction sum
sec/1 = (/ (+ 7.64572 7.64572 7.77004) 3.0) 7.69
sec/8 = (/ (+ 2.58749 2.89932 2.97508) 3.0) 2.82 (/ 7.69 2.82) 2.73x

#endif







