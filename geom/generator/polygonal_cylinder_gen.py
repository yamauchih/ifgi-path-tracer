#!/usr/bin/env python
#
# Copyright 2011 (C) Yamauchi, Hitoshi
#
# Cylinder generator
#

"""Cylinder generator
\file
\brief generate a (polygonal) cylinder from a center point list.
"""

import math, numpy

class Polygonal_cylinder_gen(object):
    """Simple poltgonal cylinder generator.
    The normal of top and bottom polygons are always z+ (0,0,1)
    """

    def __init__(self):
        """default constructor.
        """
        #------------------------------
        # inputs
        self.__poly_normal   = numpy.array([0.0, 0.0, 1.0])
        self.__poly_tangent  = numpy.array([1.0, 0.0, 0.0])
        self.__poly_binomal  = numpy.array([0.0, 1.0, 0.0])

        self.__center_list = []
        self.__radius_list = []
        self.__n_gon = 0        # fixed for a cylinder

        # switch to generate segment polygons (horizontal polygons)
        self.__is_gen_segment_tris = False

        #------------------------------
        # generated results
        self.__vertex_list       = []
        self.__segment_face_list = []
        self.__side_face_list    = []


    def clear(self):
        """clear the input center points and generated data"""
        self.__center_list = []
        self.__radius_list = []

        self.__vertex_list       = []
        self.__segment_face_list = []
        self.__side_face_list    = []


    def append_center_point(self, _center_point, _radius):
        """set polygon parameter
        \param[in] _center_point polygon center point
        \param[in] _radius       polygon radius
        """
        if (len(_center_point) != 3):
            raise StandardError, ('_center_point should be a 3D point.')

        if (_radius <= 0):
            raise StandardError, ('_radius must be > 0, but ' + str(_radius))

        # sanity check. without this check still generates cylinders,
        # but, may be looked broken
        list_sz = len(self.__center_list)
        if (list_sz > 0):
            if (self.__center_list[list_sz - 1][2] >= _center_point[2]):
                raise StandardError, ('z values must be acendent order.' +
                                      str(self.__center_list[list_sz - 1]) + ', ' +
                                      str(_center_point))

        self.__center_list.append(_center_point)
        self.__radius_list.append(_radius)


    def set_generate_segment_tris(self, _is_gen):
        """set generate top and bottom triangles.
        \param[in] _is_gen generate top and bottom triangles when True
        """
        self.__is_gen_segment_tris = _is_gen


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

        self.__gen_vertex()
        if (self.__is_gen_segment_tris):
            self.__gen_segment_tris()
        self.__gen_side_polygon()


    def export_obj(self, _objfname):
        """export obj file
        \param[in] _objfname exporting obj file name
        """
        # assert(self.__is_face_index_valid())

        if ((_objfname == None) or (len(_objfname) == 0)):
            raise StandardError, ('empty obj output file name.')

        objf = open(_objfname, 'w')

        # output mesh info
        vtx_count  = len(self.__vertex_list)
        face_count = len(self.__side_face_list) + len(self.__segment_face_list)
        if (vtx_count == 0):
            raise StandardError, ('no vertices.')
        objf.write('# ' + str(vtx_count) + ' ' + str(face_count) + ' 0\n')

        # vertices
        for v in self.__vertex_list:
            objf.write('v ' + str(v[0]) + ' ' + str(v[1]) + ' ' + str(v[2]) + '\n')

        # top and bottom faces
        for f in self.__segment_face_list:
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

        if (len(self.__center_list) < 2) :
            raise StandardError, ('fail. less than two center points.')


    def __gen_vertex(self):
        """generate vertices for the cylinder
        """
        self.__vertex_list = []
        step_angle = (2 * math.pi) / self.__n_gon

        for seg in xrange(0, len(self.__center_list)):
            for i in xrange(0, self.__n_gon):
                rad = self.__radius_list[seg]
                cp  = self.__center_list[seg]
                x = rad * math.cos(i * step_angle) + cp[0]
                y = rad * math.sin(i * step_angle) + cp[1]
                z = cp[2]
                self.__vertex_list.append(numpy.array([x, y, z]))


    def __gen_segment_tris(self):
        """generate segment triangles (horizontal top/bottom of the cylinder).
        All triangles faces z+ direction.
        __gen_vertex should be run before.
        """
        if ((len(self.__vertex_list)) != (len(self.__center_list) * self.__n_gon)):
            raise StandardError, ('unexpected vertex list length: ' +
                                  str(len(self.__vertex_list)) + ' != ' +
                                  str(len(self.__center_list) * self.__n_gon) +
                                  ' Has __gen_vertex() not called?')

        self.__segment_face_list = []
        n = self.__n_gon
        for seg in xrange(0, len(self.__center_list)):
            n_seg = seg * n     # base index of current processing segment triangles
            for i in xrange(1, ((n + 1) - 2)):
                self.__segment_face_list.append([0 + n_seg, i + n_seg, i + 1 + n_seg])


    def __gen_side_polygon(self):
        """generate cylinder side polygons
        """
        seg_count = len(self.__center_list)
        assert(seg_count >= 2)

        self.__side_face_list = []
        n = self.__n_gon

        for seg in xrange(0, seg_count - 1):
            bidx = seg * n
            for i in xrange(0, n - 1):
                self.__side_face_list.append([bidx + i, bidx + i + 1, bidx + n + i + 1])
                self.__side_face_list.append([bidx + i, bidx + n + i + 1, bidx + n + i])

            # the last quad of this segment
            self.__side_face_list.append([bidx + n - 1, bidx + 0, bidx + n])
            self.__side_face_list.append([bidx + n - 1, bidx + n, bidx + (2 * n - 1)])


    def __is_face_index_valid(self):
        """check the face index's validity
        raise an exception when not valid
        """
        vsize = len(self.__vertex_list)

        for fset in self.__segment_face_list:
            for i in fset:
                if (i < 0) or (i >= vsize):
                    raise StandardError, ('segment face list has invalid face index.')

        for fset in self.__side_face_list:
            for i in fset:
                if (i < 0) or (i >= vsize):
                    raise StandardError, ('side face list has invalid face index.' +
                                          str(i))



    # string representation
    def __str__(self):
        return 'Polygonal_cylinder_gen: ' + \
            str(len(self.__center_list)) + ' centers, ' + \
            str(self.__n_gon) + '-gon, ' + \
            str(len(self.__vertex_list)) + ' vertices, ' + \
            str(len(self.__segment_face_list)) + ' seg tris, ' + \
            str(len(self.__side_face_list)) + ' side faces'


#
# main test
#
# if __name__ == '__main__':
#     pass
