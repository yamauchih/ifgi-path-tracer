#!/usr/bin/env python
#
# Primitive
#

"""IFGI Primitive"""

import sys
import math
import numpy

import Ray

#
# Primitive class: interface
#
class Primitive(object):
    # default constructor
    def __init__(self):
        pass

    # class name
    def get_classname(self):
        assert 0, "get_classname must be implemented in a derived class."
        return None

    # get the bounding box
    def get_bbox(self):
        assert 0, "get_bbox must be implemented in a derived class."
        return None

    # compute ray intersection
    def ray_intersect(self, _ray):
        assert 0, "ray_intersect must be implemented in a derived class."
        return None

#
# BBox: axis aligned 3D bounding box
#
class BBox(Primitive):
    # default constructor
    def __init__(self):
        self.invalidate()

    # invalidate this bbox
    def invalidate(self):
        self.min = numpy.array([sys.float_info.max,
                                sys.float_info.max,   sys.float_info.max])
        self.max = numpy.array([-sys.float_info.max,
                                -sys.float_info.max, -sys.float_info.max])

    # insert point, grow the bbox
    def insert_point(self, _newpos):
        for i in xrange(0, 3, 1):
            if   (self.min[i] > _newpos[i]):
                self.min[i] = _newpos[i]
            elif (self.max[i] < _newpos[i]):
                self.max[i] = _newpos[i]

    # class name
    def get_classname(self):
        return 'BBox'

    # get the bounding box
    def get_bbox(self):
        return self

    # string representation
    def __str__(self):
        return 'bbox[%g %g %g]-[%g %g %g]' % (self.min[0], self.min[1], self.min[2],
                                              self.max[0], self.max[1], self.max[2])


    # compute ray intersection
    def ray_intersect(self, _ray):
        assert 0, "NIN."
        return None

#
# Triangle
#
# class Triangle(Primitive):
#     # default constructor
#     def __init__(self):
#         self.vertex = [
#             numpy.array([1, 0, 0])
#             numpy.array([0, 1, 0])
#             numpy.array([0, 0  1])
#             ]
#         self.bbox = BBox()

#     # class name
#     def get_classname(self):
#         return 'Triangle'

#     # get the bounding box
#     def get_bbox(self):
#         return self.bbox

#     # compute ray intersection
#     def ray_intersect(self, _ray):
#         assert 0, "NIN."
#         return None


#
# TriMesh
#
class TriMesh(Primitive):
    # default constructor
    def __init__(self):
        self.vertex_list       = []
        self.face_idx_list     = []
        self.texcoord_list     = []
        self.texcoord_idx_list = []
        self.normal_list       = []
        self.normal_idx_list   = []
        self.bbox              = BBox()

    # set data
    #
    # \param[in]  _vlist     vertex list (len(_vlist) must be > 0)
    # \param[in]  _fidxlist  face index list
    # \param[in]  _tclist    texture coordinate list
    # \param[in]  _tcidxlist texture coordinate index list
    # \param[in]  _nlist     normal list
    # \param[in]  _nidxlist  normal index list
    def set_data(self, _vlist, _fidxlist, _tclist, _tcidxlist, _nlist, _nidxlist):
        assert(len(_vlist) > 0) # at least, some points must be there.
        self.vertex_list       = _vlist
        self.face_idx_list     = _fidxlist
        self.texcoord_list     = _tclist
        self.texcoord_idx_list = _tcidxlist
        self.normal_list       = _nlist
        self.normal_idx_list   = _nidxlist
        self.update_bbox()

    # update bounding box according to current vertex list
    def update_bbox(self):
        self.bbox.invalidate()  # reset the bbox
        for pos in self.vertex_list:
            self.bbox.insert_poinst(pos)


    # class name
    def get_classname(self):
        return 'TriMesh'

    # get the bounding box
    def get_bbox(self):
        return self.bbox

    # is valid object? At least len(vertex_list) > 0
    def is_valid(self):
        if len(self.vertex_list) > 0:
            return True
        return False

    # compute ray intersection
    def ray_intersect(self, _ray):
        assert 0, "NIN."
        return None


#
# main test
#
if __name__ == '__main__':
    pass
