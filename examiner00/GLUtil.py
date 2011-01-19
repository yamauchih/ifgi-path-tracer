#!/usr/bin/env python
#
# GL utility functions
#

"""IFGI OpenGL utility functions"""

import numpy

from OpenGL import GL
from OpenGL import GLU

#
# OpenGL: draw axis aligned box
#
# \param[in] _aabox_min axis aligned box min point
# \param[in] _aabox_max axis aligned box max point
#
def draw_axis_alighed_box(_aabox_min, _aabox_max):
    # check min max validity
    assert((_aabox_min <= _aabox_max).all() == True)

    # print 'DEBUG: min: ' + str(_aabox_min) + ', max:' + str(_aabox_max)

    vtxpt = numpy.array([[_aabox_min[0], _aabox_min[1], _aabox_min[2]], # vtxpt[0]
                         [_aabox_max[0], _aabox_min[1], _aabox_min[2]], # vtxpt[1]
                         [_aabox_min[0], _aabox_max[1], _aabox_min[2]], # vtxpt[2]
                         [_aabox_max[0], _aabox_max[1], _aabox_min[2]], # vtxpt[3]
                         [_aabox_min[0], _aabox_min[1], _aabox_max[2]], # vtxpt[4]
                         [_aabox_max[0], _aabox_min[1], _aabox_max[2]], # vtxpt[5]
                         [_aabox_min[0], _aabox_max[1], _aabox_max[2]], # vtxpt[6]
                         [_aabox_max[0], _aabox_max[1], _aabox_max[2]]] # vtxpt[7]
                        )
    edgelist = numpy.array([
            [0, 1], [1, 3], [3, 2], [2, 0], # front side rectangle
            [4, 5], [5, 7], [7, 6], [6, 4], # back  side rectangle
            [0, 4], [1, 5], [2, 6], [3, 7]] # front side and back side connecting edges
                        )
    GL.glBegin(GL.GL_LINES)
    for edge in edgelist:
        GL.glVertex3dv(vtxpt[edge[0]])
        GL.glVertex3dv(vtxpt[edge[1]])
    GL.glEnd()

#
# main test
#
# if __name__ == '__main__':
