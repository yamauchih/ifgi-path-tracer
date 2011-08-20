#!/usr/bin/env python
#
# Copyright 2011 (C) Yamauchi, Hitoshi
#
# test for ObjReader
#

"""test IFGI ObjReader"""

import unittest
import ObjReader

class TestObjReader(unittest.TestCase):
    """test for obj file reader"""

    def test_objreader_unit0(self):
        """objreader test 0"""
        objreader = ObjReader.ObjReader()

        datlist = [
            ['1'],
            ['1', '2'],
            ['1', '2', '3'],
            ['1', '',  '3'],
            ['1', '2', ''],
            ['1', '',  '']
            ]
        anslist = [
            [True, False, False],
            [True, True,  False],
            [True, True,  True],
            [True, False, True],
            [True, True,  False],
            [True, False, False],
            ]
        n = len(datlist)
        i = 0
        while i < n:
            item = objreader.get_process_dict(datlist[i])
            self.assertEquals(item['face_idx'],     anslist[i][0])
            self.assertEquals(item['texcoord_idx'], anslist[i][1])
            self.assertEquals(item['normal_idx'],   anslist[i][2])
            i = i + 1


    def test_objreader_sample0(self):
        """objreader sample0"""
        objreader = ObjReader.ObjReader()
        objreader.read('../../sampledata/one_tri.obj')
        # objreader.dump()

        self.assertEquals(len(objreader.vertex_list), 3)   # nvertices
        self.assertEquals(len(objreader.face_idx_list), 1) # nface

    def test_objreader_sample2(self):
        """objreader sample2"""
        objreader = ObjReader.ObjReader()
        objreader.read('../../sampledata/cylinder.obj')
        # objreader.dump()

        self.assertEquals(len(objreader.vertex_list),   142) # nvertices
        self.assertEquals(len(objreader.face_idx_list), 280) # nface


#     def test_objreader_sample2(self):
#         objreader = ObjReader.ObjReader()
#         objreader.read('../sampledata/cylinder.obj')

#
# main test
#
suit0   = unittest.TestLoader().loadTestsFromTestCase(TestObjReader)
alltest = unittest.TestSuite([suit0])
unittest.TextTestRunner(verbosity=2).run(alltest)
