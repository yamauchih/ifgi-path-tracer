//----------------------------------------------------------------------
// ifgi c++ implementation: test_Primitive.cpp
// Copyright (C) 2010-2012 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief test primitive

#include "Camera.hh"
#include "HitRecord.hh"
#include "ImageFilm.hh"
#include "Ray.hh"
#include "Triangle.hh"

#include <gtest/gtest.h>

using namespace ifgi;

/// Test Primitive, triangle ray intersection test
/// TEST(test_case_name, test_name)
TEST(PrimitiveTest, RayTriIntersectionTest1)
{
    // One ray and one trianle
    // create a triangle
    Scalar_3 p0( 1.0f, 0.0f,    0.0f);
    Scalar_3 p1( 0.0f, 1.7321f, 0.0f);
    Scalar_3 p2(-1.0f, 0.0f,    0.0f);

    Dictionary cam_dict;
    cam_dict.set("cam_name", "default");
    cam_dict.set("eye_pos", "0.0 0.64 0.76");
    cam_dict.set("view_dir", "0.0 0.0 -1.0");
    cam_dict.set("up_dir", "0.0 1.0 0.0");
    cam_dict.set("z_near", "0.1");
    cam_dict.set("z_far", "10000");
    cam_dict.set("resolution_x", "64");
    cam_dict.set("resolution_y", "64");

    Camera cam;
    cam.set_config_dict(cam_dict);

    Triangle tri;
    tri.set_vertex(p0, p1, p2);
    // std::cout << "tri.to_string(): " << tri.to_string() << std::endl;

    HitRecord hr;

    Ray r;
    cam.get_ray(0.5, 0.5, r);
    // std::cout << "Ray: " << r.to_string() << std::endl;

    hr.initialize();
    ASSERT_EQ(tri.ray_intersect(r, hr), true);
}

/// Test Primitive, triangle ray intersection test
/// TEST(test_case_name, test_name)
TEST(PrimitiveTest, RayTriIntersectionTest2)
{
    Scalar const iw = 50.0;
    Scalar const ih = 50.0;
    // imgsize = (iw, ih);

    // create a triangle
    Scalar xoff = iw / 10.0;
    Scalar yoff = iw / 10.0;
    Scalar_3 p0(xoff,           yoff, -10.0);
    Scalar_3 p1(iw - xoff,      yoff, -10.0);
    Scalar_3 p2(iw/2.0,    ih - yoff, -10.0);

    Triangle tri;
    tri.set_vertex(p0, p1, p2);

    Color const white(1.0, 1.0, 1.0, 1.0);
    Color const red  (1.0, 0.0, 0.0, 1.0);
    Sint32_3 const imgsize(static_cast< Sint32 >(iw),
                            static_cast< Sint32 >(ih),
                            4);
    ImageFilm img(imgsize, "RGBA");
    img.fill_color(white);
    Ray r;
    HitRecord hr;

    for(Sint32 x = 0; x < imgsize[0]; ++x){
        for(Sint32 y = 0; y < imgsize[1]; ++y){
            Scalar_3 const origin(static_cast< Scalar >(x),
                                  static_cast< Scalar >(y),
                                  0.0);
            Scalar_3 const dir(0.0, 0.0, -1.0);
            Scalar const min_t = 0.1;
            Scalar const max_t = 100.0;
            r.initialize(origin, dir, min_t, max_t);
            hr.initialize();
            if(tri.ray_intersect(r, hr)){
                // std::cout << "test_Primitive: Hit: " << origin << std::endl;
                img.put_color(x, y, red);
            }
        }
    }

    std::string const fname = "res_ray_tri_intersect.ppm";
    img.save_file(fname, "ppm");
    std::cout << "Saved ... [" << fname << "]" << std::endl;
}

/// Test Primitive, triangle ray intersection test
/// TEST(test_case_name, test_name)
TEST(PrimitiveTest, BBoxTest)
{
    srand48(0);

    Scalar_3 const minp(-2.0, -1.0,  1.2);
    Scalar_3 const maxp(-0.2,  1.0,  5.5);
    Scalar_3 ipos( 0.0,  0.0,  0.0);
    BBoxScalar bbox;
    for(Sint32 p = 0; p < 1000; ++p){
        for(Sint32 i = 0; i < 3; ++i){
            ipos[i] = drand48() * (maxp[i] - minp[i]) + minp[i];
            // std::cout << i << ", " << ipos << std::endl;
        }
        bbox.insert_point(ipos);
    }
    for(Sint32 i = 0; i < 3; ++i){
        // std::cout << "[" << bbox.get_min() << "]["
        //           << bbox.get_max() << "]" << std::endl;
        ASSERT_LE(minp[i],           bbox.get_min()[i]);
        ASSERT_LE(bbox.get_min()[i], bbox.get_max()[i]);
        ASSERT_LE(bbox.get_max()[i], maxp[i]);
    }
}

int main(int argc, char **argv)
{
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}



