#!/usr/bin/env python
#
# Qt related utility
#

import math
import numpy
from PyQt4  import QtCore

#
# QPoint to numpy float array
#
# \param[in]  _qpoint2d point in a window coordinate (QPoint, int)
# \return numpy array float
def QPoint2numpy(_qpoint2d):
    pos2d = numpy.array([float(_qpoint2d.x()), float(_qpoint2d.y())])
    return pos2d

