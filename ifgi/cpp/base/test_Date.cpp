//----------------------------------------------------------------------
// ifgi c++ implementation: Date.hh
// Copyright (C) 2010-2012 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief Date unit test
#ifndef DOXYGEN_SKIP

#include "Date.hh"
#include <unistd.h>

#include <gtest/gtest.h>

// Tests DateTest
TEST(DateTest, Date)
{
    ifgi::Date date1;
    usleep(1000000);
    ifgi::Date date2;

    std::cout << "date1 getTime = " << date1.getTime()
              << ", str = "         << date1.toString() << "\n"
              << date1.toCTimeStr() << std::endl;
    std::cout << "date2 getTime = " << date2.getTime()
              << ", str = "         << date2.toString() << "\n"
              << date2.toCTimeStr() << std::endl;

    std::cout << "date1.after(date2)  = " << date1.after(date2)  << std::endl;
    std::cout << "date1.before(date2) = " << date1.before(date2) << std::endl;
    std::cout << "date1.equals(date2) = " << date1.equals(date2) << std::endl;

    double d1d = date1.getTimeAsDouble();
    double d2d = date2.getTimeAsDouble();

    std::cout << "date1.getTimeAsDouble() = "   << d1d
              << ", date2.getTimeAsDouble() = " << d2d
              << ", diff = " << d2d - d1d << std::endl;
}

int main(int argc, char **argv)
{
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}

#endif // #ifndef DOXYGEN_SKIP
