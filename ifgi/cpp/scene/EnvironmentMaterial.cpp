//----------------------------------------------------------------------
// ifgi c++ implementation: EnvironmentMaterial.hh
// Copyright (C) 2010-2011 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief environment material

#include "EnvironmentMaterial.hh"

#include "ITexture.hh"


namespace ifgi {

//----------------------------------------------------------------------
// default constructor
EnvironmentMaterial::EnvironmentMaterial(std::string const & mat_name,
                                         ITexture * p_texture)
    :
    m_material_name(mat_name),
    m_p_texture_ref(p_texture)
{
    // empty
}

//----------------------------------------------------------------------
// get class name..
std::string EnvironmentMaterial::get_classname() const
{
    return "EnvironmentMaterial";
}

//----------------------------------------------------------------------
    /// def is_emit(){
    ///     /// is emit light?.
    ///     \return true when emit light.

//----------------------------------------------------------------------

// def emit_radiance(_hit_onb, light_out_dir, tex_point, tex_uv){

//----------------------------------------------------------------------
// peek texture
ITexture * EnvironmentMaterial::peek_texture()
{
    return m_p_texture_ref;
}

//----------------------------------------------------------------------
// ambient response
void EnvironmentMaterial::ambient_response(//_hit_onb, incident_dir, tex_point, tex_uv
    Color & out_amb_res
    )
{
    out_amb_res = m_p_texture_ref->value();
}

//----------------------------------------------------------------------
// explicit brdf
void EnvironmentMaterial::explicit_brdf(// _hit_onb, out_v0, out_v1, tex_point, tex_uv)
    Color & out_brdf
    )
{
    out_brdf = Float32(M_1_PI) * m_p_texture_ref->value();
}

//----------------------------------------------------------------------
} // namespace ifgi

