#!/usr/bin/env python
#
# test for SceneGraph module
#

"""test IFGI SceneGraph module"""

import unittest
import numpy
import random
import SceneGraph
import Primitive

class TestSceneGraph(unittest.TestCase):
    # test scenegraph node
    def test_bbox(self):
        sg_node0 = SceneGraph.SceneGraphNode()
        sg_node1 = SceneGraph.SceneGraphNode()

        p0 = numpy.array([-2.0, -2.0, -2.0])
        p1 = numpy.array([ 1.0,  1.0,  3.0])
        bbox0 = Primitive.BBox()
        bbox0.insert_point(p0)
        bbox0.insert_point(p1)

        sg_node0.set_bbox(bbox0)

        # update the bbox0
        p2 = numpy.array([ 4.0,  4.0,  4.0])
        bbox0.insert_point(p2)
        sg_node1.set_bbox(bbox0)

        assert(not sg_node0.get_bbox().equal(sg_node1.get_bbox()))


#
# main test
#
suit0   = unittest.TestLoader().loadTestsFromTestCase(TestSceneGraph)
alltest = unittest.TestSuite([suit0])
unittest.TextTestRunner(verbosity=2).run(alltest)
