#!/usr/bin/env python

"""test for Drawmode"""

import unittest
import DrawMode

class TestDrawMode(unittest.TestCase):
    """test: Drawmode"""

    def test_drawmode0(self):
        """test: DrawModeItem"""
        drmode = DrawMode.DrawModeList()
        drmode.add_basic_drawmode()
        # to see the mode items
        # drmode.print_obj()


    def test_drawmode_get_string(self):
        """test: get_drawmode_string"""
        self.assertEquals(DrawMode.get_drawmode_string(
            DrawMode.DrawModeList.DM_GlobalMode),
                          'Global')

        s = DrawMode.get_drawmode_string(DrawMode.DrawModeList.DM_BBox)
        self.assertEquals(s, 'BBox');

        s = DrawMode.get_drawmode_string(DrawMode.DrawModeList.DM_BBox +
                                         DrawMode.DrawModeList.DM_Points)
        self.assertEquals(s, 'BBox+Points');

        s = DrawMode.get_drawmode_string(DrawMode.DrawModeList.DM_Points +
                                         DrawMode.DrawModeList.DM_Wireframe)
        self.assertEquals(s, 'Points+Wireframe');

        # the following casts an exception: non existing drawmode.
        # s = DrawMode.get_drawmode_string(0x100000)


#
# main test
#
suit0   = unittest.TestLoader().loadTestsFromTestCase(TestDrawMode)
alltest = unittest.TestSuite([suit0])
unittest.TextTestRunner(verbosity=2).run(alltest)
