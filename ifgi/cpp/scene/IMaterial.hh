//----------------------------------------------------------------------
// ifgi c++ implementation
// Copyright (C) 2010-2011 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief ifgi C++ scene element material interface

#ifndef IFGI_CPP_SCENE_IMATERIAL_HH
#define IFGI_CPP_SCENE_IMATERIAL_HH

#include <string>
#include <cpp/base/Vector.hh>

// import sys, math, numpy, copy
// from ifgi.base import numpy_util, ifgi_util, Sampler

// import Texture
// # import HitRecord
// # from ifgi.base import OrthonomalBasis

namespace ifgi {

/// material interface
class IMaterial
{
public:
    /// constructor
    IMaterial();

    // /// constructor
    // /// \param[in] _mat_name material name (this should be unique)
    // IMaterial(std::string const & mat_name);
    // def __init__(self, _mat_name):
    //     """constructor

    //     \param[in] _mat_name material name (this should be unique)
    //     """

    //     self.__material_name = _mat_name

    /// get class name. interface method.
    /// \return class name
    virtual std::string get_classname() const = 0;
        // """get class name. interface method. (public).
        // \return class name
        // """

    /// get material name
    /// \return material name (should be unique)
    virtual std::string get_material_name() const = 0;
        // """get material name
        // \return material name (should be unique)
        // """
        // return self.__material_name

    /// is this material emit light?
    /// \return true when emit light.
    virtual bool is_emit() const = 0;
        // """
        // \return true when emit light.
        // """
        // return False

    /// emit radiance
    ///
    /// \param[in] hit_onb hit point orthonomal basis
    /// \param[in] light_out_dir outgoing direction from the light
    /// \param[in] tex_point texture 3d point (if solid)
    /// \param[in] tex_uv    texture uv coordinate (if surface)
    /// \param[out] out_emit_rad (output) emit radiance
    virtual void emit_radiance(// hit_onb, light_out_dir, tex_point, tex_uv
        Color & out_emit_rad
        ) const;

    /// ambient response
    ///
    /// \param[in] hit_onb hit point orthonomal basis
    /// \param[in] incident_dir incident direction
    /// \param[in] tex_point texture 3d point (if solid)
    /// \param[in] tex_uv    texture uv coordinate (if surface)
    /// \param[out] out_amb_res  (output) ambient responce
    virtual void ambient_response(//_hit_onb, incident_dir, tex_point, tex_uv
        Color & out_amb_res
        ) const;
        // return numpy.array([0,0,0])


    /// explicit brdf
    ///
    /// \param[in] hit_onb hit point orthonomal basis
    /// \param[in] out_v0  outgoing vector v0
    /// \param[in] out_v1  outgoing vector v1
    /// \param[in] tex_point texture 3d point (if solid)
    /// \param[in] tex_uv    texture uv coordinate (if surface)
    /// \param[out] out_brdf  (output) brdf
    virtual void explicit_brdf(// hit_onb, out_v0, out_v1, tex_point, tex_uv
        Color & out_brdf
        ) const;
        // """
        // return None

    /// explicit brdf
    ///
    /// \param[in] hit_onb hit point orthonomal basis
    /// \param[in] incident_dir incident direction
    /// \param[in] hemisphere_sampler   uniform sampler on a hemisphere
    /// \return outgoing direction, None if not supported
    virtual Float32_3 diffuse_direction(// hit_onb, incident_dir, hemisphere_sampler
        ) const;


    /// explicit brdf
    ///
    /// \param[in] hit_onb hit point orthonomal basis
    /// \param[in] incident_dir incident direction
    /// \param[in] tex_point texture 3d point (if solid)
    /// \param[in] tex_uv    texture uv coordinate (if surface)
    /// \param[in,out] rnd_seed randomnumber seed
    /// \param[out] tex_color texture color
    /// \param[out] v_out outgoing vector?
    virtual Float32_3 specular_direction(//hit_onb, incident_dir, tex_point, tex_uv,
        // rnd_seed, tex_color, v_out
        ) const;

        // \return true when supported
        // """
        // return False

    /// explicit brdf
    /// 
    /// \param[in] hit_onb hit point orthonomal basis
    /// \param[in] incident_dir incident direction
    /// \param[in] tex_point texture 3d point (if solid)
    /// \param[in] tex_uv    texture uv coordinate (if surface)
    /// \param[in,out] rnd_seed randomnumber seed
    /// \param[out] ext_color extinction color
    /// \param[out] fresnel_scale fresnel scale
    /// \param[out] v_out outgoing vector?
    /// 
    /// \return true when supported
    // def transmission_direction(_hit_onb, incident_dir, tex_point, tex_uv,
    //                            rnd_seed, ext_color, fresnel_scale, v_out);

    /// is diffuse?
    /// \return true when diffuse
    virtual bool is_diffuse() const;

    /// is specular?
    /// \return true when specular
    virtual bool is_specular() const;

    /// is transmissive?
    /// \return true when transmissive
    virtual bool is_transmissive() const;


    // def get_gl_preview_dict();

    // def set_gl_preview_dict(self, gl_preview_dict);
};


// #----------------------------------------------------------------------


// class DiffuseMaterial(Material):
//     """Diffuse material"""

//     def _init__(self, mat_name, texture, emit_color):
//         """default constructor

//         \param[in] mat_name material name
//         \param[in] texture  texture object
//         \param[in] emit_color emittion color (may None)
//         """
//         super(DiffuseMaterial, self).__init__(_mat_name)

//         self.__texture = texture
//         self.__emit_color = None
//         self.set_emit_color(_emit_color)


//     def initialize_by_dict(self, mat_dict):
//         """initialize by dictionary

//         \param[in] mat_dict material parameter dictionary
//         """

//         mat_dict_copy = copy.deepcopy(_mat_dict)

//         # mandatory parameters
//         mkey = ['mat_type', 'mat_name', 'diffuse_color']
//         if not(ifgi_util.has_dict_all_key(mat_dict_copy, mkey)):
//             missing_keys = ifgi_util.get_dict_missing_key(mat_dict_copy, mkey)
//             raise StandardError, ('missing parameter of lambert material [' +
//                                       str(missing_keys) + ']')
//         # material type and name
//         assert(mat_dict_copy['mat_type'] == 'lambert')
//         mat_dict_copy.pop('mat_type')
//         assert(mat_dict_copy['mat_name'] == self.get_material_name())
//         mat_dict_copy.pop('mat_name')

//         # diffuse color
//         diffuse_color = mat_dict_copy['diffuse_color']
//         self.__texture = Texture.ConstantColorTexture(numpy_util.str2array(diffuse_color))
//         mat_dict_copy.pop('diffuse_color')

//         # optional parameters
//         if mat_dict_copy.has_key('emit_color'):
//             emit_color = numpy_util.str2array(mat_dict_copy['emit_color'])
//             self.set_emit_color(emit_color)
//             mat_dict_copy.pop('emit_color')
//             print 'DEBUG: this lambert material has emit_color ', self.__emit_color

//         if len(mat_dict_copy) > 0:
//             print mat_dict_copy
//             raise StandardError, ('_mat_dict has unknown parameters.' + str(mat_dict_copy))


//     def set_emit_color(self, emit_color):
//         """set emit color

//         \param[in] emit_color emit radiance color. all zeros or None,
//         no emit anymore.
//         """
//         self.__emit_color = None
//         zero4 = numpy.zeros(4)
//         # None or all zeros => None
//         if (_emit_color == None) or all(_emit_color == zero4):
//             return

//         if not(all(_emit_color >= zero4)):
//             raise StandardError, ('emit color components must be >= 0')

//         self.__emit_color = emit_color


//     def get_classname(self):
//         """get class name..
//         \return 'DiffuseMaterial'
//         """
//         return 'DiffuseMaterial'


//     def is_emit(self):
//         """is emit light?.
//         \return true when emit light.
//         """
//         return self.__emit_color != None


//     def emit_radiance(self, hit_onb, light_out_dir, tex_point, tex_uv):
//         """emitting radiance color"""
//         return self.__emit_color


//     def get_texture(self):
//         """get texture
//         """
//         return self.__texture


//     def ambient_response(self, hit_onb, incident_dir, tex_point, tex_uv):
//         """ambient response

//         \param[in] hit_onb hit point orthonomal basis
//         \param[in] incident_dir incident direction
//         \param[in] tex_point texture 3d point (if solid)
//         \param[in] tex_uv    texture uv coordinate (if surface)
//         \return ambient response
//         """
//         return self.__texture.value(_tex_uv, tex_point)



//     def explicit_brdf(self, hit_onb, out_v0, out_v1, tex_point, tex_uv):
//         """explicit brdf

//         \param[in] hit_onb hit point orthonomal basis
//         \param[in] out_v0  outgoing vector v0
//         \param[in] out_v1  outgoing vector v1
//         \param[in] tex_point texture 3d point (if solid)
//         \param[in] tex_uv    texture uv coordinate (if surface)
//         \return BRDF
//         """
//         brdf = (1/math.pi) * self.__texture.value(_tex_uv, tex_point)
//         return brdf


//     def diffuse_direction(self, hit_onb, incident_dir, hemisphere_sampler):
//         """explicit brdf

//         \param[in] hit_onb hit point orthonomal basis
//         \param[in] incident_dir incident direction
//         \param[in] hemisphere_sampler uniform sampler on a hemisphere
//         \param[out] v_out outgoing vector?

//         \return outgoing direction, None if not supported
//         """
//         v_on_hs = hemisphere_sampler.get_sample()
//         v_out   = 
//             v_on_hs[0] * hit_onb.u() +
//             v_on_hs[1] * hit_onb.v() +
//             v_on_hs[2] * hit_onb.w()

//         # need normalize?
//         assert(abs(numpy.linalg.norm(v_out) - 1.0) < 0.00001)

//         return v_out


//     # def specular_direction(self, hit_onb, incident_dir, tex_point, tex_uv,
//     #                           rnd_seed, tex_color, v_out):


//     # def transmission_direction(self, hit_onb, incident_dir, tex_point, tex_uv,
//     #                           rnd_seed, ext_color, fresnel_scale, v_out):


//     def get_gl_preview_dict(self):
//         """get material information for OpenGL preview.
//         gl_preview_dict = {'fg_color':  float4,
//                            'emission':  float4,
//                            'diffuse':   float4,
//                            'ambient':   float4,
//                            'specular':  float4,
//                            'shininess': str(float)}
//         \return OpenGL preview data
//         """
//         fg_color    = numpy.array([0.5, 0.5, 0.5, 1.0]),
//         diffuse_col = numpy.array([0.5, 0.5, 0.5, 1.0]),
//         if(self.__texture.get_classname() == 'ConstantColorTexture'):
//             diffuse_col = self.__texture.value(None, None)
//             fg_color    = copy.deepcopy(diffuse_col)


//         gl_preview_dict = {'fg_color':  fg_color,
//                            'emission':  numpy.array([0,0,0,1]),
//                            'diffuse':   diffuse_col,
//                            'ambient':   numpy.array([0,0,0,1]),
//                            'specular':  numpy.array([0,0,0,1]),
//                            'shininess': str(1.0)}
//         return gl_preview_dict


//     def set_gl_preview_dict(self, gl_preview_dict):
//         """set material information from OpenGL material editor.
//         \param[in] gl_preview_dict
//         """
//         # fg_color    = gl_preview_dict['fg_color']
//         diffuse_col = gl_preview_dict['diffuse']
//         self.__texture.set_constant_color(diffuse_col)


// # ----------------------------------------------------------------------

// class EnvironmentMaterial(Material):
//     """Environment material
//     """

//     def _init__(self, mat_name, texture):
//         """default constructor

//         \param[in] mat_name material name
//         \param[in] texture  texture object (consider as emission)
//         """
//         super(EnvironmentMaterial, self).__init__(_mat_name)

//         self.__texture = texture


//     def get_classname(self):
//         """get class name..
//         \return 'EnvironmentMaterial'
//         """
//         return 'EnvironmentMaterial'


//     # def is_emit(self):
//     #     """is emit light?.
//     #     \return true when emit light.
//     #     """
//     #     return False
//     # def emit_radiance(self, hit_onb, light_out_dir, tex_point, tex_uv):


//     def get_texture(self):
//         """get texture
//         """
//         return self.__texture


//     def ambient_response(self, hit_onb, incident_dir, tex_point, tex_uv):
//         """ambient response

//         \param[in] hit_onb hit point orthonomal basis
//         \param[in] incident_dir incident direction
//         \param[in] tex_point texture 3d point (if solid)
//         \param[in] tex_uv    texture uv coordinate (if surface)
//         \return ambient response
//         """
//         return self.__texture.value(_tex_uv, tex_point)



//     def explicit_brdf(self, hit_onb, out_v0, out_v1, tex_point, tex_uv):
//         """explicit brdf

//         \param[in] hit_onb hit point orthonomal basis
//         \param[in] out_v0  outgoing vector v0
//         \param[in] out_v1  outgoing vector v1
//         \param[in] tex_point texture 3d point (if solid)
//         \param[in] tex_uv    texture uv coordinate (if surface)
//         \return False when not supported
//         """
//         brdf = (1/math.pi) * self.__texture.value(_tex_uv, tex_point)
//         return brdf


//     def get_gl_preview_dict(self):
//         """get material information for OpenGL preview.
//         gl_preview_dict = {'const_bg_color':  float4}
//         \return OpenGL preview data
//         """
//         const_bg_color = numpy.array([0.1, 0.1, 0.1, 1.0]),
//         if(self.__texture.get_classname() == 'ConstantColorTexture'):
//             diffuse_col = self.__texture.value(None, None)
//             const_bg_color = copy.deepcopy(diffuse_col)

//         gl_preview_dict = {'const_bg_color':  const_bg_color}
//         return gl_preview_dict


//     def set_gl_preview_dict(self, gl_preview_dict):
//         """set material information from OpenGL material editor.
//         \param[in] gl_preview_dict
//         """
//         const_bg_color = gl_preview_dict['const_bg_color']
//         self.__texture.set_constant_color(const_bg_color)


// # ----------------------------------------------------------------------

// def material_factory(_mat_dict):
//     """material factory from material information dictionary.
//     \return a material
//     """
//     mat = None
//     mat_type = mat_dict['mat_type']
//     if(mat_type == 'lambert'):
//         # texture and emit color are initialized in initialized_by_dict
//         texture = None
//         emit_color = None
//         mat = DiffuseMaterial(_mat_dict['mat_name'], texture, emit_color)
//         mat.initialize_by_dict(_mat_dict)

//     elif(mat_type == 'environment_constant_color'):
//         emit_color = mat_dict['emit_color']
//         tex = Texture.ConstantColorTexture(numpy_util.str2array(emit_color))
//         mat = EnvironmentMaterial(_mat_dict['mat_name'], tex)
//     else:
//         raise StandardError, ('Unsupported material type [' + mat_type + ']')

//     return mat

} // namespace ifgi

#endif // #ifndef IFGI_CPP_SCENE_IMATERIAL_HH
