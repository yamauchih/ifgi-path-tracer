//----------------------------------------------------------------------
// test_Vector
// Copyright (C) 2010-2011 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief Vector test

#define BOOST_TEST_MODULE Vector_test test
#include <boost/test/unit_test.hpp>

#include "Vector.hh"

BOOST_AUTO_TEST_CASE( Vector_test )
{
    ifgi::Float32_3 v0(1.0f, 0.0f, 0.0f);
    ifgi::Float32_3 v1(0.0f, 1.0f, 0.0f);

    ifgi::Float32_3 v2 =  cross(v0, v1);
}
