#!/usr/bin/env python
#
# Copyright 2011 (C) Yamauchi, Hitoshi
#
# test for ExtObjReader
#

"""test IFGI ExtObjReader"""

import unittest
import ExtObjReader

class TestExtObjReader(unittest.TestCase):
    """test for extended obj file reader"""

    def test_extobjreader_unit0(self):
        """extended objreader test 0"""
        eobjreader = ExtObjReader.ExtObjReader()

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
            item = eobjreader.get_process_dict(datlist[i])
            self.assertEquals(item['face_idx'],     anslist[i][0])
            self.assertEquals(item['texcoord_idx'], anslist[i][1])
            self.assertEquals(item['normal_idx'],   anslist[i][2])
            i = i + 1


    def test_extobjreader_sample0(self):
        """extended objreader sample0"""
        eobjreader = ExtObjReader.ExtObjReader()
        eobjreader.read('../../sampledata/one_tri.ifgi')
        eobjreader.dump()

        self.assertEquals(len(eobjreader.vertex_list), 3)   # nvertices
        self.assertEquals(len(eobjreader.face_idx_list), 1) # nface

    # def test_extobjreader_sample2(self):
    #     """objreader sample2"""
    #     eobjreader = ExtObjReader.ExtObjReader()
    #     eobjreader.read('../../sampledata/two_tri.ifgi')
    #     eobjreader.dump()

    #     self.assertEquals(len(eobjreader.vertex_list),   142) # nvertices
    #     self.assertEquals(len(eobjreader.face_idx_list), 280) # nface


#     def test_objreader_sample2(self):
#         objreader = ObjReader.ObjReader()
#         objreader.read('../sampledata/cylinder.obj')

#
# main test
#
suit0   = unittest.TestLoader().loadTestsFromTestCase(TestExtObjReader)
alltest = unittest.TestSuite([suit0])
unittest.TextTestRunner(verbosity=2).run(alltest)
