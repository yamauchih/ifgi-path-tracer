#!/usr/bin/env python
#
# Copyright (C) 2010-2011 Yamauchi, Hitoshi
#
# Example 3: rendering test/example via C++ rendering core
#
# For set up the environment to run, see test_all.sh
#
"""
\file
\brief a big example. This is for developing.
"""

import cProfile
import unittest
import numpy, random, copy, math

# package import: specify a directory and file.
from ifgi.base    import Sampler, ifgi_util
from ifgi.ptracer import IfgiSys
from ifgi.scene   import SceneGraph, Primitive, Film, test_scene_util, IfgiSceneReader
from ifgi.scene   import SceneUtil
from ifgi.cpp.api import ifgi_python_cpp_translator_mod


class TestIfgiRender3(unittest.TestCase):
    """test: ifgi render test. This is a big example for development"""

    def test_render(self):
        """test rendering"""

        print
        print 'StartTime: ' + ifgi_util.get_current_localtime_str()

        # get ifgi system
        ifgi_inst = IfgiSys.IfgiSys()
        ifgi_stat = ifgi_inst.start()
        assert(ifgi_stat == True)

        # random.seed(0)

        self.__max_path_length = 10 # 2...for direct light only: FIXME not used

        # C++ rendering translator. This translator has a cpp
        # rendering core which has scenegraph, material, primitives...
        self.__ifgi_cpp_render_core = \
            ifgi_python_cpp_translator_mod.ifgi_python_cpp_translator()
        self.__ifgi_cpp_render_core.initialize()

        self.__create_scene()

        # render frames
        self.__ifgi_cpp_render_core.prepare_rendering()
        max_frame      = 10000
        save_per_frame = 100
        self.__ifgi_cpp_render_core.render_n_frame(max_frame, save_per_frame)

        ifgi_stat = self.__ifgi_cpp_render_core.shutdown()

        print 'EndTime: ', ifgi_util.get_current_localtime_str()


    def __create_scene(self):
        """create scene.
        geometry, material, and camera.
        """

        print 'creating a scene'
        # create scenegraph by the ifgi scene parser
        _infilepath = '../../sampledata/cornel_box.ifgi'
        # _infilepath = '../../sampledata/one_tri_full.ifgi'
        ifgireader = IfgiSceneReader.IfgiSceneReader()
        if(not ifgireader.read(_infilepath)):
            raise StandardError, ('load file [' + _infilepath + '] failed.')

        # add a new scene
        #   A ifgi file may have many cameras, but only default camera
        #   is handled.
        cam_dict = ifgireader.camera_dict_dict['default']

        assert(self.__ifgi_cpp_render_core != None)
        self.__ifgi_cpp_render_core.create_scene(ifgireader.material_dict_list,\
                                                     ifgireader.geometry_dict_list,\
                                                     cam_dict)
        # check the camera correctly pushed
        # print cam_dict
        # dir(ifgi_cpp_render_core)
        # ret_cam_dict = ifgi_cpp_render_core.get_camera_pydict()
        # print ret_cam_dict

        # self.__scenegraph.update_all_bbox()
        # -- now all primitive (TriMesh) can look up the material

        # # added RGBA buffer and Hit buffer to the current camera.
        # imgsz = (self.__image_xsize, self.__image_ysize, 4)
        # cur_cam.set_film('RGBA',    Film.ImageFilm(imgsz, 'RGBA'))
        # # cur_cam.print_obj()




    # save the result
    def __save_frame(self, _nframe):
        print 'DEBUG: save frame'
        cur_cam = self.__scenegraph.get_current_camera()
        assert(cur_cam != None)
        film = cur_cam.get_film('RGBA')
        assert(film != None)
        fname = 'test_ifgi_render_2.RGBA.' + str(_nframe) + '.png'
        film.save_file(fname)
        print 'Saved ... ' + fname


#
# main test
#
if __name__ == '__main__':
    suit0   = unittest.TestLoader().loadTestsFromTestCase(TestIfgiRender3)
    alltest = unittest.TestSuite([suit0])
    unittest.TextTestRunner(verbosity=2).run(alltest)
