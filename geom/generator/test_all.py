#!/usr/bin/env python
#
# Copyright (C) 2010-2011 Yamauchi, Hitoshi
#
#
"""test all in geom/generator"""

import unittest

import test_polygonal_cylinder_gen

#
# main test
#
if __name__ == '__main__':
    suits = []
    suits.append(unittest.TestLoader().loadTestsFromTestCase(test_polygonal_cylinder_gen.TestPolygonalCylinderGen))
    alltest = unittest.TestSuite(suits)
    unittest.TextTestRunner(verbosity=2).run(alltest)
