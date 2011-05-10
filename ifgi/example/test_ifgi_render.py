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
from ifgi.ptracer.IfgiSys  import IfgiSys
from ifgi.scene.SceneGraph import SceneGraph, SceneGraphNode, CameraNode



class TestIfgiRender(unittest.TestCase):
    """test: ifgi render test. This is a big example for development"""

    def test_render(self):
        """test rendering"""
        # get ifgi system
        ifgi_inst = IfgiSys()
        ifgi_stat = ifgi_inst.start()
        assert(ifgi_stat == True)

        self.__create_scene()
        self.__set_camera_paramneter()
        self.__set_framebuffer()
        self.__render_frame()
        self.__save_frame()

        ifgi_stat = ifgi_inst.shutdown()



    #----------------------------------------------------------------------
    # test subroutines
    #----------------------------------------------------------------------
    def __create_scene(self):
        print 'creating a scene'

        # create scenegraph
        self.__scenegraph = SceneGraph()
        assert(self.__scenegraph.get_root_node() == None)

        # create scenegraph's root node
        rootsg = SceneGraphNode('rootsg')

        # add a camera
        child0 = CameraNode('main_cam')
        rootsg.append_child(child0)

        self.__scenegraph.set_root_node(rootsg)
        self.__scenegraph.set_current_camera(child0.get_camera())

        assert(self.__scenegraph.is_valid())


        # add a triangle


    # set a perspective camera, look at the triangle
    def __set_camera_paramneter(self):

        assert(False)


    # set a framebuffer to the camera
    def __set_framebuffer(self):
        assert(False)

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


