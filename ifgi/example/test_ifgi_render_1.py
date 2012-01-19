#!/usr/bin/env python
#
# Copyright (C) 2010-2011 Yamauchi, Hitoshi
#
# Example 1: rendering test/example
#
# For set up the environment to run, see test_all.sh
#
"""
\file
\brief a big example. This is for developing.
"""

import cProfile
import unittest
import numpy

# package import: specify a directory and file.
from ifgi.base    import Sampler
from ifgi.ptracer import IfgiSys
from ifgi.scene   import SceneGraph, Primitive, Film, test_scene_util, IfgiSceneReader
from ifgi.scene   import SceneUtil


class TestIfgiRender1(unittest.TestCase):
    """test: ifgi render test. This is a big example for development"""

    FIXME_REDARY = numpy.array([1, 0, 0, 1])

    def test_render(self):
        """test rendering"""
        # get ifgi system
        ifgi_inst = IfgiSys.IfgiSys()
        ifgi_stat = ifgi_inst.start()
        assert(ifgi_stat == True)

        # change the camera resolution to this size 
        self.__image_xsize = 32
        self.__image_ysize = 32

        # members
        self.__scenegraph = None

        # global geometry/material list
        self.__scene_geo_mat = SceneUtil.SceneGeometryMaterialContainer()

        # run the test
        self.__create_scene()
        self.__render_frame()
        self.__save_frame()

        ifgi_stat = ifgi_inst.shutdown()


    def __create_scene(self):
        """create scene.
        geometry, material, and camera.
        """

        print 'creating a scene'

        # create scenegraph by the ifgi scene parser

        _infilepath = '../../sampledata/cornel_box.ifgi'
        ifgireader = IfgiSceneReader.IfgiSceneReader()
        if(not ifgireader.read(_infilepath)):
            raise StandardError, ('load file [' + _infilepath + '] failed.')

        self.__scenegraph = SceneGraph.create_ifgi_scenegraph(ifgireader)
        self.__scenegraph.update_all_bbox()

        # create the global material_name -> material lookup map
        self.__scene_geo_mat.append_ifgi_data(ifgireader)
        self.__scene_geo_mat.print_summary()

        # -- now all primitive (TriMesh) can look up the material

        # set the camera
        # default camera should exist
        print ifgireader.camera_dict_dict
        assert('default' in ifgireader.camera_dict_dict)

        cur_cam = self.__scenegraph.get_current_camera()
        cur_cam.set_config_dict(ifgireader.camera_dict_dict['default'])
        print 'resize the camera resolution from ['    +\
            str(cur_cam.get_resolution_x())  + ' '     +\
            str(cur_cam.get_resolution_y())  + '] -> ' +\
            str(self.__image_xsize)  + ' '     +\
            str(self.__image_ysize)  + ']'
        cur_cam.set_resolution_x(self.__image_xsize)
        cur_cam.set_resolution_y(self.__image_ysize)

        # added RGBA buffer and Hit buffer to the current camera.
        imgsz = (cur_cam.get_resolution_x(), cur_cam.get_resolution_y(), 4)
        cur_cam.set_film('Hit',     Film.ImageFilm(imgsz, 'Hit'))
        cur_cam.set_film('RGBA',    Film.ImageFilm(imgsz, 'RGBA'))
        cur_cam.set_film('Zbuffer', Film.ImageFilm(imgsz, 'Zbuffer'))
        # cur_cam.print_obj()


    # ray trimesh intersection test
    def __compute_color(self, _pixel_x, _pixel_y, _ray):
        # FIXME: super slow
        cur_cam = self.__scenegraph.get_current_camera()
        hit_buf = cur_cam.get_film('Hit')
        col_buf = cur_cam.get_film('RGBA')
        z_buf   = cur_cam.get_film('Zbuffer')

        hr = self.__scene_geo_mat.ray_intersect(_ray)
        # (/ 761295 676) average dist 1126
        dist_scale = 2000
        if hr != None:
            # Hit point visualization
            hit_buf.put_color((_pixel_x, _pixel_y), self.FIXME_REDARY)
            # lookup material
            mat = self.__scene_geo_mat.material_list[hr.hit_material_index]
            # just constant color
            col_buf.put_color((_pixel_x, _pixel_y),
                              mat.ambient_response(None, None, None, None))
            # record depth
            depth = hr.dist/dist_scale
            z_buf.put_color((_pixel_x, _pixel_y),
                            numpy.array([depth, depth, depth, 1]))
            # print 'dist ', hr.dist

    # render a frame
    def __render_frame(self):
        cur_cam = self.__scenegraph.get_current_camera()
        image_xsize = cur_cam.get_resolution_x()
        image_ysize = cur_cam.get_resolution_y()
        assert(image_xsize > 0)
        assert(image_ysize > 0)

        srs = Sampler.StratifiedRegularSampler()
        srs.compute_sample(0, image_xsize - 1, 0, image_ysize - 1)

        inv_xsz = 1.0/image_xsize
        inv_ysz = 1.0/image_ysize

        for x in xrange(0, image_xsize, 1):
            for y in xrange(0, image_ysize, 1):
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
        fname = 'test_ifgi_render_1.RGBA.png'
        film.save_file(fname)
        print 'Saved ... ' + fname

        film = cur_cam.get_film('Hit')
        assert(film != None)
        fname = 'test_ifgi_render_1.Hit.png'
        film.save_file(fname)
        print 'Saved ... ' + fname

        film = cur_cam.get_film('Zbuffer')
        assert(film != None)
        fname = 'test_ifgi_render_1.Zbuf.png'
        film.save_file(fname)
        print 'Saved ... ' + fname


#
# main test
#
if __name__ == '__main__':
    suit0   = unittest.TestLoader().loadTestsFromTestCase(TestIfgiRender1)
    alltest = unittest.TestSuite([suit0])
    unittest.TextTestRunner(verbosity=2).run(alltest)
