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

namespace ifgi {
//----------------------------------------------------------------------
// forward declaration
class Dict;

//----------------------------------------------------------------------
/// material interface
class IMaterial
{
public:
    /// constructor
    IMaterial();

    /// get class name. interface method.
    /// \return class name
    virtual std::string get_classname() const;

    /// get material name
    /// \return material name (should be unique)
    virtual std::string get_material_name() const = 0;

    /// initialize by dictionary
    ///
    /// \param[in] _mat_dict material parameter dictionary
    virtual void initialize_by_dict(Dict const & mat_dict);

    /// is this material emit light?
    /// \return true when emit light.
    virtual bool is_emit() const = 0;

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


} // namespace ifgi

#endif // #ifndef IFGI_CPP_SCENE_IMATERIAL_HH
