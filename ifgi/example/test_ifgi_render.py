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
from ifgi.scene   import SceneGraph, Primitive, Film, Light
from ifgi.base    import Sampler

class TestIfgiRender(unittest.TestCase):
    """test: ifgi render test. This is a big example for development"""

    FIXME_REDARY = numpy.array([1, 0, 0, 1])


    def test_render(self):
        """test rendering"""
        # get ifgi system
        ifgi_inst = IfgiSys.IfgiSys()
        ifgi_stat = ifgi_inst.start()
        assert(ifgi_stat == True)

        self._image_xsize = 128
        self._image_ysize = 128

        # FIXME: trimesh should be retrieved by scene (or aggregate)
        self.__fixme_trimesh = None

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
        self.__fixme_trimesh = self.__get_one_triangle_trimesh()
        trimesh_node = SceneGraph.SceneGraphNode('trimesh_0')
        trimesh_node.set_primitive(self.__fixme_trimesh)
        meshgroup_node.append_child(trimesh_node)

        # create a light and set lightgroup
        light_pos       = numpy.array([3.0, 3.0, 3.0])
        light_intensity = numpy.array([1.0, 1.0, 1.0])
        pl = Light.PointLight('light0', light_pos, light_intensity)
        lg = Light.LightGroup('lightgroup0')
        lg.add_light(pl)

        # add (global) lightgroup to the scenegraph
        self.__scenegraph.set_light_group(lg)


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
        imgsz = (self._image_xsize, self._image_ysize, 4)
        cur_cam.set_film('RGBA', Film.ImageFilm(imgsz, 'RGBA'))
        cur_cam.print_obj()


    # ray trimesh intersection test
    def __compute_color(self, _pixel_x, _pixel_y, _ray):
        # FIXME: super slow
        cur_cam = self.__scenegraph.get_current_camera()
        film = cur_cam.get_film('RGBA')

        if self.__fixme_trimesh.ray_intersect(_ray):
            film.put_color((_pixel_x, _pixel_y), self.FIXME_REDARY)
            # self.__get_all_light_radiance()



    # render a frame
    def __render_frame(self):
        srs = Sampler.StratifiedRegularSampler()
        srs.compute_sample(0, self._image_xsize - 1, 0, self._image_ysize - 1)

        assert(self._image_xsize > 0)
        assert(self._image_ysize > 0)

        inv_xsz = 1.0/self._image_xsize
        inv_ysz = 1.0/self._image_ysize
        cur_cam = self.__scenegraph.get_current_camera()

        for x in xrange(0, self._image_xsize, 1):
            for y in xrange(0, self._image_ysize, 1):
                # get normalized coordinate
                nx = srs.get_sample_x(x,y) * inv_xsz
                ny = srs.get_sample_y(x,y) * inv_ysz
                eye_ray = cur_cam.get_ray(nx, ny)
                # print eye_ray
                # print nx, ny
                self.__compute_color(x, y, eye_ray)


    # save the result
    def __save_frame(self):
        cur_cam = self.__scenegraph.get_current_camera()
        assert(cur_cam != None)
        film = cur_cam.get_film('RGBA')
        assert(film != None)
        fname = 'test_ifgi_render.png'
        film.save_file(fname)
        print 'Saved ... ' + fname


#
# main test
#
suit0   = unittest.TestLoader().loadTestsFromTestCase(TestIfgiRender)
alltest = unittest.TestSuite([suit0])
unittest.TextTestRunner(verbosity=2).run(alltest)


