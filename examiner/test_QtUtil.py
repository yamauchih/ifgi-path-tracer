#!/usr/bin/env python
#
# Copyright (C) 2010-2011 Yamauchi, Hitoshi
#

"""test QtUtil module"""

import unittest
import numpy
import QtUtil
from PySide import QtCore

class TestQtUtil(unittest.TestCase):
    """test: QtUtil"""

    def test_QPoint2numpy(self):
        """test mapToSphere function"""
        test_numlist = [[1,2], [-5,6]]

        for pos in test_numlist:
            qpos = QtCore.QPoint(pos[0], pos[1])
            npos = QtUtil.QPoint2numpy(qpos)
            assert(npos[0] == float(pos[0]))
            assert(npos[1] == float(pos[1]))

    def test_key_modifier(self):
        """test key modifiers"""

        ctrlmod  = QtCore.Qt.KeyboardModifiers(QtCore.Qt.ControlModifier)
        altmod   = QtCore.Qt.KeyboardModifiers(QtCore.Qt.AltModifier)
        shiftmod = QtCore.Qt.KeyboardModifiers(QtCore.Qt.ShiftModifier)
        nomod    = QtCore.Qt.KeyboardModifiers(QtCore.Qt.NoModifier)

        assert(    QtUtil.in_key_modifier(ctrlmod, QtCore.Qt.ControlModifier))
        assert(not QtUtil.in_key_modifier(altmod,  QtCore.Qt.ControlModifier))

        allmod = ctrlmod | altmod | shiftmod

        assert(    QtUtil.in_key_modifier(allmod, QtCore.Qt.ControlModifier))
        assert(    QtUtil.in_key_modifier(allmod, QtCore.Qt.AltModifier))
        assert(    QtUtil.in_key_modifier(allmod, QtCore.Qt.ShiftModifier))
        assert(not QtUtil.in_key_modifier(allmod, QtCore.Qt.NoModifier))
        assert(    QtUtil.in_key_modifier(nomod,  QtCore.Qt.NoModifier))
        assert(not QtUtil.in_key_modifier(nomod,  QtCore.Qt.AltModifier))

        assert(QtUtil.get_key_modifier_string(ctrlmod)  == 'Ctrl+')
        assert(QtUtil.get_key_modifier_string(altmod)   == 'Alt+')
        assert(QtUtil.get_key_modifier_string(shiftmod) == 'Shift+')
        assert(QtUtil.get_key_modifier_string(allmod)   == 'Ctrl+Alt+Shift+')

#
# main test
#
suit0   = unittest.TestLoader().loadTestsFromTestCase(TestQtUtil)
alltest = unittest.TestSuite([suit0])
unittest.TextTestRunner(verbosity=2).run(alltest)
