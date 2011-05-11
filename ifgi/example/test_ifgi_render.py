#!/usr/bin/env python
#
# Copyright (C) 2010-2011 Yamauchi, Hitoshi
#
# Example: a big example, this should be break down while developing
#
# For set up the environment to run, see test_all.sh
#
"""
\file
\brief a big example. This is for developing.
"""

import unittest
import numpy

# package import: specify a directory and file.
from ifgi.ptracer import IfgiSys
from ifgi.scene   import SceneGraph, Primitive, Film

class TestIfgiRender(unittest.TestCase):
    """test: ifgi render test. This is a big example for development"""

    def test_render(self):
        """test rendering"""
        # get ifgi system
        ifgi_inst = IfgiSys.IfgiSys()
        ifgi_stat = ifgi_inst.start()
        assert(ifgi_stat == True)

        # members
        self.__scenegraph = None

        # run the test
        self.__create_scene()
        self.__set_camera_paramneter()
        self.__render_frame()
        self.__save_frame()

        ifgi_stat = ifgi_inst.shutdown()



    #----------------------------------------------------------------------
    # test subroutines
    #----------------------------------------------------------------------
    def __create_scene(self):
        print 'creating a scene'

        # create scenegraph
        self.__scenegraph = SceneGraph.SceneGraph()
        assert(self.__scenegraph.get_root_node() == None)

        # create scenegraph's root node
        rootsg = SceneGraph.SceneGraphNode('rootsg')

        # add a camera
        child0 = SceneGraph.CameraNode('main_cam')
        rootsg.append_child(child0)

        self.__scenegraph.set_root_node(rootsg)
        self.__scenegraph.set_current_camera(child0.get_camera())

        assert(self.__scenegraph.is_valid())

        # added a mesh group
        meshgroup_node = SceneGraph.SceneGraphNode('meshgroup_0')
        rootsg.append_child(meshgroup_node)

        # create a triangle mesh and attch to the trimesh node
        trimesh = self.__get_one_triangle_trimesh()
        trimesh_node = SceneGraph.SceneGraphNode('trimesh_0')
        trimesh_node.set_primitive(trimesh)
        meshgroup_node.append_child(trimesh_node)


    # get one triangle trimesh
    # TODO: move to a test
    def __get_one_triangle_trimesh(self):
        """create one triangle trimesh"""

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
        return trimesh


    # set a perspective camera, look at the triangle
    def __set_camera_paramneter(self):
        cur_cam = self.__scenegraph.get_current_camera()
        assert(cur_cam != None)
        eye_pos    = numpy.array([ 0.0, 0.0,  5.0])
        lookat_pos = numpy.array([ 0.0, 0.0, -1.0])
        cur_cam.set_eye_lookat_pos(eye_pos, lookat_pos)
        cur_cam.set_up_dir(numpy.array([ 0.0, 1.0, 0.0]))

        # added RGBA buffer to the current camera.
        cur_cam.set_film('RGBA', Film.ImageFilm(128, 128, 4, 'RGBA'))
        cur_cam.print_obj()


    # render a frame
    def __render_frame(self):
        assert(False)

    # save the result
    def __save_frame(self):
        assert(False)


#
# main test
#
suit0   = unittest.TestLoader().loadTestsFromTestCase(TestIfgiRender)
alltest = unittest.TestSuite([suit0])
unittest.TextTestRunner(verbosity=2).run(alltest)


