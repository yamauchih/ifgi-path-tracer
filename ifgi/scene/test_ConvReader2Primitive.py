#!/usr/bin/env python

"""test IFGI ConvReader2Primitive.
\file
\brief test for ConvReader2Primitive
"""

import unittest

import ObjReader
import Primitive
import ConvReader2Primitive

class TestConvReader2Primitive(unittest.TestCase):
    """test for ConvReader2Primitive."""

    def test_converter_0(self):
        """"test converter 0"""
        objreader = ObjReader.ObjReader()
        objreader.read('../../sampledata/one_tri.obj')

        tmesh = ConvReader2Primitive.conv_objreader_trimesh(objreader)

        self.assertEquals(len(tmesh.vertex_list),       3) # nvertices
        self.assertEquals(len(tmesh.face_idx_list),     1) # nface
        self.assertEquals(len(tmesh.texcoord_list),     0)
        self.assertEquals(len(tmesh.texcoord_idx_list), 0)
        self.assertEquals(len(tmesh.normal_list),       0)
        self.assertEquals(len(tmesh.normal_idx_list),   0)



#
# main test
#
suit0   = unittest.TestLoader().loadTestsFromTestCase(TestConvReader2Primitive)
alltest = unittest.TestSuite([suit0])
unittest.TextTestRunner(verbosity=2).run(alltest)
