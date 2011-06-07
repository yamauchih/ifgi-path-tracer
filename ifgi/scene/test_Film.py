#!/usr/bin/env python
#
#
# Copyright (C) 2010-2011 Yamauchi, Hitoshi
#
# test for Film module
#

"""test IFGI Film module"""

import unittest
import numpy
import Film

# test Film
class TestFilm(unittest.TestCase):
    """test suit for Film."""
    # test bbox
    def test_imagefilm(self):
        """test for ImageFilm"""
        f = Film.ImageFilm((128, 128, 4), 'RGBA')
        assert(str(f) == '[name: RGBA, resolution: (128 128 4)]')

        res = f.get_resolution()
        assert(res == (128, 128, 4))

        # fill white
        res = f.fill_color(numpy.array([1,1,1,1]))

        # draw a line
        red = numpy.array([1, 0, 0, 1])
        for i in xrange(10, 100, 1):
            f.put_color((i, i), red)
            assert((f.get_color((i, i)) == red).all())

        # save a file
        f.save_file('test_film_result.png')

#
# main test
#
suit0   = unittest.TestLoader().loadTestsFromTestCase(TestFilm)
alltest = unittest.TestSuite([suit0])
unittest.TextTestRunner(verbosity=2).run(alltest)
