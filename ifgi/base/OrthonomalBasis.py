#!/usr/bin/env python
#
# Copyright (C) 2010-2011 Yamauchi, Hitoshi
#
# Ref. Realistic Ray Tracing by Peter Shirley

"""ifgi orthonomal basis
\file
\brief orthonomal basis"""

import numpy

# OrthonomalBasis
class OrthonomalBasis(object):
    """orthonomal basis
    """

    ONB_EPSILON = 0.01
    Vec3_N = numpy.array([1, 0, 0])
    Vec3_M = numpy.array([0, 1, 0])

    # default constructor
    def __init__(self):
        """default constructor"""
        self.__U = None
        self.__V = None
        self.__W = None


    def set(self, _u, _v, _w):
        """set all the component of orthonomal basis.
        \param[in] _u u component
        \param[in] _v v component
        \param[in] _w w component
        """
        self.__U = _u
        self.__V = _v
        self.__W = _w


    def u(self):
        """get u component.
        \return u component."""
        return self.__U


    def v(self):
        """get v component.
        \return v component."""
        return self.__V


    def w(self):
        """get w component.
        \return w component."""
        return self.__W


    def normalize(self, _vec):
        """normali the vector
        \param[in] _vec input vector to normalize.
        length should be > ONB_EPSILON
        """
        len = numpy.linalg.norm(_vec)
        assert(len > OrthonomalBasis.ONB_EPSILON)
        return _vec / len


    def init_from_u(self, _u):
        """initialize from u component.
        \param[in] _u u component."""
        self.__U = self.normalize(_u)
        self.__V = numpy.cross(self.__U, OrthonomalBasis.Vec3_N)
        v_len = numpy.linalg.norm(self.__V)
        if v_len < OrthonomalBasis.ONB_EPSILON:
            self.__V = numpy.cross(self.__U, OrthonomalBasis.Vec3_M)
        self.__W = numpy.cross(self.__U, self.__V)


    def init_from_v(self, _v):
        """initialize from v component.
        \param[in] _v v component."""
        self.__V = self.normalize(_v)
        self.__U = numpy.cross(self.__V, OrthonomalBasis.Vec3_N)
        u_len = numpy.linalg.norm(self.__U)
        if u_len < OrthonomalBasis.ONB_EPSILON:
            self.__U = numpy.cross(self.__V, OrthonomalBasis.Vec3_M)
        self.__W = numpy.cross(self.__U, self.__V)


    def init_from_w(self, _w):
        """initialize from w component.
        \param[in] _w w component."""
        self.__W = self.normalize(_w)
        self.__U = numpy.cross(self.__W, OrthonomalBasis.Vec3_N)
        u_len = numpy.linalg.norm(self.__U)
        if u_len < OrthonomalBasis.ONB_EPSILON:
            self.__U = numpy.cross(self.__W, OrthonomalBasis.Vec3_M)
        self.__V = numpy.cross(self.__W, self.__U)


    def init_from_uv(self, _u, _v):
        """initialize from uv component.
        \param[in] _u u component.
        \param[in] _v v component."""
        self.__U = self.normalize(_u)
        self.__W = self.normalize(numpy.cross(_u, _v))
        self.__V = numpy.cross(self.__W, self.__U)


    def init_from_vw(self, _v, _w):
        """initialize from vw component.
        \param[in] _v v component.
        \param[in] _w w component."""
        self.__V = self.normalize(_v)
        self.__U = self.normalize(numpy.cross(_v, _w))
        self.__W = numpy.cross(self.__U, self.__V)


    def init_from_wu(self, _w, _u):
        """initialize from wu component.
        \param[in] _w w component.
        \param[in] _u u component."""
        self.__W = self.normalize(_w)
        self.__V = self.normalize(numpy.cross(_w, _u))
        self.__U = numpy.cross(self.__V, self.__W)



    def __str__(self):
        """human readable string"""
        s = ''
        if self.__U != None:
            s += '[%g %g %g]' % (self.u()[0], self.u()[1], self.u()[2])
        else:
            s += '[None]'
        if self.__V != None:
            s += '[%g %g %g]' % (self.v()[0], self.v()[1], self.v()[2])
        else:
            s += '[None]'
        if self.__W != None:
            s += '[%g %g %g]' % (self.w()[0], self.w()[1], self.w()[2])
        else:
            s += '[None]'

        return s



#
# main test ... test_ObjReader
#
# if __name__ == '__main__':
#     objreader = ObjReader()
#     objreader.read('../sampledata/one_tri.obj')
#
