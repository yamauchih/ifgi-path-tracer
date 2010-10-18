#!/usr/bin/env python
#
# Primitive
#

"""IFGI Primitive"""

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
# BBox: axis aligned bounding box
#
class BBox(Primitive):
    # default constructor
    def __init__(self):
        self.min = numpy.array([1, 1, 1])
        self.max = numpy.array([0, 0, 0])

    # class name
    def get_classname(self):
        return 'BBox'

    # get the bounding box
    def get_bbox(self):
        return self

    # compute ray intersection
    def ray_intersect(self, _ray):
        assert 0, "NIN."
        return None


#
# Triangle
#
class Triangle(Primitive):
    # default constructor
    def __init__(self):
        self.vertex = [
            numpy.array([1, 0, 0])
            numpy.array([0, 1, 0])
            numpy.array([0, 0  1])
            ]
        self.bbox = BBox()

    # class name
    def get_classname(self):
        return 'Triangle'

    # get the bounding box
    def get_bbox(self):
        return self.bbox

    # compute ray intersection
    def ray_intersect(self, _ray):
        assert 0, "NIN."
        return None


#
# TriMesh
#
class TriMesh(Primitive):
    # default constructor
    def __init__(self):
        self.triangle = []
        self.bbox = BBox()

    # class name
    def get_classname(self):
        return 'TriMesh'

    # get the bounding box
    def get_bbox(self):
        return self.bbox

    # compute ray intersection
    def ray_intersect(self, _ray):
        assert 0, "NIN."
        return None


#
# main test
#
if __name__ == '__main__':
    pass
