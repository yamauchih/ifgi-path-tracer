#!/usr/bin/env python
#
# Copyright 2011 (C) Yamauchi, Hitoshi
#

"""IFGI Film (frame buffer)
\file
\brief scene element film (A camera has this.)
"""

from PIL import Image
import numpy

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
    def __init__(self, _res, _buffername):
        """constructor.
        \param[in] _res  resolution tuple, (x, y, z) resolution.
        \param[in] _buffername buffer name (RGBA, Z, ...)
        """
        super(ImageFilm, self).__init__()

        assert(len(_res) == 3)
        self.__resolution = _res
        assert(self.__resolution[0] > 0)
        assert(self.__resolution[1] > 0)
        assert(self.__resolution[2] > 0)

        self.__buffername = _buffername

        # allocate buffer: zeros((shepe_touple), type, ...)
        self.__framebuffer = numpy.zeros((self.__resolution[0],
                                          self.__resolution[1],
                                          self.__resolution[2]))

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

    # get resolution
    def get_resolution(self):
        """get the film resolution.
        \return resolution (tuple), e.g., (1024, 800, 3) = image size
        1024x800, 3 channels.
        """
        return self.__resolution

    # get color
    def get_color(self, _pos):
        """get color at pixel _pos in numpy array.

        The size of color tuple is depends on self.__resolution[2] (=
        depth).

        \param[in] _pos position of the pixel (x,y) or (x,y,z)
        \return color (numpy.array for (x,y), scalar for (x,y,z))
        """
        return self.__framebuffer[_pos]

    # put color at a pixel
    def put_color(self, _pos, _color):
        """put a color at pixel _pos.

        \param[in] _pos   position as pixel (tuple), e.g., (80, 120)
        \param[in] _color pixel color as numpy.array. e.g., [1.0, 0.0, 0.0, 1.0]
        """
        assert(((len(_pos) == 2) and (len(_color) == self.__resolution[2])) or
               ((len(_pos) == 3) and (len(_color) == 1)))
        self.__framebuffer[_pos] = _color


    # fill color
    def fill_color(self, _col):
        """fill color _col whole framebuffer.

        Fill the framebuffer with _col.

        \param[in] _col color to fill.
        """
        for x in xrange(0, self.__resolution[0], 1):
            for y in xrange(0, self.__resolution[1], 1):
                self.__framebuffer[(x, y)] = _col


    # save buffer as an image file
    def save_file(self, _filename):
        """save the buffer contents to a file.
        \param[in] _filename output file name
        """
        imgsize  = (self.__resolution[0], self.__resolution[1])
        print imgsize

        if(self.__resolution[2] == 1):
            # grayscale -> convert to RGB
            bg_white = (255, 255, 255)
            img = Image.new("RGB", imgsize, bg_white)

            for x in xrange(0, self.__resolution[0], 1):
                for y in xrange(0, self.__resolution[1], 1):
                    col = self.get_color(_pos)
                    # duplicate the channels
                    ucharcol = (255 * col[0], 255 * col[0], 255 * col[0])
                    img.putpixel((x, self.__resolution[1] - y - 1), ucharcol)

        elif(self.__resolution[2] == 3):
            # RGB
            bg_white = (255, 255, 255)
            img = Image.new("RGB", imgsize, bg_white)

            for x in xrange(0, self.__resolution[0], 1):
                for y in xrange(0, self.__resolution[1], 1):
                    col = self.get_color(_pos)
                    ucharcol = (255 * col[0], 255 * col[1], 255 * col[2])
                    img.putpixel((x, self.__resolution[1] - y - 1), ucharcol)

        elif(self.__resolution[2] == 4):
            # RGBA
            bg_white = (255, 255, 255, 255)
            img = Image.new("RGBA", imgsize, bg_white)

            for x in xrange(0, self.__resolution[0], 1):
                for y in xrange(0, self.__resolution[1], 1):
                    col = 255 * self.get_color((x, y))
                    ucharcol = (int(col[0]), int(col[1]), int(col[2]), int(col[3]))
                    img.putpixel((x, self.__resolution[1] - y - 1), ucharcol)
        else:
            raise StandardError, ('supported number of channels are 1, 3, and 4, only.')

        img.save(_filename)


    # human readable string
    def __str__(self):

        return '[name: %s, resolution: (%d %d %d)]' \
            % (self.__buffername,  self.__resolution[0], \
                   self.__resolution[1], self.__resolution[2])


#
# main test
#
#if __name__ == '__main__':
#    pass
