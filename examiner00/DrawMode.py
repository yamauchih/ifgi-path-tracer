#!/usr/bin/env python
#
# Copyright (C) 2010-2011 Yamauchi, Hitoshi
#
"""OpenGL Drawmode.
\file
\brief draw mode (mainly for OpenGL)
"""

import math
import numpy
from ifgi.base import enum

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
        """constructor. (public)
        \param[in] _name   mode name. should be unique
        \param[in] _bitmap mode bitmap. should be unique
        \param[in] _is_available boolean. the mode is visible to GUI or
        not"""

        self.__mode_name    = _name
        self.__mode_bitmap  = _bitmap
        self.__is_avairable = _is_available

    # get mode name
    def get_name(self):
        """get mode name. (public)
        \return mode name"""
        return self.__mode_name

    # get mode bitmap
    def get_bitmap(self):
        """get mode bitmap. (public)
        # \return mode bitmap (2^p)"""
        return self.__mode_bitmap

    # get availability/visibility
    def is_avairable(self):
        """get availability/visibility. (public)
        \return mode availability/visibility for popup menu"""
        return self.__is_avairable

    # print this object
    def print_obj(self):
        """print this object. (public)"""
        print ('DrawModeItem: [' + self.__mode_name + ']\t' +
               str(self.__mode_bitmap) + '\t' + str(self.__is_avairable))

# Draw mode list
class DrawModeList(object):
    """Draw mode list.

    DrawModeItem container/lookup.
    \see DrawModeItem"""

    # basic drawmode bitmap
    DM_GlobalMode      = 0xffffffff
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

    # in order draw mode list
    DM_Drawmode_bitmap_key_list = [
        ## bounding box
        DM_BBox,
        ## point
        DM_Points,
        ## wireframe
        DM_Wireframe,
        ## hidden line
        DM_Hiddenline,
        ## solid base color
        DM_Solid_Basecolor,
        ## solid flat shading
        DM_Solid_Flat,
        ## Gouraud shading
        DM_Solid_Gouraud,
        ## Texture mapping
        DM_Solid_Texture,
        ## for Picking
        DM_Picking
        ]

    # lookup table for name. Unfortunately, keys() doesn't return in
    # order, use DM_Drawmode_bitmap_key_list for iterate keys.
    DM_Drawmode_bitmap_dict = {
        DM_BBox:            'BBox',
        DM_Points:          'Points',
        DM_Wireframe:       'Wireframe',
        DM_Hiddenline:      'Hiddenline',
        DM_Solid_Basecolor: 'Solid_basecolor',
        DM_Solid_Flat:      'Solid_Flat',
        DM_Solid_Gouraud:   'Solid_Gouraud',
        DM_Solid_Texture:   'Solid_Texture',
        DM_Picking:         'Picking'
        }


    # default constructor
    def __init__(self):
        """default constructor. (public)"""
        self.__mode_item_list = []
        self.__mode_item_map  = {}

    # get mode item list
    def get_mode_item_list(self):
        """get mode item list. (public)
        \return drawmode item list
        """
        return self.__mode_item_list

    # find draw mode
    def find_drawmode(self, _drawmode_name):
        """find draw mode. (public)
        \param[in] _drawmode_name draw mode name
        \return a DrawModeItem if found, otherwise None."""

        if (_drawmode_name in self.__mode_item_map):
            return self.__mode_item_map[_drawmode_name]
        else:
            return None

    # find drawmode_bitmap in this list?
    def find_drawmode_bitmap(self, _drawmode_bitmap):
        """find drawmode_bitmap in this list? (public)
        \param[in] _drawmode_bitmap search _drawmode_bitmap in the list
        \return true if _drawmode_bitmap is found in the list"""

        for dm in self.__mode_item_list:
            if (dm.get_bitmap() == _drawmode_bitmap):
                return dm
        return None

    # add draw mode
    def add_drawmode(self, _drawmode_item):
        """add draw mode. (public)
        \param[in] _drawmode_item a draw mode"""

        # check the draw mode item is unique, bitmap is power of two
        if (self.find_drawmode(_drawmode_item.get_name()) != None):
            raise StandardError ('DrawModeList: ' + _drawmode_item.get_name() +
                                 ' has already submitted.')

        self.__mode_item_list.append(_drawmode_item)
        self.__mode_item_map[_drawmode_item.get_name()] = _drawmode_item
        # print 'DEBUG: added ' + _drawmode_item.mode_name

    # add basic draw mode
    def add_basic_drawmode(self):
        """add basic draw mode. (public)
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

    # get mode item list
    def get_mode_item_list(self):
        """get mode item list. (public)
        """
        return self.__mode_item_list

    # or draw mode
    def or_drawmode(self, _other_drawmode):
        """or draw mode. (public)
        \param[in] _other_drawmode other draw mode. This draw mode is
        or-ed and updated."""

        if _other_drawmode == None:
            print 'DrawModeList: No draw mode list'
            return

        print 'DrawModeList: Found draw mode list'
        for mi in _other_drawmode.get_mode_item_list():
            if (not self.find_drawmode(mi)):
                self.add_drawmode(mi)

    # print draw mode list for debug
    def print_obj(self):
        """print draw mode list for debug. (public)"""
        for dmitem in self.__mode_item_list:
            dmitem.print_obj()


# get drawmode string
def get_drawmode_string(_drawmode):
    """get drawmode string representation.
    \return string representation of drawmode."""

    if (_drawmode == DrawModeList.DM_GlobalMode):
        return 'Global'

    retstr = ''
    for mode in DrawModeList.DM_Drawmode_bitmap_key_list:
        if ((_drawmode & mode) != 0):
            if (len(retstr) > 0):
                retstr += '+'
            retstr += DrawModeList.DM_Drawmode_bitmap_dict[mode]

    if (retstr == ''):
        raise StandardError('illegal drawmode [' + str(_drawmode) + ']')

    return retstr


