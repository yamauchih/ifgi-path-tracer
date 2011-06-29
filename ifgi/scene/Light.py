#!/usr/bin/env python
#
# Copyright 2011 (C) Yamauchi, Hitoshi
#
# PointLight
#

"""IFGI Light
\file
\brief Point light. non physical light
"""

# LightGroup
class LightGroup(object):
    """non physical light group.
    This is a dictionary of light.

    In a scene, one unique LightGroup exists. (Later this will be
    removed since path tracer does not need this.)
    """

    # default constructor
    def __init__(self, _name):
        """default constructor.
        \param[in] _name light group name
        """
        self.__name       = _name
        self.__light_dict = {}

    # class name
    def get_classname(self):
        """get class name
        \return class name
        """
        return 'LightGroup'

    # add a light
    def add_light(self, _light):
        """add a light to the dictionary.
        \return light list.
        """
        return self.__light_dict

    # get dict
    def get_dict(self):
        """get the light source dictionary.
        \return light source dictionary.
        """
        return self.__light_dict

    # string representation
    def __str__(self):
        retstr = 'LightGroup [' + self.__name + ']\n'
        for li in self.__light_dict.keys():
            retstr += self.__light_dict[li]

        return retstr


# PointLight class
class PointLight(object):
    """a point light. non-physical light.
    """

    # default constructor
    def __init__(self, _name, _pos, _intensity):
        """default constructor.
        \param[in] _name      the name of this light
        \param[in] _position  light position
        \param[in] _intensity light intensity
        """
        self.__name      = _name
        self.__pos       = _pos
        self.__intensity = _intensity

    # class name
    def get_classname(self):
        """get class name
        \return class name
        """
        return 'PointLight'

    # get name
    def get_light_name(self):
        """get the light name.
        \return light instance name.
        """
        return self.__name

    # get position
    def get_position(self):
        """get the light source position.
        \return light source position.
        """
        return self.__pos

    # get intensity
    def get_intensity(self):
        """get the light source intensity.
        \return light source intensity.
        """
        return self.__intensity

    # string representation
    def __str__(self):
        return 'Point light [' + self.__name + '] pos: '+ str(self.__pos) +\
            ' intensity: ' + str(self.__intensity)
#
# main test
#
# if __name__ == '__main__':
#     pass
