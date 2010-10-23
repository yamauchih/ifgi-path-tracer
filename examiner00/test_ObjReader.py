#!/usr/bin/env python
#
# test for ObjReader
#

"""test IFGI ObjReader"""

import unittest
import ObjReader

class TestObjReader(unittest.TestCase):

    def test_objreader_unit0(self):
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
        while True:
            item = objreader.get_process_dict(datlist[i])
            self.assertEquals(item, anslist[i][0])
            self.assertEquals(item, anslist[i][1])
            self.assertEquals(item, anslist[i][2])
            i = i + 1


    def test_objreader_sample0(self):
        objreader = ObjReader.ObjReader()
        objreader.read('../sampledata/one_tri.obj')
        objreader.dump()

        self.assertEquals(len(objreader.vertex_list), 3)   # nvertices = 3
        self.assertEquals(len(objreader.face_idx_list), 1) # nface     = 1

        


#     def test_objreader_sample2(self):
#         objreader = ObjReader.ObjReader()
#         objreader.read('../sampledata/cylinder.obj')




#
# main test
#
suit0   = unittest.TestLoader().loadTestsFromTestCase(TestObjReader)
alltest = unittest.TestSuite([suit0])
unittest.TextTestRunner(verbosity=2).run(alltest)
