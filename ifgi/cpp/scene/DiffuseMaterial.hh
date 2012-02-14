//----------------------------------------------------------------------
// ifgi c++ implementation: DiffuseMaterial
// Copyright (C) 2010-2012 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief diffuse material
#ifndef IFGI_CPP_SCENE_DIFFUSEMATERIAL_HH
#define IFGI_CPP_SCENE_DIFFUSEMATERIAL_HH

#include <cpp/base/Vector.hh>

#include "IMaterial.hh"

namespace ifgi {
//----------------------------------------------------------------------

// forward declaration
class Dictionary;
class ITexture;

//----------------------------------------------------------------------

/// Diffuse material
class DiffuseMaterial : public IMaterial
{
public:
    /// default constructor
    ///
    /// \param[in] mat_name   material name
    /// \param[in] p_tex_ref  reference to a texture
    /// \param[in] emit_color emittion color
    DiffuseMaterial(std::string const & mat_name,
                    ITexture * p_tex_ref,
                    Color const & emit_color);

    /// set emit color
    ///
    /// \param[in] emit_color emit radiance color. When all zeros, no
    /// emit.
    void set_emit_color(Color const & emit_color);

    /// get texture
    /// \return reference to the texture
    ITexture * peek_texture() const;

public:

    /// \name implementation of IMaterial
    /// @{

    /// get class name..
    /// \return "DiffuseMaterial"
    virtual std::string get_classname() const;

    /// get material name
    /// \return material name (should be unique)
    virtual std::string get_material_name() const;

    /// initialize by dictionary
    ///
    /// \param[in] _mat_dict material parameter dictionary
    // virtual void initialize_by_dict(Dictionary const & mat_dict);

    /// is emit light?.
    /// \return true when emit light.
    virtual bool is_emit() const;

    /// emitting radiance color
    ///
    /// \param[in] _hit_onb hit point orthonomal basis
    /// \param[in] _light_out_dir outgoing direction from the light
    /// \param[in] _tex_point texture 3d point (if solid)
    /// \param[in] _tex_uv    texture uv coordinate (if surface)
    /// \param[out] _out_emit_rad (output) emit radiance
    virtual void emit_radiance(//_hit_onb, _light_out_dir, _tex_point, _tex_uv
        Scalar_4 & out_emit_rad
        ) const ;

    /// ambient response
    ///
    /// \param[in] _hit_onb hit point orthonomal basis
    /// \param[in] _incident_dir incident direction
    /// \param[in] _tex_point texture 3d point (if solid)
    /// \param[in] _tex_uv    texture uv coordinate (if surface)
    /// \param[out] _out_amb_res  (output) ambient responce
    virtual void ambient_response(//_hit_onb, _incident_dir, _tex_point, _tex_uv
        Color & out_amb_res
        ) const;

    /// explicit brdf
    /// \param[in] hit_onb hit point orthonomal basis
    /// \param[in] out_v0  outgoing vector v0
    /// \param[in] out_v1  outgoing vector v1
    /// \param[in] tex_point texture 3d point (if solid);
    /// \param[in] tex_uv    texture uv coordinate (if surface);
    /// \param[out] out_brdf  (output) brdf
    virtual void explicit_brdf(// _hit_onb, _out_v0, _out_v1, _tex_point, _tex_uv
        Color & out_brdf
        ) const;

    /// explicit brdf
    /// \param[in] hit_onb hit point orthonomal basis
    /// \param[in] incident_dir incident direction
    /// \param[in] hemisphere_sampler uniform sampler on a hemisphere
    /// \return outgoing vector
    virtual Scalar_3 diffuse_direction(
        OrthonomalBasis const & hit_onb,
        Scalar_3 const & incident_dir, 
        SamplerUnitHemisphereUniform * p_hemisphere_sampler) const;

    /// is diffuse?
    /// \return true when diffuse
    virtual bool is_diffuse() const      { return true; }

    /// is specular?
    /// \return true when specular
    virtual bool is_specular() const     { return false; }

    /// is transmissive?
    /// \return true when transmissive
    virtual bool is_transmissive() const { return false; }

    /// @}

public:
    // def get_gl_preview_dict(){
    //     /// get material information for OpenGL preview.
    //     gl_preview_dict = {"fg_color":  float4,
    //                        "emission":  float4,
    //                        "diffuse":   float4,
    //                        "ambient":   float4,
    //                        "specular":  float4,
    //                        "shininess": str(float)}
    //     \return OpenGL preview data
    //     ///
    //     fg_color    = numpy.array([0.5, 0.5, 0.5, 1.0]),
    //     diffuse_col = numpy.array([0.5, 0.5, 0.5, 1.0]),
    //     if(this->__texture.get_classname() == "ConstantColorTexture"){
    //         diffuse_col = this->__texture.value(None, None);
    //         fg_color    = copy.deepcopy(diffuse_col);


    //     gl_preview_dict = {"fg_color":  fg_color,
    //                        "emission":  numpy.array([0,0,0,1]),
    //                        "diffuse":   diffuse_col,
    //                        "ambient":   numpy.array([0,0,0,1]),
    //                        "specular":  numpy.array([0,0,0,1]),
    //                        "shininess": str(1.0)}
    //     return gl_preview_dict


    // def set_gl_preview_dict(_gl_preview_dict){
    //     /// set material information from OpenGL material editor.
    //     \param[in] _gl_preview_dict
    //     ///
    //     /// fg_color    = _gl_preview_dict["fg_color"]
    //     diffuse_col = _gl_preview_dict["diffuse"]
    //     this->__texture.set_constant_color(diffuse_col);

private:
    /// material name
    std::string m_material_name;
    /// is emit color?
    bool m_is_emit_color;
    /// emit color. effective only m_is_emit_color == true
    Color m_emit_color;
    /// Texture reference
    ITexture * m_p_texture_ref;
};

} // namespace ifgi
#endif // #ifndef IFGI_CPP_SCENE_DIFFUSEMATERIAL_HH
