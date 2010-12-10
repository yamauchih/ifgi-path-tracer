#!/usr/bin/env python
#
# Draw mode
#

"""IFGI Drawmode"""

import math
import numpy
import enum

#
# Projection Mode
#
# ProjectionMode = enum.Enum(['Perspective', 'Orthographic'])


#
# Draw mode item
#
class DrawModeItem(object):
    # constructor
    # \param[in] _name   mode name. should be unique
    # \param[in] _bitmap mode bitmap. should be unique
    # \param[in] _is_available boolean. the mode is visible to GUI or
    # not
    def __init__(self, _name, _bitmap, _is_available):
        self.mode_name    = _name
        self.mode_bitmap  = _bitmap
        self.is_avairable = _is_available

    # get mode name
    # \return mode name
    def get_name(self):
        return self.mode_name

    # get mode bitmap
    # \return mode bitmap (2^p)
    def get_bitmap(self):
        return self.mode_bitmap

#
# Draw mode list
#
class DrawModeList(object):
    # default constructor
    def __init__(self):
        self.mode_item_list       = []
        self.mode_name_bitmap_map = {}
        self.add_basic_draw_mode()

    # find draw mode
    # \param[in] _draw_mode_name draw mode name
    def find_draw_mode(self, _draw_mode_name):
        # NIN
        print 'NIN: find draw mode'

    # add draw mode
    # \param[in] _draw_mode_item a draw mode
    def add_draw_mode(self, _draw_mode_item):
        # NIN
        # check the draw mode item is unique, bitmap is power of two
        print 'NIN: add draw mode, no validity check'
        
        self.mode_item_list.append(_draw_mode_item)
        self.mode_name_bitmap_map[_draw_mode_item.mode_name] = \
            _draw_mode_item.mode_bitmap

    # add basic draw mode
    def add_basic_draw_mode(self):
        self.add_draw_mode(DrawModeItem('Points',          0x0001, True))
        self.add_draw_mode(DrawModeItem('Wireframe',       0x0002, True))
        self.add_draw_mode(DrawModeItem('Hiddenline',      0x0004, True))
        self.add_draw_mode(DrawModeItem('Solid Basecolor', 0x0008, True))
        self.add_draw_mode(DrawModeItem('Solid Flat',      0x0010, True))
        self.add_draw_mode(DrawModeItem('Solid Gouraud',   0x0020, True))
        self.add_draw_mode(DrawModeItem('Solid Texture',   0x0040, True))

        # internal use only
        self.add_draw_mode(DrawModeItem('Picking',         0x0080, False))
