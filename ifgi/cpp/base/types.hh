//----------------------------------------------------------------------
// ifgi c++ implementation
// Copyright (C) 2010-2011 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief ifgi type definition

#ifndef IFGI_CPP_BASE_TYPES_HH
#define IFGI_CPP_BASE_TYPES_HH

#include <boost/static_assert.hpp>

namespace ifgi {

/// 8bit signed character (integer)
typedef signed char   Sint8;
/// 8bit unsigned character (integer)
typedef unsigned char Uint8;

/// 16bit signed integer
typedef signed short   Sint16;
/// 16bit unsigned integer
typedef unsigned short Uint16;

/// 32bit signed integer
typedef signed int   Sint32;
/// 32bit unsigned integer
typedef unsigned int Uint32;

/// 64bit signed integer
typedef signed long long   Sint64;
/// 64bit unsigned integer
typedef unsigned long long Uint64;

/// 32bit floating point
typedef float  Float32;
/// 64bit floating point
typedef double Float64;

BOOST_STATIC_ASSERT( sizeof(  Sint8) == 1);
BOOST_STATIC_ASSERT( sizeof(  Uint8) == 1);

BOOST_STATIC_ASSERT( sizeof( Sint16) == 2);
BOOST_STATIC_ASSERT( sizeof( Uint16) == 2);

BOOST_STATIC_ASSERT( sizeof( Sint32) == 4);
BOOST_STATIC_ASSERT( sizeof( Uint32) == 4);

BOOST_STATIC_ASSERT( sizeof( Sint64) == 8);
BOOST_STATIC_ASSERT( sizeof( Uint64) == 8);

BOOST_STATIC_ASSERT( sizeof(Float32) == 4);
BOOST_STATIC_ASSERT( sizeof(Float64) == 8);

} // namespace ifgi

#endif // #ifndef IFGI_CPP_BASE_TYPES_HH
