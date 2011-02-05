#!/usr/bin/env python

"""IFGI Primitive
\file
\brief scene element primitives
"""

import sys
import math
import numpy

import Ray

# Primitive class: interface
class Primitive(object):
    """Primitive class: interface"""

    # default constructor
    def __init__(self):
        """default constructor (public)"""
        pass

    # class name
    def get_classname(self):
        """get class name. interface method. (public).
        \return class name
        """
        assert 0, "get_classname must be implemented in a derived class."
        return None

    # get the bounding box
    def get_bbox(self):
        """get the bounding box. interface method. (public).
        \return bounding box of this primitive.
        """
        assert 0, "get_bbox must be implemented in a derived class."
        return None

    # compute ray intersection
    def ray_intersect(self, _ray):
        """compute ray intersection. interface method. (public)
        \param[in] _ray a ray
        """
        assert 0, "ray_intersect must be implemented in a derived class."
        return None

# BBox: axis aligned 3D bounding box
class BBox(Primitive):
    """BBox: axis aligned 3D bounding box"""

    # default constructor
    def __init__(self):
        """default constructor (public)."""
        self.invalidate()

    # invalidate this bbox
    def invalidate(self):
        """invalidate this bbox (public)."""
        self.min = numpy.array([sys.float_info.max,
                                sys.float_info.max,   sys.float_info.max])
        self.max = numpy.array([-sys.float_info.max,
                                -sys.float_info.max, -sys.float_info.max])

    # insert point, grow the bbox
    def insert_point(self, _newpos):
        """insert a point and grow the bbox. (public).
        \param[in] _newpos newly inserted point
        """
        for i in xrange(0, 3, 1):
            if (self.min[i] > _newpos[i]):
                self.min[i] = _newpos[i]
            # here elif (self.max[i] < _newpos[i]): doesn't work, when
            # just after invalidate() call when [max, max, max]-[-max,
            # -max, -max], insert [0,0,0], both min, max must be
            # [0,0,0], if I use elif, only min is updated. Therefore
            # this must be if:
            if (self.max[i] < _newpos[i]):
                self.max[i] = _newpos[i]
        # print 'DEBUG: ' + str(self) + ', p' + str(_newpos)

    # insert bbox, grow the bbox
    def insert_bbox(self, _bbox):
        """insert a bbox and grow the bbox. (public)
        \param _bbox bounding box to be inserted.
        """
        self.insert_point(bbox.min)
        self.insert_point(bbox.max)

    # get minimal point
    def get_min(self):
        """get minimal point (public).
        \return minimal point (numpy.array[3])
        """
        return self.min

    # get maximal point
    # \return maximal point (numpy.array[3])
    def get_max(self):
        """get maximal point (public).
        \return maximal point (numpy.array[3])
        """
        return self.max

    # class name
    def get_classname(self):
        """ get class name (public).
        \return class name
        """
        return 'BBox'

    # get the bounding box
    def get_bbox(self):
        """get the bounding box (public).
        \return self
        """
        return self

    # equal?
    def equal(self, _other):
        """equal? (public).
        comparison self with _other. If exact the same, return True
        otherwise False.
        \param[in] _other other bounding box to compare
        """
        if (self is _other):    # if the same object, True
            return True
        elif (((self.min == _other.min).all()) and ((self.max == _other.max).all())):
            # numpy == is elementwise, all() is all element-and
            return True
        return False

    # string representation
    def __str__(self):
        """string representation (public).
        \return string representation of this object.
        """
        return 'bbox[%g %g %g]-[%g %g %g]' % (self.min[0], self.min[1], self.min[2],
                                              self.max[0], self.max[1], self.max[2])

    # compute ray intersection
    def ray_intersect(self, _ray):
        """compute ray intersection. interface. (public).
        \param[in] _ray a ray
        """
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


# TriMesh
class TriMesh(Primitive):
    """TriMesh: simple triangle mesh primitive
    """


    # default constructor
    def __init__(self):
        """default constructor (public)."""
        self.vertex_list       = []
        self.face_idx_list     = []
        self.texcoord_list     = []
        self.texcoord_idx_list = []
        self.normal_list       = []
        self.normal_idx_list   = []
        self.bbox              = BBox()

    # set data
    def set_data(self, _vlist, _fidxlist, _tclist, _tcidxlist, _nlist, _nidxlist):
        """set data (public).

        \param[in]  _vlist     vertex list (len(_vlist) must be > 0)
        \param[in]  _fidxlist  face index list
        \param[in]  _tclist    texture coordinate list
        \param[in]  _tcidxlist texture coordinate index list
        \param[in]  _nlist     normal list
        \param[in]  _nidxlist  normal index list
        """
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
        """update bounding box according to current vertex list (public).
        """
        self.bbox.invalidate()  # reset the bbox
        for pos in self.vertex_list:
            self.bbox.insert_point(pos)

    # class name
    def get_classname(self):
        """get class name (public).
        """
        return 'TriMesh'

    # get the bounding box
    def get_bbox(self):
        """get the bounding box. (public).
        \return trimesh's bouding box.
        """
        return self.bbox

    # is this valid object?
    def is_valid(self):
        """is this valid object? (public).
        At least len(vertex_list) > 0
        """
        if len(self.vertex_list) > 0:
            return True
        return False

    # compute ray intersection
    def ray_intersect(self, _ray):
        """compute ray intersection. (public).
        \param[in] _ray a ray
        """
        assert 0, "NIN."
        return None

#
# main test
#
#if __name__ == '__main__':
#    pass
