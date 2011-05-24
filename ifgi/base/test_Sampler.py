#!/usr/bin/env python
#
# Copyright (C) 2010-2011 Yamauchi, Hitoshi
#
#
"""test ifgi Sampler"""

import unittest

# From file ILog (first one), import ILog (second one) class
from Sampler import StratifiedRegularSampler

class TestStratifiedRegularSampler(unittest.TestCase):
    """test: StratifiedRegularSampler"""

    def test_stratified_regular_sample(self):
        """test stratified regular sample."""

        srs = StratifiedRegularSampler()

        xstart = 0
        xend   = 16
        ystart = 0
        yend   = 10

        srs.compute_sample(xstart, xend, ystart, yend)
        for x in xrange(xstart, xend + 1, 1):
            for y in xrange(ystart, yend + 1, 1):
                assert(srs.get_sample_x(x,y) == x + 0.5)
                assert(srs.get_sample_y(x,y) == y + 0.5)


#
# main test
#
suit0   = unittest.TestLoader().loadTestsFromTestCase(TestStratifiedRegularSampler)
alltest = unittest.TestSuite([suit0])
unittest.TextTestRunner(verbosity=2).run(alltest)
