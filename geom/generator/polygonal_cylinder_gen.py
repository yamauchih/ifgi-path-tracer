#!/usr/bin/env python
#
# Copyright 2011 (C) Yamauchi, Hitoshi
#
# Cylinder generator
#

"""Cylinder generator
\file
\brief generate a (polygonal) cylinder from two points.
"""

import math, numpy

class Polygonal_cylinder_gen(object):
    """Simple poltgonal cylinder generator.
    The normal of top and bottom polygons are always z+ (0,0,1)
    """

    def __init__(self):
        """default constructor.
        """
        zero_pos = numpy.array([0.0, 0.0, 0.0])
        self.__poly_normal   = numpy.array([0.0, 0.0, 1.0])
        self.__poly_tangent  = numpy.array([1.0, 0.0, 0.0])
        self.__poly_binomal  = numpy.array([0.0, 1.0, 0.0])

        self.__center = [zero_pos, zero_pos]
        self.__radius = [-1, -1]
        self.__n_gon = 0

        self.__vertex_list  = []
        self.__bt_face_list = []
        self.__side_face_list = []

        # switch to generate top and bottom triangles
        self.__is_gen_top_bottom_tris = True


    def clear(self):
        """clear the generated data"""
        self.__vertex_list  = []
        self.__bt_face_list = []
        self.__side_face_list = []


    def set_polygon(self, _top_or_bottom, _center, _radius):
        """set polygon parameter
        \param[in] _top_or_bottom 0 for top, 1 for bottom
        \param[in] _center polygon center position
        \param[in] _radius polygon radius
        """
        if ((_top_or_bottom != 0) and (_top_or_bottom != 1)):
            raise StandardError, ('_top_or_bottom must be 0 or 1, but ' +\
                                      str(_top_or_bottom))

        if (_radius <= 0):
            raise StandardError, ('_radius must be > 0, but ' + str(_radius))

        self.__center[_top_or_bottom] = _center
        self.__radius[_top_or_bottom] = _radius


    def set_generate_top_bottom_triangle(self, _is_gen):
        """set generate top and bottom triangles.
        \param[in] _is_gen generate top and bottom triangles when True
        """
        self.__is_gen_top_bottom_tris = _is_gen


    def set_n_gon(self, _n):
        """set n of n-gon.
        \param[in] _n top and bottom polygon n-gon
        """
        if (_n < 3):
            raise StandardError, ('_n be >= 3, but ' + str(_n))

        self.__n_gon = _n


    def gen_cylinder(self):
        """generate a cylinder
        """
        self.__is_able_to_gen()

        self.clear()
        self.__gen_top_bottom_vertex()
        if (self.__is_gen_top_bottom_tris):
            self.__gen_top_bottom_polygon()
        self.__gen_side_polygon()


    def export_obj(self, _objfname):
        """export obj file
        \param[in] _objfname exporting obj file name
        """
        if ((_objfname == None) or (len(_objfname) == 0)):
            raise StandardError, ('empty obj output file name.')

        objf = open(_objfname, 'w')

        # output mesh info
        vtx_count  = len(self.__vertex_list)
        face_count = len(self.__side_face_list) + len(self.__bt_face_list)
        if (vtx_count == 0):
            raise StandardError, ('no vertices.')
        objf.write('# ' + str(vtx_count) + ' ' + str(face_count) + ' 0\n')

        # vertices
        for v in self.__vertex_list:
            objf.write('v ' + str(v[0]) + ' ' + str(v[1]) + ' ' + str(v[2]) + '\n')

        # top and bottom faces
        for f in self.__bt_face_list:
            objf.write('f ' + str(f[0]+1) + ' ' + str(f[1]+1) + ' ' + str(f[2]+1) + '\n')

        # side faces
        for f in self.__side_face_list:
            objf.write('f ' + str(f[0]+1) + ' ' + str(f[1]+1) + ' ' + str(f[2]+1) + '\n')


    def __is_able_to_gen(self):
        """check we can generate a cylinder.
        raise an exception if not.
        """
        if (self.__n_gon < 3) :
            raise StandardError, ('illegal n_gon setting. _n be >= 3, but ' +\
                                      str(self.__n_gon))

        if (self.__radius[0] <= 0.0) :
            raise StandardError, ('illegal top radius: ' + str(self.__radius[0]))

        if (self.__radius[1] <= 0.0) :
            raise StandardError, ('illegal bottojm radius: ' + str(self.__radius[1]))



    def __gen_top_bottom_vertex(self):
        """generate top and bottom polygon vertices
        """
        self.__vertex_list = []
        step_angle = (2 * math.pi) / self.__n_gon

        for tp in xrange(0, 2):
            for i in xrange(0, self.__n_gon):
                x = self.__radius[tp] * math.cos(i * step_angle) + self.__center[tp][0]
                y = self.__radius[tp] * math.sin(i * step_angle) + self.__center[tp][1]
                z = self.__center[tp][2]
                self.__vertex_list.append(numpy.array([x, y, z]))


    def __gen_top_bottom_polygon(self):
        """generate top and bottom polygons.
        __gen_top_bottom_vertex should be run before.
        """
        if ((len(self.__vertex_list)) != (2 * self.__n_gon)):
            raise StandardError, ('unexpected vertex list length: ' +
                                  str(len(self.__vertex_list)) + ' != ' +
                                  str(2 * self.__n_gon) +
                                  ' Has __gen_top_bottom_vertex() not called?')

        self.__bt_face_list = []
        n = self.__n_gon
        for i in xrange(1, ((n + 1) - 2)):
            self.__bt_face_list.append([0, i,   i+1]) # top
        for i in xrange(1, ((n + 1) - 2)):
            self.__bt_face_list.append([n, n+i, n+i+1]) # bottom


    def __gen_side_polygon(self):
        """generate cylinder side polygons
        """
        self.__side_face_list = []
        n = self.__n_gon
        for i in xrange(0, self.__n_gon - 1):
            self.__side_face_list.append([i, n+i+1, i+1])
            self.__side_face_list.append([i, n+i,   n+i+1])

        # the last quad
        self.__side_face_list.append([n-1, n, 0])
        self.__side_face_list.append([n-1, 2*n-1, n])


    # string representation
    def __str__(self):
        return 'Polygonal_cylinder_gen'



#
# main test
#
# if __name__ == '__main__':
#     pass
