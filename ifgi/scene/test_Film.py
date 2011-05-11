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
        f = Film.ImageFilm(128, 128, 4, 'RGBA')
        assert(str(f) == '[name: RGBA, resolution: (128 128 4)]')

#
# main test
#
suit0   = unittest.TestLoader().loadTestsFromTestCase(TestFilm)
alltest = unittest.TestSuite([suit0])
unittest.TextTestRunner(verbosity=2).run(alltest)
