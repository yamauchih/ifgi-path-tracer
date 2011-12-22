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
import numpy, random, copy

# package import: specify a directory and file.
from ifgi.base    import Sampler
from ifgi.ptracer import IfgiSys
from ifgi.scene   import SceneGraph, Primitive, Film, test_scene_util, IfgiSceneReader
from ifgi.scene   import SceneUtil


class TestIfgiRender1(unittest.TestCase):
    """test: ifgi render test. This is a big example for development"""

    # DELETEME FIXME_REDARY = numpy.array([1, 0, 0, 1])

    def test_render(self):
        """test rendering"""
        # get ifgi system
        ifgi_inst = IfgiSys.IfgiSys()
        ifgi_stat = ifgi_inst.start()
        assert(ifgi_stat == True)

        random.seed(0)
        # unit hemisphere uniform sampler
        self.__hemisphere_sampler = Sampler.UnitHemisphereUniformSampler()

        # FIXME random.uniform(0,1)

        self.__image_xsize = 50
        self.__image_ysize = 50
        self.__max_path_length = 2 # 2...for direct light only

        # members
        self.__scenegraph = None

        # global geometry/material list
        self.__scene_geo_mat = SceneUtil.SceneGeometryMaterialContainer()

        self.__create_scene()

        # get environment material from the scene
        self.__environment_mat = self.__retrieve_environment_material_from_scene()

        save_per_frame = 25

        for nf in xrange(0, 10000):
            self.__render_frame(nf)
            print nf
            if ((nf != 0) and (nf % save_per_frame == 0)):
                self.__save_frame(nf)

        self.__save_frame(0)


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

        # added RGBA buffer and Hit buffer to the current camera.
        imgsz = (self.__image_xsize, self.__image_ysize, 4)
        cur_cam.set_film('RGBA',    Film.ImageFilm(imgsz, 'RGBA'))
        # cur_cam.print_obj()


    def __retrieve_environment_material_from_scene(self):
        """retrieve environment material from the scene.
        The scene should be constructed.

        \return found environment material in the scene"""

        env_mat_name = 'default_env'
        if not(self.__scene_geo_mat.material_name_idx_dict.has_key(env_mat_name)):
            raise StandardError, ('Not found environment material [' + env_mat_name + '].')

        env_mat_idx = self.__scene_geo_mat.material_name_idx_dict[env_mat_name]
        env_mat = self.__scene_geo_mat.material_list[env_mat_idx]
        assert(env_mat.get_classname() == 'EnvironmentMaterial')

        return env_mat


    def __compute_color(self, _pixel_x, _pixel_y, _ray, _nframe):
        """compute framebuffer color"""
        # FIXME: super slow
        cur_cam = self.__scenegraph.get_current_camera()
        col_buf = cur_cam.get_film('RGBA')

        for _ray.path_length in xrange(0, self.__max_path_length):
            hr = self.__scene_geo_mat.ray_intersect(_ray)
            if hr != None:
                # hit somthing, lookup material
                assert(hr.hit_material_index >= 0)
                mat = self.__scene_geo_mat.material_list[hr.hit_material_index]
                # FIXME: only Lambert
                # mat.explicit_brdf(hr.hit_basis, _out_v0, _out_v1, _tex_point, _tex_uv)
                # print 'DEBUG: mat ref = ', mat.explicit_brdf(None, None, None, None, None)
                brdf = mat.explicit_brdf(None, None, None, None, None)
                _ray.reflectance = (_ray.reflectance * brdf)
                if mat.is_emit():
                    # FIXME: only Lambert emittance
                    # mat.emit_radiance(_hit_onb, _light_out_dir, _tex_point, _tex_uv))
                    _ray.intensity = _ray.intensity + \
                        (_ray.reflectance * mat.emit_radiance(None, None, None, None))
                    # hit the light source
                    print 'DEBUG: Hit a light source at path length = ', _ray.path_length

                    break

                # Do not stop by reflectance criterion. (if stop, wrong)

                # update ray information
                out_v = mat.diffuse_direction(hr.hit_basis, _ray.get_dir(), \
                                                  self.__hemisphere_sampler)
                _ray.set_origin(copy.deepcopy(hr.intersect_pos))
                _ray.set_dir(copy.deepcopy(out_v))

            else:
                # done. hit to the environmnt.
                # FIXME: currently assume the environment color is always constant
                hit_onb = None
                light_out_dir = None
                tex_point = None
                tex_uv = None
                # print 'DEBUG: ray int = ', _ray.intensity, ', ref = ' , _ray.reflectance
                amb_col = self.__environment_mat.ambient_response(hit_onb, light_out_dir,\
                                                                      tex_point, tex_uv)
                _ray.intensity = _ray.intensity + (_ray.reflectance * amb_col)
                # print 'DEBUG: hit env, amb_col = ', amb_col
                break


        # now we know the color
        col = float(_nframe) * col_buf.get_color((_pixel_x, _pixel_y)) + _ray.intensity
        col_buf.put_color((_pixel_x, _pixel_y), col/(float(_nframe) + 1.0))


    # no more refrection, too less reflectance
    def __enough_reflectance(self, _ray):
        if _ray.reflectance.max() < 0.01:
            print 'DEBUG: max reflectance is less than 0.01 ', _ray.reflectance
            return False
        return True


    # render a frame
    def __render_frame(self, _nframe):
        srs = Sampler.StratifiedRegularSampler()
        srs.compute_sample(0, self.__image_xsize - 1, 0, self.__image_ysize - 1)

        assert(self.__image_xsize > 0)
        assert(self.__image_ysize > 0)

        inv_xsz = 1.0/self.__image_xsize
        inv_ysz = 1.0/self.__image_ysize
        cur_cam = self.__scenegraph.get_current_camera()

        for x in xrange(0, self.__image_xsize, 1):
            # print 'DEBUG x = ', x
            for y in xrange(0, self.__image_ysize, 1):
                # get normalized coordinate
                nx = srs.get_sample_x(x,y) * inv_xsz
                ny = srs.get_sample_y(x,y) * inv_ysz
                eye_ray = cur_cam.get_ray(nx, ny)
                # print eye_ray
                # print nx, ny
                self.__compute_color(x, y, eye_ray, _nframe)

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

        # DELETEME
        # film = cur_cam.get_film('Hit')
        # assert(film != None)
        # fname = 'test_ifgi_render_2.Hit.png'
        # film.save_file(fname)
        # print 'Saved ... ' + fname

        # film = cur_cam.get_film('Zbuffer')
        # assert(film != None)
        # fname = 'test_ifgi_render_2.Zbuf.png'
        # film.save_file(fname)
        # print 'Saved ... ' + fname


#
# main test
#
if __name__ == '__main__':
    suit0   = unittest.TestLoader().loadTestsFromTestCase(TestIfgiRender1)
    alltest = unittest.TestSuite([suit0])
    unittest.TextTestRunner(verbosity=2).run(alltest)
