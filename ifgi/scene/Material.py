#!/usr/bin/env python
#
# Copyright 2010-2011 (C) Yamauchi, Hitoshi
#
"""IFGI Material
\file
\brief scene element material
"""

import sys, math, numpy, copy
from ifgi.base import numpy_util

import Texture
# import HitRecord
# from ifgi.base import OrthonomalBasis

class Material(object):
    """Material class: interface"""

    def __init__(self, _mat_name):
        """constructor

        \param[in] _mat_name material name (this should be unique)
        """

        self.__material_name = _mat_name


    def get_classname(self):
        """get class name. interface method. (public).
        \return class name
        """
        assert 0, "get_classname must be implemented in a derived class."
        return None


    def get_material_name(self):
        """get material name
        \return material name (should be unique)
        """
        return self.__material_name


    def is_emit(self):
        """is emit light?.
        \return true when emit light.
        """
        return False


    def emit_radiance(self, _hit_onb, _light_out_dir, _tex_point, _tex_uv):
        """emit radiance

        \param[in] _hit_onb hit point orthonomal basis
        \param[in] _light_out_dir outgoing direction from the light
        \param[in] _tex_point texture 3d point (if solid)
        \param[in] _tex_uv    texture uv coordinate (if surface)
        \return emit radiance
        """
        return numpy.array([0,0,0])


    def ambient_response(self, _hit_onb, _incident_dir, _tex_point, _tex_uv):
        """ambient response

        \param[in] _hit_onb hit point orthonomal basis
        \param[in] _incident_dir incident direction
        \param[in] _tex_point texture 3d point (if solid)
        \param[in] _tex_uv    texture uv coordinate (if surface)
        \return ambient response
        """
        return numpy.array([0,0,0])



    def explicit_brdf(self, _hit_onb, _out_v0, _out_v1, _tex_point, _tex_uv):
        """explicit brdf

        \param[in] _hit_onb hit point orthonomal basis
        \param[in] _out_v0  outgoing vector v0
        \param[in] _out_v1  outgoing vector v1
        \param[in] _tex_point texture 3d point (if solid)
        \param[in] _tex_uv    texture uv coordinate (if surface)
        \return False when not supported
        """
        return False


    def diffuse_direction(self, _hit_onb, _incident_dir, _tex_point, _tex_uv,\
                              _rnd_seed, _out_color, _v_out):
        """explicit brdf

        \param[in] _hit_onb hit point orthonomal basis
        \param[in] _incident_dir incident direction
        \param[in] _tex_point texture 3d point (if solid)
        \param[in] _tex_uv    texture uv coordinate (if surface)
        \param[in,out] _rnd_seed random number seed on screen (vec2)
        \param[out] _out_color output color
        \param[out] _v_out outgoing vector?

        \return true when supported
        """
        return False


    def specular_direction(self, _hit_onb, _incident_dir, _tex_point, _tex_uv,\
                              _rnd_seed, _tex_color, _v_out):
        """explicit brdf

        \param[in] _hit_onb hit point orthonomal basis
        \param[in] _incident_dir incident direction
        \param[in] _tex_point texture 3d point (if solid)
        \param[in] _tex_uv    texture uv coordinate (if surface)
        \param[in,out] _rnd_seed randomnumber seed
        \param[out] _tex_color texture color
        \param[out] _v_out outgoing vector?

        \return true when supported
        """
        return False


    def transmission_direction(self, _hit_onb, _incident_dir, _tex_point, _tex_uv,\
                              _rnd_seed, _ext_color, _fresnel_scale, _v_out):
        """explicit brdf

        \param[in] _hit_onb hit point orthonomal basis
        \param[in] _incident_dir incident direction
        \param[in] _tex_point texture 3d point (if solid)
        \param[in] _tex_uv    texture uv coordinate (if surface)
        \param[in,out] _rnd_seed randomnumber seed
        \param[out] _ext_color extinction color
        \param[out] _fresnel_scale fresnel scale
        \param[out] _v_out outgoing vector?

        \return true when supported
        """
        return False


    def is_diffuse(self):
        """is diffuse?
        \return true when diffuse
        """
        return False


    def is_specular(self):
        """is specular?
        \return true when specular
        """
        return False


    def is_transmissive(self):
        """is transmissive?
        \return true when transmissive

        """
        return False


    def get_gl_preview_dict(self):
        """get material information for OpenGL preview.

        gl_preview_dict = {'fg_color':  float4,
                           'emission':  float4,
                           'diffuse':   float4,
                           'ambient':   float4,
                           'specular':  float4,
                           'shininess': str(float)}
        \return OpenGL preview data
        """
        gl_preview_dict = {'fg_color':  numpy.array([1.0,0.5,0.5,1.0]),
                           'emission':  numpy.array([0,0,0,1]),
                           'diffuse':   numpy.array([1.0,0.5,0.5,1.0]),
                           'ambient':   numpy.array([0,0,0,1]),
                           'specular':  numpy.array([0,0,0,1]),
                           'shininess': str(1.0)}
        return gl_preview_dict


    def set_gl_preview_dict(self, _gl_preview_dict):
        """set material information from OpenGL material editor.
        \param[in] _gl_preview_dict
        """
        pass



#----------------------------------------------------------------------


class DiffuseMaterial(Material):
    """Diffuse material"""

    def __init__(self, _mat_name, _texture):
        """default constructor

        \param[in] _mat_name material name
        \param[in] _texture  texture object
        """
        super(DiffuseMaterial, self).__init__(_mat_name)

        self.__texture = _texture


    def get_classname(self):
        """get class name..
        \return 'DiffuseMaterial'
        """
        return 'DiffuseMaterial'


    # def is_emit(self):
    #     """is emit light?.
    #     \return true when emit light.
    #     """
    #     return False
    # def emit_radiance(self, _hit_onb, _light_out_dir, _tex_point, _tex_uv):


    def get_texture(self):
        """get texture
        """
        return self.__texture


    def ambient_response(self, _hit_onb, _incident_dir, _tex_point, _tex_uv):
        """ambient response

        \param[in] _hit_onb hit point orthonomal basis
        \param[in] _incident_dir incident direction
        \param[in] _tex_point texture 3d point (if solid)
        \param[in] _tex_uv    texture uv coordinate (if surface)
        \return ambient response
        """
        return self.__texture.value(_tex_uv, _tex_point)



    def explicit_brdf(self, _hit_onb, _out_v0, _out_v1, _tex_point, _tex_uv):
        """explicit brdf

        \param[in] _hit_onb hit point orthonomal basis
        \param[in] _out_v0  outgoing vector v0
        \param[in] _out_v1  outgoing vector v1
        \param[in] _tex_point texture 3d point (if solid)
        \param[in] _tex_uv    texture uv coordinate (if surface)
        \return False when not supported
        """
        (1/math.pi) * self.__texture.value(_tex_uv, _tex_point)

        return True


    def diffuse_direction(self, _hit_onb, _incident_dir, _tex_point, _tex_uv,\
                              _rnd_seed, _out_color, _v_out):
        """explicit brdf

        \param[in] _hit_onb hit point orthonomal basis
        \param[in] _incident_dir incident direction
        \param[in] _tex_point texture 3d point (if solid)
        \param[in] _tex_uv    texture uv coordinate (if surface)
        \param[in,out] _rnd_seed random number seed on screen (vec2)
        \param[out] _out_color output color
        \param[out] _v_out outgoing vector?

        \return true when supported
        """

        phi = 2 * math.pi * _rnd_seed.x()
        r   = math.sqrt(_rnd_seed.y())
        x   = r * math.cos(phi)
        y   = r * math.sin(phi)
        z   = math.sqrt(1 - x*x - y*y)
        _out_color = self.__texture.value(_tex_uv, _tex_point)
        _v_out     = x * _hit_onb.u() + y * _hit_onb.v() + z * _hit_onb.v()

        _rnd_seed.scramble()

        return True


    # def specular_direction(self, _hit_onb, _incident_dir, _tex_point, _tex_uv,\
    #                           _rnd_seed, _tex_color, _v_out):


    # def transmission_direction(self, _hit_onb, _incident_dir, _tex_point, _tex_uv,\
    #                           _rnd_seed, _ext_color, _fresnel_scale, _v_out):




    def get_gl_preview_dict(self):
        """get material information for OpenGL preview.
        gl_preview_dict = {'fg_color':  float4,
                           'emission':  float4,
                           'diffuse':   float4,
                           'ambient':   float4,
                           'specular':  float4,
                           'shininess': str(float)}
        \return OpenGL preview data
        """
        fg_color    = numpy.array([0.5, 0.5, 0.5, 1.0]),
        diffuse_col = numpy.array([0.5, 0.5, 0.5, 1.0]),
        if(self.__texture.get_classname() == 'ConstantColorTexture'):
            diffuse_col = self.__texture.value(None, None)
            fg_color    = copy.deepcopy(diffuse_col)


        gl_preview_dict = {'fg_color':  fg_color,
                           'emission':  numpy.array([0,0,0,1]),
                           'diffuse':   diffuse_col,
                           'ambient':   numpy.array([0,0,0,1]),
                           'specular':  numpy.array([0,0,0,1]),
                           'shininess': str(1.0)}
        return gl_preview_dict


    def set_gl_preview_dict(self, _gl_preview_dict):
        """set material information from OpenGL material editor.
        \param[in] _gl_preview_dict
        """
        # fg_color    = _gl_preview_dict['fg_color']
        diffuse_col = _gl_preview_dict['diffuse']
        self.__texture.set_constant_color(diffuse_col)


# ----------------------------------------------------------------------

class EnvironmentMaterial(Material):
    """Environment material
    """

    def __init__(self, _mat_name, _texture):
        """default constructor

        \param[in] _mat_name material name
        \param[in] _texture  texture object
        """
        super(EnvironmentMaterial, self).__init__(_mat_name)

        self.__texture = _texture


    def get_classname(self):
        """get class name..
        \return 'EnvironmentMaterial'
        """
        return 'EnvironmentMaterial'


    # def is_emit(self):
    #     """is emit light?.
    #     \return true when emit light.
    #     """
    #     return False
    # def emit_radiance(self, _hit_onb, _light_out_dir, _tex_point, _tex_uv):


    def get_texture(self):
        """get texture
        """
        return self.__texture


    def ambient_response(self, _hit_onb, _incident_dir, _tex_point, _tex_uv):
        """ambient response

        \param[in] _hit_onb hit point orthonomal basis
        \param[in] _incident_dir incident direction
        \param[in] _tex_point texture 3d point (if solid)
        \param[in] _tex_uv    texture uv coordinate (if surface)
        \return ambient response
        """
        return self.__texture.value(_tex_uv, _tex_point)



    def explicit_brdf(self, _hit_onb, _out_v0, _out_v1, _tex_point, _tex_uv):
        """explicit brdf

        \param[in] _hit_onb hit point orthonomal basis
        \param[in] _out_v0  outgoing vector v0
        \param[in] _out_v1  outgoing vector v1
        \param[in] _tex_point texture 3d point (if solid)
        \param[in] _tex_uv    texture uv coordinate (if surface)
        \return False when not supported
        """
        (1/math.pi) * self.__texture.value(_tex_uv, _tex_point)

        return True


    def get_gl_preview_dict(self):
        """get material information for OpenGL preview.
        gl_preview_dict = {'const_bg_color':  float4}
        \return OpenGL preview data
        """
        const_bg_color = numpy.array([0.1, 0.1, 0.1, 1.0]),
        if(self.__texture.get_classname() == 'ConstantColorTexture'):
            diffuse_col = self.__texture.value(None, None)
            const_bg_color = copy.deepcopy(diffuse_col)

        gl_preview_dict = {'const_bg_color':  const_bg_color}
        return gl_preview_dict


    def set_gl_preview_dict(self, _gl_preview_dict):
        """set material information from OpenGL material editor.
        \param[in] _gl_preview_dict
        """
        const_bg_color = _gl_preview_dict['const_bg_color']
        self.__texture.set_constant_color(const_bg_color)


# ----------------------------------------------------------------------

def material_factory(_mat_dict):
    """material factory from material information dictionary.
    \return a material
    """
    mat = None
    mat_type = _mat_dict['mat_type']
    if(mat_type == 'lambert'):
        diffuse_color = _mat_dict['diffuse_color']
        tex = Texture.ConstantColorTexture(numpy_util.str2array(diffuse_color))
        mat = DiffuseMaterial(_mat_dict['mat_name'], tex)
    elif(mat_type == 'environment_constant_color'):
        diffuse_color = _mat_dict['diffuse_color']
        tex = Texture.ConstantColorTexture(numpy_util.str2array(diffuse_color))
        mat = EnvironmentMaterial(_mat_dict['mat_name'], tex)
    else:
        raise StandardError, ('Unsupported material type [' + mat_type + ']')

    return mat


#
# main test
#
#if __name__ == '__main__':
#    pass
