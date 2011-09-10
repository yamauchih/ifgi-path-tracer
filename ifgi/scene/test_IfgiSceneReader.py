#!/usr/bin/env python
#
# Copyright 2011 (C) Yamauchi, Hitoshi
#
# test for IfgiSceneReader
#

"""test IFGI IfgiSceneReader"""

import unittest
import IfgiSceneReader

class TestIfgiSceneReader(unittest.TestCase):
    """test for ifgi scene reader"""

    def test_ifgiscenereader_unit0(self):
        """ifgi scene reader sample0"""
        ifgireader = IfgiSceneReader.IfgiSceneReader()
        ifgireader.read('../../sampledata/cornel_box.ifgi')
        # ifgireader.dump()

        self.assertEquals(len(ifgireader.material_list), 8)
        self.assertEquals(len(ifgireader.geometry_list), 8)


#
# main test
#
if __name__ == '__main__':
    suit0   = unittest.TestLoader().loadTestsFromTestCase(TestIfgiSceneReader)
    alltest = unittest.TestSuite([suit0])
    unittest.TextTestRunner(verbosity=2).run(alltest)
