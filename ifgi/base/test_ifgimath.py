#!/usr/bin/env python
#
# Copyright (C) 2010-2011 Yamauchi, Hitoshi
#

"""test IFGI math module"""

import unittest
import numpy
import ifgimath

class TestIFGImathModule(unittest.TestCase):
    """test: IFGImathModule"""

    def test_mapToSphere(self):
        """test mapToSphere function."""

        win_pos_list = [numpy.array([  0,   0]),
                        numpy.array([100,   0]),
                        numpy.array([ 80,  90]), # center
                        numpy.array([150, 150]),
                        numpy.array([159, 179]) # corner
                        # out of range numpy.array([200, 200])
                        ]
        win_width  = 160
        win_height = 180
        pos3d_on_sphere = numpy.array([0, 0, 0])

        for wpos in win_pos_list:
            ret = ifgimath.mapToSphere(wpos, win_width, win_height)
            # print 'map to sphere ' + str(wpos) + ' -> ' + str(ret)

    # test getRotationMat
    # def test_getRotateMat(self):


#
# main test
#
if __name__ == '__main__':
    suit0   = unittest.TestLoader().loadTestsFromTestCase(TestIFGImathModule)
    alltest = unittest.TestSuite([suit0])
    unittest.TextTestRunner(verbosity=2).run(alltest)
