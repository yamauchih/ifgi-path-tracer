#!/usr/bin/env python
#
# test for Drawmode
#

"""test IFGI Drawmode"""

import unittest
import DrawMode

class TestDrawMode(unittest.TestCase):

    def test_drawmode0(self):
        drmode = DrawMode.DrawModeList()


#
# main test
#
suit0   = unittest.TestLoader().loadTestsFromTestCase(TestDrawMode)
alltest = unittest.TestSuite([suit0])
unittest.TextTestRunner(verbosity=2).run(alltest)
