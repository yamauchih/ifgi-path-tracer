#!/usr/bin/env python
#
# Copyright (C) 2010-2011 Yamauchi, Hitoshi
#
#
"""test ifgi Sampler"""

import unittest
import numpy
from PIL import Image

# From file ILog (first one), import ILog (second one) class
import Sampler

class TestStratifiedRegularSampler(unittest.TestCase):
    """test: StratifiedRegularSampler"""

    def test_stratified_regular_sample(self):
        """test stratified regular sample."""

        srs = Sampler.StratifiedRegularSampler()

        xstart = 0
        xend   = 16
        ystart = 0
        yend   = 10

        srs.compute_sample(xstart, xend, ystart, yend)
        for x in xrange(xstart, xend + 1, 1):
            for y in xrange(ystart, yend + 1, 1):
                assert(srs.get_sample_x(x,y) == x + 0.5)
                assert(srs.get_sample_y(x,y) == y + 0.5)


class TestUnitDiskUniformSampler(unittest.TestCase):
    """test: UnitDiskUniformSampler"""

    def test_unit_disk_uniform_sampler(self):
        """test unit disk uniform sampler."""

        udus = Sampler.UnitDiskUniformSampler()

        sample_count = 1000

        # set up an image
        bg_white = (255, 255, 255)
        fg_red   = (255, 0,   0)
        imgsize  = (128, 128)
        img = Image.new("RGB", imgsize, bg_white)

        for i in xrange(sample_count):
            # p = [-1,1]x[-1,1]
            p = udus.get_sample()

            half_x = 0.5 * (imgsize[0] - 1)
            half_y = 0.5 * (imgsize[1] - 1)
            x = half_x * p[0] + half_x
            y = imgsize[1] - (half_y * p[1] + half_y) - 1
            img.putpixel((int(x), int(y)), fg_red)


        fname = 'unit_disk_uniform_sampler_res.png'
        img.save(fname)


class TestUnitHemisphereUniformSampler(unittest.TestCase):
    """test: UnitHemisphereUniformSampler"""

    def test_unit_hemisphere_uniform_sampler(self):
        """test unit hemisphere uniform sampler."""

        uhus = Sampler.UnitHemisphereUniformSampler()

        sample_count = 100

        for i in xrange(sample_count):
            v = uhus.get_sample()
            v_len = numpy.linalg.norm(v)
            assert(abs(v_len - 1.0) < 0.00001)


#
# main test
#
if __name__ == '__main__':
    suit0   = unittest.TestLoader().loadTestsFromTestCase(TestStratifiedRegularSampler)
    suit1   = unittest.TestLoader().loadTestsFromTestCase(TestUnitDiskUniformSampler)
    suit2   = unittest.TestLoader().loadTestsFromTestCase(TestUnitHemisphereUniformSampler)
    alltest = unittest.TestSuite([suit0, suit1, suit2])
    unittest.TextTestRunner(verbosity=2).run(alltest)
