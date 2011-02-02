#!/usr/bin/env python
"""OpenGL Drawmode.
\file
\brief draw mode (mainly for OpenGL)
"""

import math
import numpy
import enum

#
# Projection Mode
#
# ProjectionMode = enum.Enum(['Perspective', 'Orthographic'])


# Draw mode item
class DrawModeItem(object):
    """Draw mode item.
    a draw mode"""

    # constructor
    def __init__(self, _name, _bitmap, _is_available):
        """constructor.
        \param[in] _name   mode name. should be unique
        \param[in] _bitmap mode bitmap. should be unique
        \param[in] _is_available boolean. the mode is visible to GUI or
        not"""

        self.mode_name    = _name
        self.mode_bitmap  = _bitmap
        self.is_avairable = _is_available

    # get mode name
    def get_name(self):
        """get mode name.
        \return mode name"""

        return self.mode_name

    # get mode bitmap
    def get_bitmap(self):
        """get mode bitmap.
        # \return mode bitmap (2^p)"""

        return self.mode_bitmap

    # get availability/visibility
    def is_avairable(self):
        """get availability/visibility
        \return mode availability/visibility for popup menu"""
        return self.is_avairable

    # print this object
    def print_obj(self):
        """print this object"""
        print ('DrawModeItem: [' + self.mode_name + ']\t' +
               str(self.mode_bitmap) + '\t' + str(self.is_avairable))

# Draw mode list
class DrawModeList(object):
    """Draw mode list.

    DrawModeItem container/lookup.
    \see DrawModeItem"""

    ## basic drawmode bitmap
    DM_BBox            = 0x0001
    DM_Points          = 0x0002
    DM_Wireframe       = 0x0004
    DM_Hiddenline      = 0x0008
    DM_Solid_Basecolor = 0x0010
    DM_Solid_Flat      = 0x0020
    DM_Solid_Gouraud   = 0x0040
    DM_Solid_Texture   = 0x0080
    DM_Picking         = 0x0100
    DM_USER00          = 0x0200

    # default constructor
    def __init__(self):
        """default constructor"""
        self.mode_item_list = []
        self.mode_item_map  = {}


    # find draw mode
    def find_drawmode(self, _drawmode_name):
        """find draw mode.
        \param[in] _drawmode_name draw mode name
        \return a DrawModeItem if found, otherwise None."""

        if (_drawmode_name in self.mode_item_map):
            return self.mode_item_map[_drawmode_name]
        else:
            return None

    # find drawmode_bitmap in this list?
    def find_drawmode_bitmap(self, _drawmode_bitmap):
        """find drawmode_bitmap in this list?
        \param[in] _drawmode_bitmap search _drawmode_bitmap in the list
        \return true if _drawmode_bitmap is found in the list"""

        for dm in self.mode_item_list:
            if (dm.get_bitmap() == _drawmode_bitmap):
                return dm
        return None

    # add draw mode
    def add_drawmode(self, _drawmode_item):
        """add draw mode
        \param[in] _drawmode_item a draw mode"""

        # check the draw mode item is unique, bitmap is power of two
        if (self.find_drawmode(_drawmode_item.mode_name) != None):
            raise StandardError ('DrawModeList: ' + _drawmode_item.mode_name +
                                 ' has already submitted.')

        self.mode_item_list.append(_drawmode_item)
        self.mode_item_map[_drawmode_item.mode_name] = _drawmode_item
        # print 'DEBUG: added ' + _drawmode_item.mode_name

    # add basic draw mode
    def add_basic_drawmode(self):
        """add basic draw mode.
        convenience method"""

        self.add_drawmode(DrawModeItem('BBox',
                                       DrawModeList.DM_BBox,            True))
        self.add_drawmode(DrawModeItem('Points',
                                       DrawModeList.DM_Points,          True))
        self.add_drawmode(DrawModeItem('Wireframe',
                                       DrawModeList.DM_Wireframe,       True))
        self.add_drawmode(DrawModeItem('Hiddenline',
                                       DrawModeList.DM_Hiddenline,      True))
        self.add_drawmode(DrawModeItem('Solid Basecolor',
                                       DrawModeList.DM_Solid_Basecolor, True))
        self.add_drawmode(DrawModeItem('Solid Flat',
                                       DrawModeList.DM_Solid_Flat,      True))
        self.add_drawmode(DrawModeItem('Solid Gouraud',
                                       DrawModeList.DM_Solid_Gouraud,   True))
        self.add_drawmode(DrawModeItem('Solid Texture',
                                       DrawModeList.DM_Solid_Texture,   True))
        # internal use only
        self.add_drawmode(DrawModeItem('Picking',
                                       DrawModeList.DM_Picking,         False))

    # or draw mode
    def or_drawmode(self, _other_drawmode):
        """or draw mode.
        \param[in] _other_drawmode other draw mode. This draw mode is
        or-ed and updated."""

        if _other_drawmode == None:
            print 'DrawModeList: No draw mode list'
            return

        print 'DrawModeList: Found draw mode list'
        for mi in _other_drawmode.mode_item_list:
            if (not self.find_drawmode(mi)):
                self.add_drawmode(mi)

    # print draw mode list for debug
    def print_obj(self):
        """print draw mode list for debug"""
        for dmitem in self.mode_item_list:
            dmitem.print_obj()
