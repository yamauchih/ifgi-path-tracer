#!/usr/bin/env python
#
# Copyright (C) 2010-2011 Yamauchi, Hitoshi
#
"""ifgi sampler
\file
\brief samplers: stratified sampler, QMC (maybe), ..."""

import numpy, random, math, ifgimath

class StratifiedRegularSampler(object):
    """a simple stratified regular sampler.
    """

    def __init__(self):
        """default constructor"""
        self._xstart = 0
        self._xend   = 0
        self._ystart = -1
        self._yend   = -1
        self._xsize  = 0
        self._ysize  = 0
        self._sample_loc_x = numpy.zeros( (0, 0) )
        self._sample_loc_y = numpy.zeros( (0, 0) )


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


class UnitDiskUniformSampler(object):
    """Generate uniform sampling on a unit disk.
    Uniform respect to area
    """
    
    def __init__(self):
        """default constructor"""
        pass


    def get_sample(self):
        """get sample point on an unit disk
        \return a touple (x,y)"""
        u1 = random.random()
        u2 = random.random()        
        r  = math.sqrt(u1)
        t  = 2.0 * math.pi * u2
        x  = r * math.cos(t)
        y  = r * math.sin(t)
        return (x, y)



class UnitHemisphereUniformSampler(object):
    """Generate uniform sampling on a hemisphere.
    Using UnitDiskUniformSampler.
    """

    def __init__(self):
        """default constructor"""
        self.__udus = UnitDiskUniformSampler()

    def get_sample(self):
        """get sample point on a unit hemisphere
        \return numpy.array([x,y,z])"""

        # p = [-1,1]x[-1,1]
        p = self.__udus.get_sample()

        x = p[0]
        y = p[1]
        z = math.sqrt(numpy.max([0, 1 - x * x - y * y]))
        v = numpy.array([x, y, z])
        r = ifgimath.normalize_vec(v)

        return v

        

#
# main test
#
# if __name__ == '__main__':
#
