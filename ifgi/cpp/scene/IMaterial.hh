//----------------------------------------------------------------------
// ifgi c++ implementation
// Copyright (C) 2010-2012 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief ifgi C++ scene element material interface

#ifndef IFGI_CPP_SCENE_IMATERIAL_HH
#define IFGI_CPP_SCENE_IMATERIAL_HH

#include <string>
#include <cpp/base/Vector.hh>
#include <cpp/base/Exception.hh>

namespace ifgi {
//----------------------------------------------------------------------
// forward declaration
class Dictionary;
class OrthonomalBasis;
class SamplerUnitHemisphereUniform; // FIXME

//----------------------------------------------------------------------
/// material interface
class IMaterial
{
public:
    /// constructor
    IMaterial();
    /// destructor
    virtual ~IMaterial();

    /// get class name. interface method.
    /// \return class name
    virtual std::string get_classname() const = 0;

    /// get material name
    /// \return material name (should be unique)
    virtual std::string get_material_name() const = 0;

    // initialize by dictionary. This doesn't fit C++. Ownership of
    // texture should be outside of material. Therefore, I should not
    // create texture here.
    //
    // \param[in] _mat_dict material parameter dictionary
    // virtual void initialize_by_dict(Dictionary const & mat_dict);

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
        ) const
    {
        assert(this->is_emit());
        throw Exception("IMaterial::emit_radiance: not supported");
    }

    /// ambient response
    ///
    /// \param[in] hit_onb hit point orthonomal basis
    /// \param[in] incident_dir incident direction
    /// \param[in] tex_point texture 3d point (if solid)
    /// \param[in] tex_uv    texture uv coordinate (if surface)
    /// \return ambient responce
    virtual Color ambient_response(//_hit_onb, incident_dir, tex_point, tex_uv
        ) const
    {
        throw Exception("IMaterial::ambient_response: not supported");
    }


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
        ) const
    {
        throw Exception("IMaterial::explicit_brdf: not supported");
    }

    /// explicit brdf
    ///
    /// \param[in] hit_onb hit point orthonomal basis
    /// \param[in] incident_dir incident direction
    /// \param[in] hemisphere_sampler   uniform sampler on a hemisphere
    /// \return outgoing vector
    virtual Scalar_3 diffuse_direction(
        OrthonomalBasis const & hit_onb,
        Scalar_3 const & incident_dir,
        SamplerUnitHemisphereUniform * p_hemisphere_sampler) const
    {
        assert(this->is_diffuse());
        throw Exception("IMaterial::diffuse_direction: not supported");
        return Scalar_3();
    }

    /// explicit brdf
    ///
    /// \param[in] hit_onb hit point orthonomal basis
    /// \param[in] incident_dir incident direction
    /// \param[in] tex_point texture 3d point (if solid)
    /// \param[in] tex_uv    texture uv coordinate (if surface)
    /// \param[in,out] rnd_seed randomnumber seed
    /// \param[out] tex_color texture color
    /// \param[out] v_out outgoing vector?
    virtual Scalar_3 specular_direction(//hit_onb, incident_dir, tex_point, tex_uv,
        // rnd_seed, tex_color, v_out
        ) const
    {
        assert(this->is_specular());
        throw Exception("IMaterial::specular_direction: not supported");
        return Scalar_3();
    }

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
    virtual Scalar_3 transmission_direction(//_hit_onb, incident_dir, tex_point, tex_uv,
                                             //rnd_seed, ext_color, fresnel_scale, v_out);
        ) const
    {
        assert(this->is_transmissive());
        throw Exception("IMaterial::transmission_direction: not supported");
        return Scalar_3();
    }

    /// is diffuse?
    /// \return true when diffuse
    virtual bool is_diffuse() const = 0;

    /// is specular?
    /// \return true when specular
    virtual bool is_specular() const = 0;

    /// is transmissive?
    /// \return true when transmissive
    virtual bool is_transmissive() const = 0;


    // def get_gl_preview_dict();

    // def set_gl_preview_dict(self, gl_preview_dict);
};

} // namespace ifgi
#endif // #ifndef IFGI_CPP_SCENE_IMATERIAL_HH
