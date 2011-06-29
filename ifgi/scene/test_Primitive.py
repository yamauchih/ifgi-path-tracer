#!/usr/bin/env python
#
# Copyright 2011 (C) Yamauchi, Hitoshi
#
#
# test for Primitive module
#

"""test IFGI Primitive module"""

from PIL import Image           # image

import unittest
import numpy
import random
import Primitive
import Ray
import cProfile
import pstats

# test primitive: triangle ray intersection
def primitive_tri_ray_intersection_sub():
    """primitive: ray-triangle intesection subroutine"""

    iw = 50
    ih = 50
    imgsize = (iw, ih)
    # create a triangle
    xoff = iw/10
    yoff = iw/10
    p0 = numpy.array([xoff,           yoff, -10.0])
    p1 = numpy.array([iw - xoff,      yoff, -10.0])
    p2 = numpy.array([iw/2,      ih - yoff, -10.0])

    tri = Primitive.Triangle()
    tri.set_vertex(p0, p1, p2)

    white   = (255, 255, 255)
    red     = (255,   0,   0)
    resimg = Image.new("RGBA", imgsize, white)

    for x in xrange(0, imgsize[0], 1):
        for y in xrange(0, imgsize[1], 1):
            origin = numpy.array([ x, y, 0])
            dir    = numpy.array([ 0, 0, -1])
            min_t  = 0.1
            max_t  = 100
            r = Ray.Ray(origin, dir, min_t, max_t)
            is_hit, dist = tri.ray_intersect(r)
            if is_hit == True:
                # print origin, 'Hit'

                resimg.putpixel((x, imgsize[1]-y), red)

    resimg.save("res_ray_tri_intersect.png")
    print 'Saved ... res_ray_tri_intersect.png'


# test primitives
class TestPrimitive(unittest.TestCase):
    """test suit for Primitive."""
    # test bbox
    def test_bbox(self):
        """test for bbox"""
        random.seed(0)

        minp = numpy.array([-2.0, -1.0,  1.2])
        maxp = numpy.array([-0.2,  1.0,  5.5])
        ipos = numpy.array([ 0.0,  0.0,  0.0])
        bbox = Primitive.BBox()
        for p in xrange(1000):
            for i in xrange(0, 3, 1):
                ipos[i] = random.uniform(minp[i], maxp[i])
                # print i, ipos
            bbox.insert_point(ipos)

        for i in xrange(2):
            assert(minp[i]     <= bbox.get_min()[i])
            assert(bbox.get_min()[i] <= bbox.get_max()[i])
            assert(bbox.get_max()[i] <= maxp[i])

    # test primitive: one triangle
    def test_primitive_one_tri(self):
        """test primitive: one triangle"""
        tmesh = Primitive.TriMesh()

        vertex_list       = []
        face_idx_list     = []
        texcoord_list     = []
        texcoord_idx_list = []
        normal_list       = []
        normal_idx_list   = []

        # add a triangle
        vertex_list.append(numpy.array([ 1.0, 0.0, 0.0]))
        vertex_list.append(numpy.array([ 0.0, 1.0, 0.0]))
        vertex_list.append(numpy.array([-1.0, 0.0, 0.0]))
        face_idx_list.append(numpy.array([0, 1, 2]))

        tmesh.set_data(vertex_list,
                       face_idx_list,
                       texcoord_list,
                       texcoord_idx_list,
                       normal_list,
                       normal_idx_list
                       )
        bbox = Primitive.BBox()
        bbox.insert_point(numpy.array([-1.0, 0.0, 0.0]))
        bbox.insert_point(numpy.array([ 1.0, 1.0, 0.0]))
        assert(tmesh.get_bbox().equal(bbox))


    # primitive: ray-triangle intesection
    def test_primitive_tri_ray_intersection_sub(self):
        """primitive: ray-triangle intesection"""

        primitive_tri_ray_intersection_sub()

        #--- profile
        # cProfile.run('primitive_tri_ray_intersection_sub()')
        #
        # cProfile.run('primitive_tri_ray_intersection_sub()',
        #              'test_primitive.prof')
        # p = pstats.Stats('test_primitive.prof')

#
# main test
#
suit0   = unittest.TestLoader().loadTestsFromTestCase(TestPrimitive)
alltest = unittest.TestSuite([suit0])
unittest.TextTestRunner(verbosity=2).run(alltest)
