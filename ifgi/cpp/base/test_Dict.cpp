//----------------------------------------------------------------------
// test_vector: google test
// Copyright (C) 2010-2011 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief Dictionary test

#include "Dict.hh"

#include <gtest/gtest.h>

// Tests Dict
TEST(DictTest, Vectos)
{
    ifgi::Float32_3 const v0(1.0f, 2.0f, 3.0f);
    ifgi::Dict dict;

    // insert test
    dict.insert("v0", ifgi::Dict_value(v0));
    ifgi::Float32_3 v1 = dict.get< ifgi::Float32_3 >("v0");
    ASSERT_EQ(v0, v1);

    // override
    ifgi::Float32_3 const v2(10.0f, 11.0f, 12.0f);
    dict.set("v0", v2);
    ASSERT_EQ(v2, dict.get< ifgi::Float32_3 >("v0"));

    ASSERT_EQ(dict.empty(), false);
    ASSERT_EQ(dict.size(),  1);
}

int main(int argc, char **argv)
{
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
