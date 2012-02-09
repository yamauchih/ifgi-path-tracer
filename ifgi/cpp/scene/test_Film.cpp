//----------------------------------------------------------------------
// ifgi c++ implementation: test_Film.py
// Copyright (C) 2010-2012 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief test_Film.py

#include "ImageFilm.hh"

#include <string>
#include <gtest/gtest.h>


/// Test ImageFilm
/// TEST(test_case_name, test_name)
TEST(ImageFilmTest, ImageFilmLineSaveTest)
{
    ifgi::ImageFilm film(ifgi::Sint32_3(128, 100, 4), "RGBA");
    ASSERT_EQ(film.to_string(), std::string("[name: RGBA, resolution: (128 100 4)]"));

    ifgi::Sint32_3 const res = film.get_resolution();
    ASSERT_EQ(res, ifgi::Sint32_3(128, 100, 4));

    // fill white color
    film.fill_color(ifgi::Color(1.0, 1.0, 1.0, 1.0));

    // draw a line
    ifgi::Color const red(1.0, 0.0, 0.0, 1.0);
    for(ifgi::Sint32 i = 10; i < 90; ++i){
        film.put_color(i, i, red);
        ASSERT_EQ(film.get_color(i, i), red);
    }

    // save a file
    ASSERT_EQ(film.save_file("test_film_result.ppm", "ppm"), true);
    ASSERT_EQ(film.save_file("test_film_result.gfi", "gfi"), true);
}

int main(int argc, char **argv)
{
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
