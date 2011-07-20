#!/usr/bin/env python
#
# Copyright (C) 2010-2011 Yamauchi, Hitoshi
#

"""test numpy utility"""

import unittest
import numpy
import numpy_util

class TestNumpyUtil(unittest.TestCase):
    """test: IFGImathModule"""

    def test_conversion(self):
        """test numpy utility conversion function."""

        array_list = [numpy.array([  0,   0,  0]),
                      numpy.array([100,   0, 10]),
                      numpy.array([ 80,  90, 20]),
                      numpy.array([150, 150, 30]),
                      numpy.array([159, 179, 40])
                        ]

        for ary in array_list:
            s = numpy_util.array2str(ary)
            back_ary = numpy_util.str2array(s)
            # print ary, ' -> ', s, ' -> ', back_ary, ' -> ',\
            #     numpy_util.array2str(back_ary)
            assert(all(ary == back_ary))


#
# main test
#
suit0   = unittest.TestLoader().loadTestsFromTestCase(TestNumpyUtil)
alltest = unittest.TestSuite([suit0])
unittest.TextTestRunner(verbosity=2).run(alltest)
