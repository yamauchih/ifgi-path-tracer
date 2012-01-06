//----------------------------------------------------------------------
// test_Dictionary
// Copyright (C) 2010-2011 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief Dictionary unit test

#include "Dictionary.hh"

#include <gtest/gtest.h>

// Tests Dictionary
TEST(DictionaryTest, Vectos)
{
    // POD types
    {
        ifgi::Dictionary dict;
        bool const b0 = true;
        ifgi::Sint32  const x0(42);
        ifgi::Float32 const x1(27.5);
        ifgi::Float64 const x2(-10.1);

        dict.insert("b0", ifgi::Dictionary_value(b0));
        dict.insert("x0", ifgi::Dictionary_value(x0));
        dict.insert("x1", ifgi::Dictionary_value(x1));
        dict.insert("x2", ifgi::Dictionary_value(x2));


        bool          const b1 = dict.get< bool > ("b0");
        ifgi::Sint32  const y0 = dict.get< ifgi::Sint32 > ("x0");
        ifgi::Float32 const y1 = dict.get< ifgi::Float32 >("x1");
        ifgi::Float64 const y2 = dict.get< ifgi::Float64 >("x2");

        ASSERT_EQ(b0, b1);
        ASSERT_EQ(x0, y0);
        ASSERT_EQ(x1, y1);
        ASSERT_EQ(x2, y2);
        // write test
        dict.write(std::cout, "write_test::");

        ASSERT_EQ(dict.erase("b0"), true);  // erase succeeded
        ASSERT_EQ(dict.erase("b0"), false); // no more key

        // iterator test
        for(ifgi::Dictionary::const_iterator di = dict.begin();
            di != dict.end(); ++di)
        {
            std::cout << "di->first: " << di->first
                      << ", di->second: " << di->second.get_string() << std::endl;
        }
    }

    // std::string
    {
        ifgi::Dictionary dict;
        std::string const in = "Hello IFGI.";

        dict.insert("in", ifgi::Dictionary_value(in));

        std::string const out = dict.get< std::string > ("in");

        ASSERT_EQ(in, out);
    }

    // Float32_3
    {
        ifgi::Dictionary dict;
        ifgi::Float32_3 const v0(1.0f, 2.0f, 3.0f);

        // insert test
        dict.insert("v0", ifgi::Dictionary_value(v0));
        ifgi::Float32_3 v1 = dict.get< ifgi::Float32_3 >("v0");
        ASSERT_EQ(v0, v1);

        // override
        ifgi::Float32_3 const v2(10.0f, 11.0f, 12.0f);
        dict.set("v0", v2);
        ASSERT_EQ(v2, dict.get< ifgi::Float32_3 >("v0"));

        ASSERT_EQ(dict.empty(), false);
        ASSERT_EQ(dict.size(),  1);
    }
}

int main(int argc, char **argv)
{
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
