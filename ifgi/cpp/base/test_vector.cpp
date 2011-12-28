//----------------------------------------------------------------------
// test_vector: google test
// Copyright (C) 2010-2011 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief Vector test

#include "Vector.hh"

#include <gtest/gtest.h>

// Tests Vector
TEST(VectorTest, Vectos)
{
    ifgi::Float32_3 v0(1.0f, 0.0f, 0.0f);
    ifgi::Float32_3 v1(0.0f, 1.0f, 0.0f);

    ifgi::Float32_3 v2 =  cross(v0, v1);
}

int main(int argc, char **argv)
{
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
