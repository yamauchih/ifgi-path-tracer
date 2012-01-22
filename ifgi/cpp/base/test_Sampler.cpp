//----------------------------------------------------------------------
// ifgi c++ implementation: test_Sampler.py
// Copyright (C) 2010-2012 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief Sampler unit test

#include "SamplerUnitDiskUniform.hh"
#include "Array3D.hh"
#include "LoadSavePPM.hh"

#include <gtest/gtest.h>

using namespace ifgi;

// # From file ILog (first one), import ILog (second one) class
// import Sampler

// class TestStratifiedRegularSampler(unittest.TestCase){
//     /// test: StratifiedRegularSampler/// 

//     def test_stratified_regular_sample(){
//         /// test stratified regular sample./// 

//         srs = Sampler.StratifiedRegularSampler();

//         xstart = 0
//         xend   = 16
//         ystart = 0
//         yend   = 10

//         srs.compute_sample(xstart, xend, ystart, yend);
//         for x in xrange(xstart, xend + 1, 1){
//             for y in xrange(ystart, yend + 1, 1){
//                 assert(srs.get_sample_x(x,y) == x + 0.5);
//                 assert(srs.get_sample_y(x,y) == y + 0.5);


/// Sampler: UnitDiskUniform
/// TEST(test_case_name, test_name)
TEST(SamplarTest, UnitDiskUniform)
{
    SamplerUnitDiskUniform udus;

    int const sample_count = 1000;

    /// set up an image
    Color bg_white(1.0f, 1.0f, 1.0f, 1.0f);
    Color fg_red  (1.0f, 0.0f, 0.0f, 1.0f);
    Float32_2 imgsize(128.0f, 128.0f);
    // img = Image.new("RGB", imgsize, bg_white);
    Array3D_Float32 img(static_cast< int >(imgsize[0]),
                        static_cast< int >(imgsize[1]),
                        4);
    img.clearWithValue(1.0f);

    for(int i = 0; i < sample_count; ++i){
        // p = [-1,1]x[-1,1]
        Float32_2 const p = udus.get_sample();

        Float32 half_x = 0.5 * (imgsize[0] - 1.0f);
        Float32 half_y = 0.5 * (imgsize[1] - 1.0f);
        Float32 x = half_x * p[0] + half_x;
        Float32 y = imgsize[1] - (half_y * p[1] + half_y) - 1.0;

        img.set(int(x), int(y), 0, fg_red[0]);
        img.set(int(x), int(y), 1, fg_red[1]);
        img.set(int(x), int(y), 2, fg_red[2]);
        img.set(int(x), int(y), 3, fg_red[3]);
    }
    std::string const fname = "unit_disk_uniform_sampler_res.ppm";

    bool const ret = saveArray3DPPM(img, fname, true);
    ASSERT_EQ(ret, true);
}



// class TestUnitHemisphereUniformSampler(unittest.TestCase){
//     /// test: UnitHemisphereUniformSampler/// 

//     def test_unit_hemisphere_uniform_sampler(){
//         /// test unit hemisphere uniform sampler./// 

//         uhus = Sampler.UnitHemisphereUniformSampler();

//         sample_count = 100

//         for i in xrange(sample_count){
//             v = uhus.get_sample();
//             v_len = numpy.linalg.norm(v);
//             assert(abs(v_len - 1.0) < 0.00001);

int main(int argc, char **argv)
{
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}


