#!/usr/bin/env python
#
# Copyright 2010-2011 (C) Yamauchi, Hitoshi
#
"""IFGI Primitive
\file
\brief scene element primitives
"""

import sys
import math
import numpy

import Ray
import HitRecord
from ifgi.base import OrthonomalBasis

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

    # can this primitive intersect with a ray?
    def can_intersect(self):
        """can this primitive intersect with a ray?

        Some of primitives can not directory intersect with a ray. For
        example, TriMesh. These primitives need refinement first.
        """
        assert 0, "can_intersect must be implemented in a derived class."
        return False

    # compute ray intersection
    def ray_intersect(self, _ray):
        """compute ray intersection. interface method. (public)
        \param[in] _ray a ray
        \return None (A HitRecord)
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

    # can this primitive intersect with a ray?
    def can_intersect(self):
        """can bbox primitive intersect with a ray? yes.
        """
        return True

    # compute ray intersection
    def ray_intersect(self, _ray):
        """compute ray intersection. interface.
        \param[in] _ray a ray
        \return None (A HitRecord)
        """
        assert 0, "NIN."
        return None


    # invalidate this bbox
    def invalidate(self):
        """invalidate this bbox (public)."""
        self.__min = numpy.array([sys.float_info.max,
                                  sys.float_info.max,   sys.float_info.max])
        self.__max = numpy.array([-sys.float_info.max,
                                  -sys.float_info.max, -sys.float_info.max])

    # insert point, grow the bbox
    def insert_point(self, _newpos):
        """insert a point and grow the bbox. (public).
        \param[in] _newpos newly inserted point
        """
        for i in xrange(0, 3, 1):
            if (self.__min[i] > _newpos[i]):
                self.__min[i] = _newpos[i]
            # here elif (self.max[i] < _newpos[i]): doesn't work, when
            # just after invalidate() call when [max, max, max]-[-max,
            # -max, -max], insert [0,0,0], both min, max must be
            # [0,0,0], if I use elif, only min is updated. Therefore
            # this must be if:
            if (self.__max[i] < _newpos[i]):
                self.__max[i] = _newpos[i]
        # print 'DEBUG: ' + str(self) + ', p' + str(_newpos)

    # insert bbox, grow the bbox
    def insert_bbox(self, _bbox):
        """insert a bbox and grow the bbox. (public)
        \param _bbox bounding box to be inserted.
        """
        self.insert_point(_bbox.get_min())
        self.insert_point(_bbox.get_max())

    # get minimal point
    def get_min(self):
        """get minimal point (public).
        \return minimal point (numpy.array[3])
        """
        return self.__min

    # get maximal point
    # \return maximal point (numpy.array[3])
    def get_max(self):
        """get maximal point (public).
        \return maximal point (numpy.array[3])
        """
        return self.__max

    # equal?
    def equal(self, _other):
        """equal? (public).
        comparison self with _other. If exact the same, return True
        otherwise False.
        \param[in] _other other bounding box to compare
        """
        if (self is _other):    # if the same object, True
            return True
        elif (((self.__min == _other.get_min()).all()) and
              ((self.__max == _other.get_max()).all())):
            # numpy == is elementwise, all() is all element-and
            return True
        return False

    # string representation
    def __str__(self):
        """string representation (public).
        \return string representation of this object.
        """
        return 'bbox[%g %g %g]-[%g %g %g]' % (self.__min[0], self.__min[1], self.__min[2],
                                              self.__max[0], self.__max[1], self.__max[2])

# Triangle
class Triangle(Primitive):
    """A triangle.
    """

    # default constructor
    def __init__(self):
        """default constructor.
        """
        self.__vertex = None
        self.__bbox   = None

    # class name
    def get_classname(self):
        return 'Triangle'

    # get the bounding box
    def get_bbox(self):
        if self.__bbox == None:
            raise StandardError, ('Invalid triangle, no bounding box.')

        return self.__bbox

    # can this primitive intersect with a ray?
    def can_intersect(self):
        """can a triangle intersect with a ray? Yes.
        """
        return True

    # compute ray intersection
    def ray_intersect(self, _ray):
        """compute ray intersection. interface method.
        \param[in]  _ray a ray
        \return a HitRecord. None when not hit.
        \
        """
        assert(self.__vertex != None)

        # Cramer's rule based ray-triangle intersection

        # get s1
        e1 = self.__vertex[1] - self.__vertex[0]
        e2 = self.__vertex[2] - self.__vertex[0]
        s1 = numpy.cross(_ray.get_dir(), e2)
        div = numpy.dot(s1, e1)
        if div == 0.0:
            return None
        inv_div = 1.0/div

        # get barycentric coord b1
        d = _ray.get_origin() - self.__vertex[0]
        b1 = numpy.dot(d, s1) * inv_div
        if ((b1 < 0.0) or (b1 > 1.0)):
            return None

        # get barycentric coord b2
        s2 = numpy.cross(d, e1)
        b2 = numpy.dot(_ray.get_dir(), s2) * inv_div
        if ((b2 < 0.0) or ((b1 + b2) > 1.0)):
            return None

        # get intersection point (distance t)
        t = numpy.dot(e2, s2) * inv_div
        if ((t < _ray.get_min_t()) or (t > _ray.get_max_t())):
            return None

        # print 'Hit: t = ' + str(t) + ', b1 = ' + str(b1) + ', b2 = ' + str(b2)
        hr = HitRecord.HitRecord()
        hr.dist = t
        hr.hit_primitive = self
        hr.hit_basis = OrthonomalBasis.OrthonomalBasis()
        hr.hit_basis.init_from_uv(e1, e2) # set normal
        return hr

    # set vertex
    def set_vertex(self, _v0, _v1, _v2):
        """Set triangle vertices.
        \param[in] _v0 vertex 0
        \param[in] _v1 vertex 1
        \param[in] _v2 vertex 2
        """
        self.__vertex = [_v0, _v1, _v2]
        self.__update_bbox()

    # update bbox
    def __update_bbox(self):
        self.__bbox = BBox()
        self.__bbox.insert_point(self.__vertex[0])
        self.__bbox.insert_point(self.__vertex[1])
        self.__bbox.insert_point(self.__vertex[2])




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

    # class name
    def get_classname(self):
        """get class name. interface method.
        \return class name
        """
        return 'TriMesh'

    # get the bounding box
    def get_bbox(self):
        """get the bounding box. interface method.
        \return bounding box of this primitive.
        """
        return self.bbox

    # can this primitive intersect with a ray?
    def can_intersect(self):
        """can TriMesh primitive intersect with a ray? no.
        This object needs refinement.
        """
        return False

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
        \return a HitRecord. None if no hit.
        """
        # NIN: bounding box test?

        trimesh_hr = HitRecord.HitRecord()

        # following init is make sure only (done in the HitRecord.__init__())
        trimesh_hr.dist = sys.float_info.max
        trimesh_hr.hit_primitive = None

        for fi in self.face_idx_list:
            tri = Triangle()
            tri.set_vertex(self.vertex_list[fi[0]],
                           self.vertex_list[fi[1]],
                           self.vertex_list[fi[2]])
            # FIXME: need nearest hit
            hr = tri.ray_intersect(_ray)
            if hr != None:
                if trimesh_hr.dist > hr.dist:
                    trimesh_hr.dist = hr.dist
                    trimesh_hr.hit_primitive = tri
                    trimesh_hr.hit_basis = hr.hit_basis

        if trimesh_hr.hit_primitive != None:
            return trimesh_hr

        return None









#
# main test
#
#if __name__ == '__main__':
#    pass
