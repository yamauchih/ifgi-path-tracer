#!/usr/bin/env python
#
# Copyright (C) 2010-2011 Yamauchi, Hitoshi
#
# polygonal cylinder generator test
#
# For set up the environment to run, see test_all.sh
#
"""
\file
\brief polygonal cylinder generator test
"""

import unittest, numpy
import polygonal_cylinder_gen

# package import: specify a directory and file.
# from ifgi.ptracer import IfgiSys

class TestPolygonalCylinderGen(unittest.TestCase):
    """test: polygonal cylinder generator test."""

    def test_gen(self):
        """test generating a cylinder"""
        pc_gen = polygonal_cylinder_gen.Polygonal_cylinder_gen()

        # a simple one
        pc_gen.set_n_gon(6)
        pc_gen.set_polygon(0, numpy.array([0.0, 0.0, 10.0]), 2)
        pc_gen.set_polygon(1, numpy.array([0.0, 0.0,  0.0]), 2)
        pc_gen.gen_cylinder()
        pc_gen.export_obj('cylinder0.obj')

        # different radius, 12-gon
        pc_gen.set_n_gon(12)
        pc_gen.set_polygon(0, numpy.array([0.0, 0.0, 10.0]), 2)
        pc_gen.set_polygon(1, numpy.array([0.0, 0.0,  0.0]), 5)
        pc_gen.gen_cylinder()
        pc_gen.export_obj('cylinder1.obj')

        # skewed center, 12-gon
        pc_gen.set_n_gon(12)
        pc_gen.set_polygon(0, numpy.array([3.0, 0.0, 10.0]), 2)
        pc_gen.set_polygon(1, numpy.array([0.0, 0.0,  0.0]), 5)
        pc_gen.gen_cylinder()
        pc_gen.export_obj('cylinder2.obj')


#
# main test
#
# if __name__ == '__main__':
#     suit0   = unittest.TestLoader().loadTestsFromTestCase(TestPolygonalCylinderGen)
#     alltest = unittest.TestSuite([suit0])
#     unittest.TextTestRunner(verbosity=2).run(alltest)


