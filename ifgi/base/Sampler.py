#!/usr/bin/env python
#
# Copyright (C) 2010-2011 Yamauchi, Hitoshi
#
"""ifgi sampler
\file
\brief samplers: stratified sampler, QMC (maybe), ..."""

import numpy

# Logger
class StratifiedRegularSampler(object):
    """a simple stratified regular sampler.
    """

    # default constructor
    def __init__(self):
        self._xstart = 0
        self._xend   = 0
        self._ystart = -1
        self._yend   = -1
        self._xsize  = 0
        self._ysize  = 0
        self._sample_loc_x = numpy.zeros( (0, 0) )
        self._sample_loc_y = numpy.zeros( (0, 0) )

    # compute sample
    def compute_sample(self, _xstart, _xend, _ystart, _yend):
        """compute samples. Allocate memory.

        we can access pixel index [_xstart, _xend], [_ystart, _yend]

        \param[in] _xstart start of pixel x
        \param[in] _xend   end   of pixel x (inclusive)
        \param[in] _ystart start of pixel y
        \param[in] _yend   end   of pixel y (inclusive)
        """
        assert(_xstart <= _xend)
        assert(_ystart <= _yend)

        self._xstart = _xstart
        self._xend   = _xend
        self._ystart = _ystart
        self._yend   = _yend
        self._xsize  = self._xend - self._xstart + 1
        self._ysize  = self._yend - self._ystart + 1
        if(self._sample_loc_x.shape != ( (self._xsize, self._ysize) )):
            # resize
            print 'resize the sample location from ' + str(self._sample_loc_x.shape) +\
                ' to ' + str((self._xsize, self._ysize) )
            self._sample_loc_x = numpy.zeros( (self._xsize, self._ysize) )
            self._sample_loc_y = numpy.zeros( (self._xsize, self._ysize) )

        for x in xrange(0, self._xsize, 1):
            for y in xrange(0, self._ysize, 1):
                self._sample_loc_x[x,y] = x + 0.5
                self._sample_loc_y[x,y] = y + 0.5

    # get sample location x
    def get_sample_x(self, _xidx, _yidx):
        """get the sample location x from the pixel index."""
        return self._sample_loc_x[_xidx,_yidx]

    # get sample location y
    def get_sample_y(self, _xidx, _yidx):
        """get the sample location y from the pixel index."""
        return self._sample_loc_y[_xidx,_yidx]





#
# main test ... test_ObjReader
#
# if __name__ == '__main__':
#     objreader = ObjReader()
#     objreader.read('../sampledata/one_tri.obj')
#
