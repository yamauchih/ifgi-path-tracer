//----------------------------------------------------------------------
// test_Vector
// Copyright (C) 2010-2012 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief Vector unit test

#include "Vector.hh"

#include <gtest/gtest.h>

// Tests Vector
TEST(VectorTest, Vectos)
{
    ifgi::Float32_3 const v0(1.0f, 0.0f, 0.0f);
    ifgi::Float32_3 const v1(0.0f, 1.0f, 0.0f);
    ifgi::Float32_3 const v2(1.0f, 1.0f, 0.0f);
    ifgi::Float32_3 const v3(0.0f, 0.0f, 1.0f);

    // add
    {
        ifgi::Float32_3 vr0(0.0f, 0.0f, 0.0f);
        vr0 += v0;
        ASSERT_EQ(vr0, v0);
        ifgi::Float32_3 const vr1 = v0 + v1;
        ASSERT_EQ(vr1, v2);
    }

    // sub
    {
        ifgi::Float32_3 vr0(0.0f, 0.0f, 0.0f);
        vr0 -= v0;
        ifgi::Float32_3 vr1(-1.0f, 0.0f, 0.0f);
        ASSERT_EQ(vr0, vr1);

        ifgi::Float32_3 const vr2 = v0 - v1;
        ifgi::Float32_3 const vr3(1.0f, -1.0f, 0.0f);
        ASSERT_EQ(vr2, vr3);
    }

    // cross
    {
        ifgi::Float32_3 vr0 =  cross(v0, v1);
        ASSERT_EQ(v3, vr0);
    }
}

int main(int argc, char **argv)
{
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
