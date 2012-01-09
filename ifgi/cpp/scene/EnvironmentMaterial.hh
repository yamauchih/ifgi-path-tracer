//----------------------------------------------------------------------
// ifgi c++ implementation: EnvironmentMaterial.hh
// Copyright (C) 2010-2012 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief environment material
#ifndef IFGI_PATH_TRACER_IFGI_CPP_SCENE_ENVIRONMENTMATERIAL_HH
#define IFGI_PATH_TRACER_IFGI_CPP_SCENE_ENVIRONMENTMATERIAL_HH

#include "IMaterial.hh"

namespace ifgi {
//----------------------------------------------------------------------

// forward declaration
class ITexture;
class Dictionary;

//----------------------------------------------------------------------
/// Environment material
class EnvironmentMaterial : public IMaterial
{
public:
    /// default constructor
    /// \param[in] mat_name material name
    /// \param[in] texture  texture object (consider as emission);
    EnvironmentMaterial(std::string const & mat_name,
                        ITexture * p_texture);

    /// peek texture
    /// \return reference to the texture
    ITexture * peek_texture() const;

public:

    /// \name implementation of IMaterial
    /// @{

    /// get class name.
    /// \return get this class name
    virtual std::string get_classname() const;

    /// get material name
    /// \return material name (should be unique)
    virtual std::string get_material_name() const;

    /// is emit light?.
    /// \return true when emit light.
    virtual bool is_emit() const;

    /// def emit_radiance(_hit_onb, light_out_dir, tex_point, tex_uv){

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

    /// explicit brdf
    ///
    /// \param[in] hit_onb hit point orthonomal basis
    /// \param[in] out_v0  outgoing vector v0
    /// \param[in] out_v1  outgoing vector v1
    /// \param[in] tex_point texture 3d point (if solid)
    /// \param[in] tex_uv    texture uv coordinate (if surface)
    /// \param[out] out_brdf  (output) brdf
    virtual void explicit_brdf(// _hit_onb, out_v0, out_v1, tex_point, tex_uv)
        Color & out_brdf
        ) const;

        // ///
        // brdf = (1/math.pi) * this->__texture.value(_tex_uv, tex_point);
        // return brdf

    /// is diffuse?
    /// \return false. no diffuse direction.
    virtual bool is_diffuse() const      { return false; }

    /// is specular?
    /// \return false. no specular direction.
    virtual bool is_specular() const     { return false; }

    /// is transmissive?
    /// \return false. no transmissive direction.
    virtual bool is_transmissive() const { return false; }

public:
    // def get_gl_preview_dict(){
    //     /// get material information for OpenGL preview.
    //     gl_preview_dict = {"const_bg_color":  float4}
    //     \return OpenGL preview data
    //     ///
    //     const_bg_color = numpy.array([0.1, 0.1, 0.1, 1.0]),
    //     if(this->__texture.get_classname() == "ConstantColorTexture"){
    //         diffuse_col = this->__texture.value(None, None);
    //         const_bg_color = copy.deepcopy(diffuse_col);

    //     gl_preview_dict = {"const_bg_color":  const_bg_color}
    //     return gl_preview_dict


    // def set_gl_preview_dict(_gl_preview_dict){
    //     /// set material information from OpenGL material editor.
    //     \param[in] gl_preview_dict
    //     ///
    //     const_bg_color = gl_preview_dict["const_bg_color"]
    //     this->__texture.set_constant_color(const_bg_color);

    /// @}

private:
    /// material name
    std::string m_material_name;
    /// reference to the texture
    ITexture * m_p_texture_ref;
};

//----------------------------------------------------------------------
} // namespace ifgi
#endif // #ifndef IFGI_CPP_SCENE_ENVIRONMENTMATERIAL_HH
