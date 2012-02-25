//----------------------------------------------------------------------
// ifgi c++ implementation: test_Sampler.py
// Copyright (C) 2010-2012 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief Sampler unit test

#include "SamplerStratifiedRegular.hh"
#include "SamplerUnitDiskUniform.hh"
#include "SamplerUnitHemisphereUniform.hh"
#include "Array3D.hh"
#include "LoadSavePPM.hh"
#include "StopWatch.hh"

#include <gtest/gtest.h>

using namespace ifgi;

/// Sampler: UnitDiskUniform
/// TEST(test_case_name, test_name)
TEST(SamplarTest, StratifiedRegular)
{
    SamplerStratifiedRegular srs;

    Sint32 const xstart = 0;
    Sint32 const xend   = 16;
    Sint32 const ystart = 0;
    Sint32 const yend   = 10;

    srs.compute_sample(xstart, xend, ystart, yend);
    for(Sint32 x = xstart; x < (xend + 1); ++x){
        for(Sint32 y = ystart; y < (yend + 1); ++y){
            ASSERT_EQ(srs.get_sample(x, y, 0), (static_cast< Scalar >(x) + 0.5f));
            ASSERT_EQ(srs.get_sample(x, y, 1), (static_cast< Scalar >(y) + 0.5f));
        }
    }
}

/// Sampler: UnitDiskUniform
/// TEST(test_case_name, test_name)
TEST(SamplarTest, UnitDiskUniform)
{
    SamplerUnitDiskUniform udus;

    int const sample_count = 1000;

    /// set up an image
    Color bg_white(1.0f, 1.0f, 1.0f, 1.0f);
    Color fg_red  (1.0f, 0.0f, 0.0f, 1.0f);
    Scalar_2 imgsize(128.0f, 128.0f);
    // img = Image.new("RGB", imgsize, bg_white);
    Array3D_Float32 img(static_cast< int >(imgsize[0]),
                        static_cast< int >(imgsize[1]),
                        4);
    img.clearWithValue(1.0f);

    for(int i = 0; i < sample_count; ++i){
        // p = [-1,1]x[-1,1]
        Scalar_2 const p = udus.get_sample();

        Scalar half_x = 0.5 * (imgsize[0] - 1.0f);
        Scalar half_y = 0.5 * (imgsize[1] - 1.0f);
        Scalar x = half_x * p[0] + half_x;
        Scalar y = imgsize[1] - (half_y * p[1] + half_y) - 1.0;

        img.set(int(x), int(y), 0, fg_red[0]);
        img.set(int(x), int(y), 1, fg_red[1]);
        img.set(int(x), int(y), 2, fg_red[2]);
        img.set(int(x), int(y), 3, fg_red[3]);
    }
    std::string const fname = "unit_disk_uniform_sampler_res.ppm";

    bool const ret = saveArray3DPPM(img, fname, true);
    ASSERT_EQ(ret, true);
}


/// Sampler: UnitHemisphereUniform
/// TEST(test_case_name, test_name)
TEST(SamplarTest, UnitHemisphereUniform)
{
    SamplerUnitHemisphereUniform uhus;
    int const sample_count = 1024 * 1024 * 16;

    StopWatch sw;
    sw.run();

    // with #pragma omp parallel
    //   prng: drand48: 9.37715e+06 samples/sec (1 core, -max)
    //   prng: drand48: 7.1548e+06  samples/sec (2 core, -max)
    {
// #pragma omp parallel
        for(int i = 0; i < sample_count; ++i){
            Scalar_3 const v   = uhus.get_sample();
            Scalar const v_len = v.norm();
            assert(abs(v_len - 1.0) < 0.00001);
        }
    }
    sw.stop();
    std::cout << "prng: drand48: "
              << static_cast< Float64 >(sample_count) / sw.get_accumulated_time()
              << std::endl;
}

int main(int argc, char **argv)
{
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}


