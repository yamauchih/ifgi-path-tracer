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

    # get availability/visibility
    # \return mode availability/visibility for popup menu
    def is_avairable(self):
        return self.is_avairable

    # print this object
    def print_obj(self):
        print ('DrawModeItem: [' + self.mode_name + ']\t' + str(self.mode_bitmap) +
               '\t' + str(self.is_avairable))
        

#
# Draw mode list
#
class DrawModeList(object):
    # default constructor
    def __init__(self):
        self.mode_item_list = []
        self.mode_item_map  = {}


    # find draw mode
    # \param[in] _draw_mode_name draw mode name
    # \return a DrawModeItem if found, otherwise None.
    def find_draw_mode(self, _draw_mode_name):
        if (_draw_mode_name in self.mode_item_map):
            return self.mode_item_map[_draw_mode_name]
        else:
            return None

    # add draw mode
    # \param[in] _draw_mode_item a draw mode
    def add_draw_mode(self, _draw_mode_item):
        # check the draw mode item is unique, bitmap is power of two
        if (self.find_draw_mode(_draw_mode_item.mode_name) != None):
            raise StandardError ('DrawModeList: ' + _draw_mode_item.mode_name +
                                 ' has already submitted.')

        self.mode_item_list.append(_draw_mode_item)
        self.mode_item_map[_draw_mode_item.mode_name] = _draw_mode_item
        print 'DEBUG: added ' + _draw_mode_item.mode_name

    # add basic draw mode
    def add_basic_draw_mode(self):
        self.add_draw_mode(DrawModeItem('BBox',            0x0001, True))
        self.add_draw_mode(DrawModeItem('Points',          0x0002, True))
        self.add_draw_mode(DrawModeItem('Wireframe',       0x0004, True))
        self.add_draw_mode(DrawModeItem('Hiddenline',      0x0008, True))
        self.add_draw_mode(DrawModeItem('Solid Basecolor', 0x0010, True))
        self.add_draw_mode(DrawModeItem('Solid Flat',      0x0020, True))
        self.add_draw_mode(DrawModeItem('Solid Gouraud',   0x0040, True))
        self.add_draw_mode(DrawModeItem('Solid Texture',   0x0080, True))
        # internal use only
        self.add_draw_mode(DrawModeItem('Picking',         0x0100, False))


    # or draw mode
    #
    # \param[in] _other_drawmode other draw mode. This draw mode is
    # or-ed and updated.
    def or_drawmode(self, _other_drawmode):
        if _other_drawmode == None:
            print 'DrawModeList: No draw mode list'
            return

        print 'DrawModeList: Found draw mode list'
        for mi in _other_drawmode.mode_item_list:
            if (not find_draw_mode(mi)):
                self.add_draw_mode(mi)

    # print draw mode list
    def print_obj(self):
        for dmitem in self.mode_item_list:
            dmitem.print_obj()
