#!/usr/bin/env python

"""IFGI Film (frame buffer)
\file
\brief scene element film (A camera has this.)
"""

# import sys
# import math
import numpy
# import Ray

# # Film class: interface
# class FilmIF(object):
#     """film (frame buffer) interface"""

#     # constructor
#     def __init__(self):
#         """constructor.
#         """
#         pass

#     # class name
#     def get_classname(self):
#         """get class name. interface method.
#         \return class name
#         """
#         assert 0, "get_classname must be implemented in a derived class."
#         return None

#     # buffer name
#     def get_buffername(self):
#         """get buffer name (buffer instance name).
#         \return buffer name
#         """
#         assert 0, "get_buffername must be implemented in a derived class."
#         return None


# Image Film class
class ImageFilm(object):
    """image film (frame buffer)"""

    # constructor
    def __init__(self, _xres, _yres, _zres, _buffername):
        """constructor.
        \param[in] _xres  x resolution.
        \param[in] _yres  y resolution.
        \param[in] _zres z resolution.
        \param[in] _buffername buffer name (RGBA, Z, ...)
        """
        super(ImageFilm, self).__init__()
        self.__x_resolution = _xres
        self.__y_resolution = _yres
        self.__z_resolution = _zres
        assert(self.__x_resolution > 0)
        assert(self.__y_resolution > 0)
        assert(self.__z_resolution > 0)

        self.__buffername = _buffername

        # allocate buffer
        self.__framebuffer = zeros(self.__x_resolution,
                                   self.__y_resolution,
                                   self.__z_resolution)

    # class name
    def get_classname(self):
        """get class name. interface method..
        \return class name
        """
        return 'ImageFilm'

    # buffer name
    def get_buffername(self):
        """get buffer name (buffer instance name).
        \return buffer name
        """
        return self.__buffername




#
# main test
#
#if __name__ == '__main__':
#    pass
