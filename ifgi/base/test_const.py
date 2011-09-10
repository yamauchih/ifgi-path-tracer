#!/usr/bin/env python
#
# Copyright (C) 2010-2011 Yamauchi, Hitoshi
#
"""const test.
\file
\brief test for python const.
"""
import unittest
import const

# This works well
# const.a = 'hello'
# const.a = 'world'

# This works well
class TestConst(unittest.TestCase):
    """const test"""

    def test_const(self):
        """test const."""
        const.a = 'hello'
        self.a = const.a
        self.a = 'world'
        # print self.a

#
# main test
#
if __name__ == '__main__':
    suit0   = unittest.TestLoader().loadTestsFromTestCase(TestConst)
    alltest = unittest.TestSuite([suit0])
    unittest.TextTestRunner(verbosity=2).run(alltest)


