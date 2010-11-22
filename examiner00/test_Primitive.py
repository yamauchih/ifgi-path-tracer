#!/usr/bin/env python
#
# test for Primitive module
#

"""test IFGI Primitive module"""

import unittest
import numpy
import random
import Primitive

class TestPrimitive(unittest.TestCase):
    # test bbox
    def test_bbox(self):
        random.seed(0)

        minp = numpy.array([-2.0, -1.0,  1.2])
        maxp = numpy.array([-0.2,  1.0,  5.5])
        ipos = numpy.array([ 0.0,  0.0,  0.0])
        bbox = Primitive.BBox()
        for p in xrange(1000):
            for i in xrange(0, 3, 1):
                ipos[i] = random.uniform(minp[i], maxp[i])
                # print i, ipos
            bbox.insert_point(ipos)

        for i in xrange(2):
            assert(minp[i]     <= bbox.min[i])
            assert(bbox.min[i] <= bbox.max[i])
            assert(bbox.max[i] <= maxp[i])


#
# main test
#
suit0   = unittest.TestLoader().loadTestsFromTestCase(TestPrimitive)
alltest = unittest.TestSuite([suit0])
unittest.TextTestRunner(verbosity=2).run(alltest)
