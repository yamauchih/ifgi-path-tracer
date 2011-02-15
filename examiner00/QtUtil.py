#!/usr/bin/env python
"""Qt related utility.
\file
\brief PyQt related utilities
"""

import math
import numpy
from PyQt4  import QtCore

# QPoint to numpy float array
def QPoint2numpy(_qpoint2d):
    """QPoint to numpy float array.

    \param[in]  _qpoint2d point in a window coordinate (QPoint, int)
    \return numpy array float"""

    pos2d = numpy.array([float(_qpoint2d.x()), float(_qpoint2d.y())])
    return pos2d


# is key modifier included?
def in_key_modifier(_modifier_state, _modifier_mask):
    """Does _modifier_state include _modifier_mask key?

    Check the _modifier_state include _modifier_mask or not.

    \param[in] _modifier_state qt keyevent ev.modifiers()
    \param[in] _modifier_mask modifier
    mask. e.g. QtCore.Qt.ControlModifier
    \return True when _modifier_mask is included.
    """

    assert(isinstance(_modifier_state, QtCore.Qt.KeyboardModifiers))

    # no modifier is a special case
    if (_modifier_mask == QtCore.Qt.NoModifier):
        if (_modifier_state == QtCore.Qt.NoModifier):
            return True
        else:
            return False

    # depends on operator'&' of Qt.KeyboardModifiers
    if (_modifier_state & _modifier_mask == _modifier_mask):
        return True

    return False



# get key modifier string
def get_key_modifier_string(_mstate):
    """get key modifier string.

    Modifiers are object and '&' is just an operator, therefore,
    we can not use:
    if (_mstate & QtCore.Qt.ControlModifier != 0):
    # This doesn't tell control modifier or not. '&' might not
    # returns integer.

    \param[in] modifier qt keyevent ev.modifiers()
    \return modifier strings
    """

    modstr = ''
    if (in_key_modifier(_mstate, QtCore.Qt.ControlModifier)):
        modstr += 'Ctrl+'

    if (in_key_modifier(_mstate, QtCore.Qt.AltModifier)):
        modstr += 'Alt+'

    if (in_key_modifier(_mstate, QtCore.Qt.ShiftModifier)):
        modstr += 'Shift+'

    if (in_key_modifier(_mstate, QtCore.Qt.NoModifier)):
        modstr = 'NoModifier'

    return modstr

