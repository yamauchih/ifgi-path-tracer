#!/usr/bin/env python
#
# Copyright (C) 2010-2011 Yamauchi, Hitoshi
#
# test utility for scene module
#
# This is a utility and not a unit test, but used from unit tests.
#

"""test scene module utility"""

import numpy
import Primitive

def test_scene_util_get_one_triangle_trimesh():
    """create one triangle trimesh

    Camera parameters for this object.
    eye_pos    = numpy.array([ 0.0, 0.0,  5.0])
    lookat_pos = numpy.array([ 0.0, 0.0, -1.0])
    cur_cam.set_eye_lookat_pos(eye_pos, lookat_pos)
    cur_cam.set_up_dir(numpy.array([ 0.0, 1.0, 0.0]))
    """

    trimesh = Primitive.TriMesh()
    # create a triangle
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

    trimesh.set_data(vertex_list,
                     face_idx_list,
                     texcoord_list,
                     texcoord_idx_list,
                     normal_list,
                     normal_idx_list
                     )

    # check bbox is correct
    bbox = Primitive.BBox()
    bbox.insert_point(numpy.array([-1.0, 0.0, 0.0]))
    bbox.insert_point(numpy.array([ 1.0, 1.0, 0.0]))
    assert(trimesh.get_bbox().equal(bbox))

    return trimesh
