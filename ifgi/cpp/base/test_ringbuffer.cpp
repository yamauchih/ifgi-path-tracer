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

/// print ring buffer
void print_ring_buffer(RingBuffer & rb)
{
    for(RingBuffer::iterator ri = rb.begin(); ri != rb.end(); ++ri){
        std::cout << (*ri) << " ";
    }
    std::cout << std::endl;
}


/// Tests ring buffer
/// TEST(test_case_name, test_name)
TEST(RingBuffer, RingBufferTest)
{
    size_t bufsize = 10;
    RingBuffer rb(bufsize);

    ASSERT_EQ(rb.empty(), true);
    ASSERT_EQ(rb.full(),  false);

    std::cout << rb.to_string() << std::endl;
    for(int i = 0; i < 15; ++i){
        ASSERT_EQ(rb.size(), (static_cast< size_t >(i) >= bufsize) ? bufsize : i);
        rb.push_back(static_cast< Float64 >(i));

        std::cout << rb.to_string() << std::endl;
        print_ring_buffer(rb);
    }
    ASSERT_EQ(rb.size(),  bufsize);

    rb.clear();
    std::cout << rb.to_string() << std::endl;

    bufsize = 6;
    rb.resize_buffer(bufsize);
    ASSERT_EQ(rb.empty(), true);
    for(int i = 0; i < 12; ++i){
        rb.push_back(static_cast< Float64 >(i));

        std::cout << rb.to_string() << std::endl;
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
