#!/usr/bin/env python
#
# Copyright 2011 (C) Yamauchi, Hitoshi
#
#
# test for SceneGraph module
#

"""test IFGI SceneGraph module"""

import unittest
import numpy
import random
import SceneGraph, Primitive, Material

class TestSceneGraph(unittest.TestCase):
    """test scenegraph node"""

    def test_bbox(self):
        """"scenegraph bbox"""
        sg_node0 = SceneGraph.SceneGraphNode('sg_node0')
        sg_node1 = SceneGraph.SceneGraphNode('sg_node1')

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


    def test_node_creation(self):
        """test node creation"""
        sg = SceneGraph.create_empty_scenegraph()
        sg_root = sg.get_root_node()

        grp0 = SceneGraph.SceneGraphNode('group_test')
        sg_root.append_child(grp0)

        # primitives, but no data so far
        prim0 = SceneGraph.PrimitiveNode('tri')
        prim0.set_primitive(Primitive.Triangle())
        grp0.append_child(prim0)

        prim1 = SceneGraph.PrimitiveNode('trimesh')
        prim1.set_primitive(Primitive.TriMesh())
        grp0.append_child(prim1)

        # material group
        grp1 = SceneGraph.SceneGraphNode('materialgroup')
        sg_root.append_child(grp1)

        mat0 = SceneGraph.MaterialNode('mat0')
        mat0.set_material(Material.Material())
        grp1.append_child(mat0)


#
# main test
#
suit0   = unittest.TestLoader().loadTestsFromTestCase(TestSceneGraph)
alltest = unittest.TestSuite([suit0])
unittest.TextTestRunner(verbosity=2).run(alltest)
