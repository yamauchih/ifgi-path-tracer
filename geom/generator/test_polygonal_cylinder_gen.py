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
        pc_gen.clear()
        pc_gen.set_n_gon(6)
        pc_gen.set_generate_segment_tris(True)
        pc_gen.append_center_point(numpy.array([0.0, 0.0,  0.0]), 2)
        pc_gen.append_center_point(numpy.array([0.0, 0.0,  5.0]), 2)
        pc_gen.append_center_point(numpy.array([0.0, 0.0, 10.0]), 2)
        pc_gen.gen_cylinder()
        pc_gen.export_obj('cylinder0.obj')
        # print pc_gen

        # different radius, 12-gon
        pc_gen.clear()
        pc_gen.set_n_gon(12)
        pc_gen.append_center_point(numpy.array([0.0, 0.0,  0.0]), 2)
        pc_gen.append_center_point(numpy.array([0.0, 0.0,  4.0]), 2)
        pc_gen.append_center_point(numpy.array([0.0, 0.0,  5.0]), 3)
        pc_gen.append_center_point(numpy.array([0.0, 0.0,  6.0]), 2)
        pc_gen.append_center_point(numpy.array([0.0, 0.0, 10.0]), 2)
        pc_gen.gen_cylinder()
        pc_gen.export_obj('cylinder1.obj')
        # print pc_gen

        # skewed center, 12-gon, without top and bottom polygons
        pc_gen.clear()
        pc_gen.set_n_gon(12)
        pc_gen.append_center_point(numpy.array([0.3, 0.0,  0.0]), 1)
        pc_gen.append_center_point(numpy.array([0.0, 0.0,  4.0]), 1)
        pc_gen.append_center_point(numpy.array([0.0, 0.0,  5.0]), 3)
        pc_gen.append_center_point(numpy.array([0.0, 0.0,  6.0]), 1)
        pc_gen.append_center_point(numpy.array([0.3, 0.0, 10.0]), 2)
        pc_gen.gen_cylinder()
        pc_gen.export_obj('cylinder2.obj')
        # print pc_gen


#
# main test
#
# if __name__ == '__main__':
#     suit0   = unittest.TestLoader().loadTestsFromTestCase(TestPolygonalCylinderGen)
#     alltest = unittest.TestSuite([suit0])
#     unittest.TextTestRunner(verbosity=2).run(alltest)


