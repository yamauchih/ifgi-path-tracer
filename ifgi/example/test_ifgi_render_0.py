#!/usr/bin/env python
#
# Copyright (C) 2010-2011 Yamauchi, Hitoshi
#
# Example 0: create a scene and only hit test buffer
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
from ifgi.scene   import SceneGraph, Primitive, Film, test_scene_util
from ifgi.base    import Sampler

class TestIfgiRender0(unittest.TestCase):
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

        # create a triangle mesh and attach to the trimesh node
        objfname = '../../sampledata/cornel_box.obj'
        self.__trimesh = SceneGraph.load_one_trimesh_from_objfile(objfname)
        trimesh_node = SceneGraph.PrimitiveNode('trimesh_0', self.__trimesh)

        # TODO: when attach create (removable) acceleration structure
        # Idea: create an aggregate node, that has a method
        # set_primitive, it creates acceleration structure, for
        # instance.

        meshgroup_node.append_child(trimesh_node)


    # set a perspective camera, look at the triangle
    def __set_camera_paramneter(self):
        cur_cam = self.__scenegraph.get_current_camera()
        assert(cur_cam != None)
        # cornel box official camera parameter
        # Position	278 273 -800
        # Direction	0 0 1
        # Up direction	0 1 0
        # Focal length	0.035
        # Width, height	0.025 0.025
        eye_pos    = numpy.array([278.0, 273.0, -800.0])
        view_dir   = numpy.array([ 0.0, 0.0, 1.0])
        up_dir     = numpy.array([ 0.0, 1.0, 0.0])
        cur_cam.set_eye_pos(eye_pos)
        cur_cam.set_view_dir(view_dir)
        cur_cam.set_up_dir(up_dir)
        cur_cam.set_z_near(0.01)
        cur_cam.set_z_far(5000.0)

        # added RGBA buffer to the current camera.
        imgsz = (self._image_xsize, self._image_ysize, 4)
        cur_cam.set_film('Hit',  Film.ImageFilm(imgsz, 'Hit'))
        cur_cam.print_obj()


    # ray trimesh intersection test
    def __compute_color(self, _pixel_x, _pixel_y, _ray):
        # FIXME: super slow
        cur_cam = self.__scenegraph.get_current_camera()
        hit_buf = cur_cam.get_film('Hit')

        hr = self.__trimesh.ray_intersect(_ray)
        if hr != None:
            # Hit point visualization
            hit_buf.put_color((_pixel_x, _pixel_y), self.FIXME_REDARY)



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
        film = cur_cam.get_film('Hit')
        assert(film != None)
        fname = 'test_ifgi_render_0.Hit.png'
        film.save_file(fname)
        print 'Saved ... ' + fname


#
# main test
#
if __name__ == '__main__':
    suit0   = unittest.TestLoader().loadTestsFromTestCase(TestIfgiRender0)
    alltest = unittest.TestSuite([suit0])
    unittest.TextTestRunner(verbosity=2).run(alltest)


