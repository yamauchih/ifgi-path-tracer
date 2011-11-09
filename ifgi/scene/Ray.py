#!/usr/bin/env python
#
# Copyright 2011 (C) Yamauchi, Hitoshi
#
# Ray

"""IFGI Ray
\file
\brief a ray
"""

#import math
import numpy

# Ray class
class Ray(object):
    """a Ray
    """

    # default constructor
    def __init__(self, _origin, _dir, _min_t, _max_t):
        """default constructor.
        \param[in] _origin ray origin
        \param[in] _dir    ray direction
        \param[in] _min_t ray minimal distance (less than this
        distance doesn't intersect)
        \param[in] _max_t ray maximal distance (more than this
        distance doesn't intersect)
        """
        self.__origin = _origin
        self.__dir    = _dir
        self.__min_t  = _min_t
        self.__max_t  = _max_t

        self.path_length = 0
        self.reflectance = numpy.array([1.0, 1.0, 1.0, 1.0])
        self.intensity   = numpy.array([0.0, 0.0, 0.0, 1.0])

    # class name
    def get_classname(self):
        """get class name
        \return class name
        """
        return 'Ray'

    # get origin
    def get_origin(self):
        """get the ray origin.
        \return ray origin.
        """
        return self.__origin

    # get ray dir
    def get_dir(self):
        """get the ray direction vector.
        \return ray dir.
        """
        return self.__dir

    # get min distance
    def get_min_t(self):
        """get minimal ray distance.
        \return ray min_t.
        """
        return self.__min_t

    # get ray dir
    def get_max_t(self):
        """get maximal ray distance.
        \return ray max_t.
        """
        return self.__max_t

    # string representation
    def __str__(self):
        return 'orig: '+ str(self.__origin) + ' dir: ' + str(self.__dir) +\
            ' range: [' + str(self.__min_t)  + ' ' + str(self.__max_t) + ']'



#
# main test
#
# if __name__ == '__main__':
#     pass
