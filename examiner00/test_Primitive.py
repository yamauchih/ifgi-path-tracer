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
    """test suit for Primitive."""
    # test bbox
    def test_bbox(self):
        """test for bbox"""
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

    # test primitive: one triangle
    def test_primitive_one_tri(self):
        """test primitive: one triangle"""
        tmesh = Primitive.TriMesh()

        vertex_list       = []
        face_idx_list     = []
        texcoord_list     = []
        texcoord_idx_list = []
        normal_list       = []
        normal_idx_list   = []

        # add a triangle
        vertex_list.append(numpy.array([ 1.0, 0.0, 0.0]))
        vertex_list.append(numpy.array([ 0.0, 1.0, 0.0]))
        vertex_list.append(numpy.array([-1.0, 0.0, 0.0]))
        face_idx_list.append(numpy.array([0, 1, 2]))

        tmesh.set_data(vertex_list,
                       face_idx_list,
                       texcoord_list,
                       texcoord_idx_list,
                       normal_list,
                       normal_idx_list
                       )
        bbox = Primitive.BBox()
        bbox.insert_point(numpy.array([-1.0, 0.0, 0.0]))
        bbox.insert_point(numpy.array([ 1.0, 1.0, 0.0]))
        assert(tmesh.get_bbox().equal(bbox))

#
# main test
#
suit0   = unittest.TestLoader().loadTestsFromTestCase(TestPrimitive)
alltest = unittest.TestSuite([suit0])
unittest.TextTestRunner(verbosity=2).run(alltest)
