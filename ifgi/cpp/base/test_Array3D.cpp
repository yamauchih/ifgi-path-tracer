//----------------------------------------------------------------------
// test_Vector
// Copyright (C) 2010-2012 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief Array3D unit test

#include "Array3D.hh"

#include <gtest/gtest.h>

// Tests Vector
TEST(Array3DTest, Vectos)
{
    ifgi::Array3D_Float32 buf(256, 256, 4);

}

int main(int argc, char **argv)
{
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
