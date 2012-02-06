//----------------------------------------------------------------------
// ifgi c++ implementation: test_OrthonomalBasis.cpp
// Copyright (C) 2010-2012 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief test_OrthonomalBasis.cpp

#include "OrthonomalBasis.hh"

#include <gtest/gtest.h>

using namespace ifgi;

/// OrthonomalBasis
/// TEST(test_case_name, test_name)
TEST(OrthonomalBasisTest, InitializeTest)
{
    OrthonomalBasis onb0;
    onb0.init_from_u(Scalar_3(1.0, 0.0, 0.0));
    std::cout << onb0.to_string() << std::endl;
}

int main(int argc, char **argv)
{
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
