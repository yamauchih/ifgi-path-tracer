//----------------------------------------------------------------------
// ifgi c++ implementation: DiffuseMaterial
// Copyright (C) 2010-2012 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief diffuse material

#include "DiffuseMaterial.hh"

#include <cpp/base/Exception.hh>
#include <cpp/base/Dictionary.hh>

#include "ITexture.hh"

namespace ifgi {

//----------------------------------------------------------------------
// default constructor
DiffuseMaterial::DiffuseMaterial(std::string const & mat_name,
                                 ITexture * p_tex_ref,
                                 Color const & emit_color)
    :
    m_material_name(mat_name),
    m_is_emit_color(false),
    m_emit_color(0.0, 0.0, 0.0, 0.0),
    m_p_texture_ref(p_tex_ref)
{
    this->set_emit_color(emit_color);
}

//----------------------------------------------------------------------
// set emit color
void DiffuseMaterial::set_emit_color(Color const & emit_color)
{
    // all zeros -> no emit
    if(emit_color == Color(0.0, 0.0, 0.0, 0.0)){
        m_emit_color = emit_color;
        m_is_emit_color = false;
        return;
    }

    for(int i = 0; i < m_emit_color.dim(); ++i){
        if(m_emit_color[i] < 0.0){
            throw Exception("DiffuseMaterial::set_emit_color: illegal emit color. "
                            "minus emission.");
        }
    }

    m_emit_color = emit_color;
}


//----------------------------------------------------------------------
// get texture
ITexture * DiffuseMaterial::peek_texture() const
{
    return m_p_texture_ref;
}

//----------------------------------------------------------------------
// get class name
std::string DiffuseMaterial::get_classname() const
{
    return std::string("DiffuseMaterial");
}

//----------------------------------------------------------------------
// get material name
std::string DiffuseMaterial::get_material_name() const
{
    return m_material_name;
}

// //----------------------------------------------------------------------
// // initialize by dictionary
// void DiffuseMaterial::initialize_by_dict(Dictionary const & mat_dict)
// {
//     Dictionary mat_dict_copy = mat_dict;

//     // mandatory parameters
//     // mkey = ["mat_type", "mat_name", "diffuse_color"];
//     // if(!(ifgi_util.has_dict_all_key(mat_dict_copy, mkey))){
//     //     missing_keys = ifgi_util.get_dict_missing_key(mat_dict_copy, mkey);
//     //     raise StandardError, ("missing parameter of lambert material [" +
//     //                           str(missing_keys) + "]");
//     // }
//     char const * p_mandatory_key[] = { "mat_type",
//                                        "mat_name",
//                                        "diffuse_color",
//                                        0};
//     std::vector< std::string > undef_keys;
//     if(!(is_all_key_defined(mat_dict_copy, p_mandatory_key, & undef_keys))){
//         std::stringstream sstr;
//         std::copy(undef_keys.begin(), undef_keys.end(),
//                   std::ostream_iterator< std::string >(sstr, " "));
//         throw Exception("missing parameter of lambert material [" + sstr.str() + "]");
//     }

//     // material type and name
//     assert(mat_dict_copy["mat_type"] == "lambert");
//     mat_dict_copy.erase("mat_type");
//     assert(mat_dict_copy["mat_name"] == this->get_material_name());
//     mat_dict_copy.erase("mat_name");

//     // diffuse color
//     Color diffuse_color = mat_dict_copy.get< Color >("diffuse_color");
//     m_texture = Texture.ConstantColorTexture(numpy_util.str2array(diffuse_color));
//     mat_dict_copy.pop("diffuse_color");

//     // optional parameters
//     if(mat_dict_copy.has_key("emit_color")){
//         emit_color = numpy_util.str2array(mat_dict_copy["emit_color"]);
//         this->set_emit_color(emit_color);
//         mat_dict_copy.pop("emit_color");
//         print "DEBUG: this lambert material has emit_color ", this->__emit_color;
//     }

//     if(len(mat_dict_copy) > 0){
//         print mat_dict_copy;
//         raise StandardError, ("_mat_dict has unknown parameters." + str(mat_dict_copy));
//     }
// }

//----------------------------------------------------------------------
// is emit light?.
bool DiffuseMaterial::is_emit() const
{
    return m_is_emit_color;
}

//----------------------------------------------------------------------
// emitting radiance color
void DiffuseMaterial::emit_radiance(// _hit_onb, _light_out_dir, _tex_point, _tex_uv
    Color & out_emit_rad
    ) const
{
    out_emit_rad = m_emit_color;
}

//----------------------------------------------------------------------
// ambient response
void DiffuseMaterial::ambient_response(// _hit_onb, _incident_dir, _tex_point, _tex_uv
    Color & out_amb_res
    ) const
{
    out_amb_res = m_p_texture_ref->value(); // _tex_uv, _tex_point);
}

//----------------------------------------------------------------------
// explicit brdf
void DiffuseMaterial::explicit_brdf(// _hit_onb, _out_v0, _out_v1, _tex_point, _tex_uv
    Color & out_brdf
    ) const
{
    // 1/pi * pho
    out_brdf = Scalar(M_1_PI) * m_p_texture_ref->value(); //_tex_uv, _tex_point
}

//----------------------------------------------------------------------
// explicit brdf
Scalar_3 DiffuseMaterial::diffuse_direction(// _hit_onb, _incident_dir, _hemisphere_sampler
    ) const
{
    // v_on_hs = _hemisphere_sampler.get_sample();
    // v_out =
    //     v_on_hs[0] * _hit_onb.u() +
    //     v_on_hs[1] * _hit_onb.v() +
    //     v_on_hs[2] * _hit_onb.w();

    // // need normalize?
    // assert(abs(numpy.linalg.norm(v_out) - 1.0) < 0.00001);

    std::cout << "NIN DiffuseMaterial::diffuse_direction" << std::endl;

    return Scalar_3();
}

//----------------------------------------------------------------------
// def specular_direction(_hit_onb, _incident_dir, _tex_point, _tex_uv,
//                           _rnd_seed, _tex_color, _v_out)

//----------------------------------------------------------------------
// def transmission_direction(_hit_onb, _incident_dir, _tex_point, _tex_uv,
///                           _rnd_seed, _ext_color, _fresnel_scale, _v_out)


//----------------------------------------------------------------------
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

//----------------------------------------------------------------------
// def set_gl_preview_dict(_gl_preview_dict){
//     /// set material information from OpenGL material editor.
//     \param[in] _gl_preview_dict
//     ///
//     /// fg_color    = _gl_preview_dict["fg_color"]
//     diffuse_col = _gl_preview_dict["diffuse"]
//     this->__texture.set_constant_color(diffuse_col);

} // namespace ifgi
