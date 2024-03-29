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

# ----------------------------------------------------------------------

class Primitive(object):
    """Primitive class: interface"""


    def __init__(self):
        """default constructor"""
        # primitive name (may None)
        self.__name = None
        # material name (may None)
        self.__material_name = None
        # material global index. set when the scene is fixed.
        self.__material_global_index = -1

    def get_classname(self):
        """get class name. interface method.
        \return class name
        """
        assert 0, "get_classname must be implemented in a derived class."
        return None


    def set_name(self, _name):
        """set primitive associated name.
        \return primitive name
        """
        self.__name = _name


    def get_name(self):
        """get primitive associated name.
        \return primitive name
        """
        return self.__name


    def set_material_name(self, _mat_name):
        """set primitive's material name.
        \param[in] _mat_name material name
        """
        self.__material_name = _mat_name


    def get_material_name(self):
        """get primitive's material name.
        \return material name
        """
        return self.__material_name


    def set_material_global_index(self, _mat_idx):
        """set primitive's material global index.
        material index is scene global index for fast material lookup.
        \param[in] _mat_idx material index (for fast lookup)
        """
        self.__material_global_index = _mat_idx


    def get_material_global_index(self):
        """get primitive's material global index.
        If -1, no material is indicated.
        \return global material index
        """
        return self.__material_global_index


    def get_bbox(self):
        """get the bounding box. interface method.
        \return bounding box of this primitive.
        """
        assert 0, "get_bbox must be implemented in a derived class."
        return None


    def can_intersect(self):
        """can this primitive intersect with a ray?

        Some of primitives can not directory intersect with a ray. For
        example, TriMesh. These primitives need refinement first.
        """
        assert 0, "can_intersect must be implemented in a derived class."
        return False


    def ray_intersect(self, _ray):
        """compute ray intersection. interface method. (public)
        \param[in] _ray a ray
        \return None (A HitRecord)
        """
        assert 0, "ray_intersect must be implemented in a derived class."
        return None

# ----------------------------------------------------------------------

class BBox(Primitive):
    """BBox: axis aligned 3D bounding box"""


    def __init__(self):
        """default constructor (public)."""
        super(Primitive, self).__init__()
        self.invalidate()


    def get_classname(self):
        """ get class name (public).
        \return class name
        """
        return 'BBox'


    def get_bbox(self):
        """get the bounding box (public).
        \return self
        """
        return self


    def can_intersect(self):
        """can bbox primitive intersect with a ray? yes.
        """
        return True


    def ray_intersect(self, _ray):
        """compute ray intersection. interface.
        \param[in] _ray a ray
        \return None (A HitRecord)
        """
        assert 0, "NIN."
        return None


    def invalidate(self):
        """invalidate this bbox.
        The bbox has no volume after invalidate().
        """
        self.__min = numpy.array([sys.float_info.max,
                                  sys.float_info.max,   sys.float_info.max])
        self.__max = numpy.array([-sys.float_info.max,
                                  -sys.float_info.max, -sys.float_info.max])


    def get_rank(self):
        """get rank of this bbox.
        The number of self.__max > self.__min satisfied axis.
        \return True when this bbox has area.
        """
        tflist = self.__max > self.__min
        rank_count = 0
        for tf in tflist:
            if tf:
                rank_count += 1
        return rank_count


    def has_volume(self):
        """has this bbox volume?.
        After invalidate(), bbox has no volume.
        \return True when this bbox has volume.
        """
        # for all max > min.
        return all(self.__max > self.__min)


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


    def insert_bbox(self, _bbox):
        """insert a bbox and grow the bbox. (public)
        \param _bbox bounding box to be inserted.
        """
        assert(_bbox.get_rank() > 0) # handle line/plane case.
        self.insert_point(_bbox.get_min())
        self.insert_point(_bbox.get_max())


    def get_min(self):
        """get minimal point (public).
        \return minimal point (numpy.array[3])
        """
        return self.__min


    def get_max(self):
        """get maximal point (public).
        \return maximal point (numpy.array[3])
        """
        return self.__max


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


    def __str__(self):
        """string representation (public).
        \return string representation of this object.
        """
        return 'bbox[%g %g %g]-[%g %g %g]' % (self.__min[0], self.__min[1], self.__min[2],
                                              self.__max[0], self.__max[1], self.__max[2])

# ----------------------------------------------------------------------

class Triangle(Primitive):
    """A triangle.
    """

    def __init__(self):
        """default constructor.
        """
        super(Triangle, self).__init__()
        self.__vertex = None
        self.__bbox   = None


    def get_classname(self):
        return 'Triangle'


    def get_bbox(self):
        if self.__bbox == None:
            raise StandardError, ('Invalid triangle, no bounding box.')

        return self.__bbox


    def can_intersect(self):
        """can a triangle intersect with a ray? Yes.
        """
        return True


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
        hr.intersect_pos = self.__vertex[0] + b1 * e1 + b2 * e2
        hr.hit_primitive = self
        hr.hit_basis = OrthonomalBasis.OrthonomalBasis()
        hr.hit_basis.init_from_uv(e1, e2) # set normal
        return hr


    def set_vertex(self, _v0, _v1, _v2):
        """Set triangle vertices.
        \param[in] _v0 vertex 0
        \param[in] _v1 vertex 1
        \param[in] _v2 vertex 2
        """
        self.__vertex = [_v0, _v1, _v2]
        self.__update_bbox()


    def __update_bbox(self):
        self.__bbox = BBox()
        self.__bbox.insert_point(self.__vertex[0])
        self.__bbox.insert_point(self.__vertex[1])
        self.__bbox.insert_point(self.__vertex[2])

# ----------------------------------------------------------------------

class TriMesh(Primitive):
    """TriMesh: simple triangle mesh primitive
    """

    def __init__(self, _mash_name, _mat_name):
        """default constructor (public)."""
        super(TriMesh, self).__init__()
        super(TriMesh, self).set_name(_mash_name)
        super(TriMesh, self).set_material_name(_mat_name)

        # geometry information
        self.vertex_list       = []
        self.face_idx_list     = []
        self.texcoord_list     = []
        self.texcoord_idx_list = []
        self.normal_list       = []
        self.normal_idx_list   = []
        self.bbox              = BBox()

        # global material index of this geometry (valid after
        # preprocessing)
        self.material_index = -1


    def get_classname(self):
        """get class name. interface method.
        \return class name
        """
        return 'TriMesh'


    def get_bbox(self):
        """get the bounding box. interface method.
        \return bounding box of this primitive.
        """
        return self.bbox


    def can_intersect(self):
        """can TriMesh primitive intersect with a ray? no.
        This object needs refinement.
        """
        return False


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


    def set_material_index(self, _mat_idx):
        """set global material index.

        \param[in] _mat_idx global material index.
        """
        # FIXME: Or shall I push this information to each triangles?
        self.material_index = _mat_idx


    def info_summary(self):
        """summary information

        \return summary information string
        """
        ret_str =\
            '# vertices     = ' + str(len(self.vertex_list))   + '\n' +\
            '# faces        = ' + str(len(self.face_idx_list)) + '\n' +\
            '# texcoords    = ' + str(len(self.texcoord_list)) + '\n' +\
            '# texcoord idx = ' + str(len(self.texcoord_idx_list)) + '\n' +\
            '# normal       = ' + str(len(self.normal_list))   + '\n' +\
            '# normal idx   = ' + str(len(self.normal_idx_list)) + '\n' +\
            'bbox           = ' + str(self.get_bbox())         + '\n' +\
            'material idx   = ' + str(self.material_index)

        return ret_str


    def update_bbox(self):
        """update bounding box according to current vertex list (public).
        """
        self.bbox.invalidate()  # reset the bbox
        for pos in self.vertex_list:
            self.bbox.insert_point(pos)


    def is_valid(self):
        """is this valid object? (public).
        At least len(vertex_list) > 0
        """
        if len(self.vertex_list) > 0:
            return True
        return False


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

            hr = tri.ray_intersect(_ray)
            if hr != None:
                if trimesh_hr.dist > hr.dist:
                    trimesh_hr.dist = hr.dist
                    trimesh_hr.intersect_pos = hr.intersect_pos
                    trimesh_hr.hit_primitive = tri
                    trimesh_hr.hit_basis = hr.hit_basis
                    trimesh_hr.hit_material_index = self.material_index

        if trimesh_hr.hit_primitive != None:
            return trimesh_hr

        return None




#
# main test
#
#if __name__ == '__main__':
#    pass
