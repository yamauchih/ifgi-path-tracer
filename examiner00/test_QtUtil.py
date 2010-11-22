#!/usr/bin/env python
#
# test for QtUtil module
#

"""test QtUtil module"""

import unittest
import numpy
import QtUtil
from PyQt4  import QtCore

class TestQtUtil(unittest.TestCase):
    # test mapToSphere function
    def test_QPoint2numpy(self):
        test_numlist = [[1,2], [-5,6]]

        for pos in test_numlist:
            qpos = QtCore.QPoint(pos[0], pos[1])
            npos = QtUtil.QPoint2numpy(qpos)
            assert(npos[0] == float(pos[0]))
            assert(npos[1] == float(pos[1]))



#
# main test
#
suit0   = unittest.TestLoader().loadTestsFromTestCase(TestQtUtil)
alltest = unittest.TestSuite([suit0])
unittest.TextTestRunner(verbosity=2).run(alltest)
