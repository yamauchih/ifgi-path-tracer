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
    # \param[in] _drawmode_name draw mode name
    # \return a DrawModeItem if found, otherwise None.
    def find_drawmode(self, _drawmode_name):
        if (_drawmode_name in self.mode_item_map):
            return self.mode_item_map[_drawmode_name]
        else:
            return None

    # find drawmode_bitmap in this list?
    #
    # \param[in] _drawmode_bitmap search _drawmode_bitmap in the list
    # \return true if _drawmode_bitmap is found in the list
    def find_drawmode_bitmap(self, _drawmode_bitmap):
        for dm in self.mode_item_list:
            if (dm.get_bitmap() == _drawmode_bitmap):
                return dm
        return None

    # add draw mode
    # \param[in] _drawmode_item a draw mode
    def add_drawmode(self, _drawmode_item):
        # check the draw mode item is unique, bitmap is power of two
        if (self.find_drawmode(_drawmode_item.mode_name) != None):
            raise StandardError ('DrawModeList: ' + _drawmode_item.mode_name +
                                 ' has already submitted.')

        self.mode_item_list.append(_drawmode_item)
        self.mode_item_map[_drawmode_item.mode_name] = _drawmode_item
        # print 'DEBUG: added ' + _drawmode_item.mode_name

    # add basic draw mode
    def add_basic_drawmode(self):
        self.add_drawmode(DrawModeItem('BBox',            0x0001, True))
        self.add_drawmode(DrawModeItem('Points',          0x0002, True))
        self.add_drawmode(DrawModeItem('Wireframe',       0x0004, True))
        self.add_drawmode(DrawModeItem('Hiddenline',      0x0008, True))
        self.add_drawmode(DrawModeItem('Solid Basecolor', 0x0010, True))
        self.add_drawmode(DrawModeItem('Solid Flat',      0x0020, True))
        self.add_drawmode(DrawModeItem('Solid Gouraud',   0x0040, True))
        self.add_drawmode(DrawModeItem('Solid Texture',   0x0080, True))
        # internal use only
        self.add_drawmode(DrawModeItem('Picking',         0x0100, False))


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
            if (not self.find_drawmode(mi)):
                self.add_drawmode(mi)

    # print draw mode list
    def print_obj(self):
        for dmitem in self.mode_item_list:
            dmitem.print_obj()
