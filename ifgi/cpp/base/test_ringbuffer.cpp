//----------------------------------------------------------------------
// ifgi c++ implementation: unit test for RingBuffer
// Copyright (C) 2010-2012 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief ring buffer unit test.
#ifndef DOXYGEN_SKIP

#include "RingBuffer.hh"

#include <gtest/gtest.h>

using namespace ifgi;

// enable debug logging when DEBUG_OUTPUT_MESSAGE is defined.
// #define DEBUG_OUTPUT_MESSAGE

/// logging
void println_message(std::string const & mes)
{
#ifdef DEBUG_OUTPUT_MESSAGE
    std::cout << mes << std::endl;
#endif
}

/// print ring buffer
void print_ring_buffer(RingBuffer & rb)
{
    std::stringstream sstr;
    for(RingBuffer::iterator ri = rb.begin(); ri != rb.end(); ++ri){
        sstr << (*ri) << " ";
    }
    println_message(sstr.str());
}

/// Tests ring buffer
/// TEST(test_case_name, test_name)
TEST(RingBuffer, RingBufferTest)
{
    size_t bufsize = 10;
    RingBuffer rb(bufsize);

    ASSERT_EQ(rb.empty(), true);
    ASSERT_EQ(rb.full(),  false);

    println_message(rb.to_string());
    for(int i = 0; i < 15; ++i){
        ASSERT_EQ(rb.size(), (static_cast< size_t >(i) >= bufsize) ? bufsize : i);
        rb.push_back(static_cast< Float64 >(i));

        println_message(rb.to_string());
        print_ring_buffer(rb);
    }
    ASSERT_EQ(rb.size(),  bufsize);

    rb.clear();
    println_message(rb.to_string());

    bufsize = 6;
    rb.resize_buffer(bufsize);
    ASSERT_EQ(rb.empty(), true);
    for(int i = 0; i < 12; ++i){
        rb.push_back(static_cast< Float64 >(i));

        println_message(rb.to_string());
        print_ring_buffer(rb);
    }

    ASSERT_EQ(rb.empty(), false);
    ASSERT_EQ(rb.full(),  true);
    ASSERT_EQ(rb.size(),  bufsize);
}

int main(int argc, char **argv)
{
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}

#endif
