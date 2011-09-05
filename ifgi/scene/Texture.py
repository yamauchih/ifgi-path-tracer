#!/usr/bin/env python
#
# Copyright 2010-2011 (C) Yamauchi, Hitoshi
#
"""IFGI Texture
\file
\brief scene element texture
"""

import sys
import math
import numpy


class Texture(object):
    """Texture class: interface"""

    def __init__(self):
        """default constructor"""
        pass


    def get_classname(self):
        """get class name. interface method. (public).
        \return class name
        """
        assert 0, "get_classname must be implemented in a derived class."
        return None


    def value(self, _uv, _point):
        """texture value.

        \param[in] _uv    texture uv coordinate (if surface)
        \param[in] _point texture point in 3d (if solid)
        \return texture color value
        """
        assert 0, "value must be implemented in a derived class."
        return None


class ConstantColorTexture(Texture):
    """Constant color texture"""

    def __init__(self, _color):
        """default constructor

        \param[in] _color constant color float4
        """
        self.__color = _color


    def get_classname(self):
        """get class name. interface method. (public).
        \return class name
        """
        return 'ConstantColorTexture'


    def value(self, _uv, _point):
        """texture value.

        \param[in] _uv    texture uv coordinate (if surface)
        \param[in] _point texture point in 3d (if solid)
        \return texture color value
        """
        return _color


class ImageTexture(object):
    """Image texture class"""

    def __init__(self, ):
        """default constructor"""
        pass


    def get_classname(self):
        """get class name. interface method. (public).
        \return class name
        """
        assert 0, "get_classname must be implemented in a derived class."
        return None


    def value(self, _uv, _point):
        """texture value.

        \param[in] _uv    texture uv coordinate (if surface)
        \param[in] _point texture point in 3d (if solid)
        \return texture color value
        """
        assert 0, "value must be implemented in a derived class."
        return None



#
# main test
#
#if __name__ == '__main__':
#    pass
