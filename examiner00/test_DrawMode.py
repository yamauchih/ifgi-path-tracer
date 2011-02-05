#!/usr/bin/env python

"""test for Drawmode"""

import unittest
import DrawMode

class TestDrawMode(unittest.TestCase):
    """test: Drawmode"""

    def test_drawmode0(self):
        """test: Drawmode"""
        drmode = DrawMode.DrawModeList()
        drmode.add_basic_drawmode()
        drmode.print_obj()


#
# main test
#
suit0   = unittest.TestLoader().loadTestsFromTestCase(TestDrawMode)
alltest = unittest.TestSuite([suit0])
unittest.TextTestRunner(verbosity=2).run(alltest)
