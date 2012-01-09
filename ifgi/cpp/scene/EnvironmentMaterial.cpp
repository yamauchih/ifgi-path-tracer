//----------------------------------------------------------------------
// ifgi c++ implementation: EnvironmentMaterial.hh
// Copyright (C) 2010-2012 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief environment material

#include "EnvironmentMaterial.hh"

#include "ITexture.hh"
#include "cpp/base/Dictionary.hh"

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
// peek texture
ITexture * EnvironmentMaterial::peek_texture() const
{
    return m_p_texture_ref;
}

//----------------------------------------------------------------------
// get class name..
std::string EnvironmentMaterial::get_classname() const
{
    return std::string("EnvironmentMaterial");
}

//----------------------------------------------------------------------
// get material name
std::string EnvironmentMaterial::get_material_name() const
{
    return m_material_name;
}

//----------------------------------------------------------------------
// is emit light?.
bool EnvironmentMaterial::is_emit() const
{
    return false;
}

//----------------------------------------------------------------------

// def emit_radiance(_hit_onb, light_out_dir, tex_point, tex_uv){


//----------------------------------------------------------------------
// ambient response
void EnvironmentMaterial::ambient_response(//_hit_onb, incident_dir, tex_point, tex_uv
    Color & out_amb_res
    ) const
{
    out_amb_res = m_p_texture_ref->value();
}

//----------------------------------------------------------------------
// explicit brdf
void EnvironmentMaterial::explicit_brdf(// _hit_onb, out_v0, out_v1, tex_point, tex_uv)
    Color & out_brdf
    ) const
{
    out_brdf = Float32(M_1_PI) * m_p_texture_ref->value();
}

//----------------------------------------------------------------------
} // namespace ifgi

