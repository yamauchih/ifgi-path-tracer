//----------------------------------------------------------------------
// ifgi c++ implementation: EnvironmentMaterial.hh
// Copyright (C) 2010-2011 Yamauchi, Hitoshi
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

    // ///
    // super(EnvironmentMaterial, ).__init__(_mat_name);
    // this->__texture = texture


    /// get class name..
    /// \return get this class name
    virtual std::string get_classname() const;
    ///
    // return "EnvironmentMaterial"


    /// def is_emit(){
    ///     /// is emit light?.
    ///     \return true when emit light.
    ///     ///
    ///     return False
    /// def emit_radiance(_hit_onb, light_out_dir, tex_point, tex_uv){

    /// peek texture
    ITexture * peek_texture();
    // return this->__texture

    /// ambient response
    ///
    /// \param[in] hit_onb hit point orthonomal basis
    /// \param[in] incident_dir incident direction
    /// \param[in] tex_point texture 3d point (if solid)
    /// \param[in] tex_uv    texture uv coordinate (if surface)
    /// \param[out] out_amb_res  (output) ambient responce
    virtual void ambient_response(//_hit_onb, incident_dir, tex_point, tex_uv
        Color & out_amb_res
        );
    ///
    /// return this->__texture.value(_tex_uv, tex_point);


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
        );

        // ///
        // brdf = (1/math.pi) * this->__texture.value(_tex_uv, tex_point);
        // return brdf

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
private:
    /// material name
    std::string m_material_name;
    ///
    ITexture * m_p_texture_ref;
};

//----------------------------------------------------------------------

// IMaterial * material_factory(Dictionary const & mat_dict){
//     /// material factory from material information dictionary.
//     \return a material
//     ///
//     mat = None
//     mat_type = mat_dict["mat_type"]
//     if(mat_type == "lambert"){
//         /// texture and emit color are initialized in initialized_by_dict
//         texture = None
//         emit_color = None
//         mat = DiffuseMaterial(_mat_dict["mat_name"], texture, emit_color);
//         mat.initialize_by_dict(_mat_dict);

//     elif(mat_type == "environment_constant_color"){
//         emit_color = mat_dict["emit_color"]
//         tex = Texture.ConstantColorTexture(numpy_util.str2array(emit_color));
//         mat = EnvironmentMaterial(_mat_dict["mat_name"], tex);
//     else:
//         raise StandardError, ("Unsupported material type [" + mat_type + "]");

//     return mat

} // namespace ifgi

#endif // #ifndef IFGI_CPP_SCENE_ENVIRONMENTMATERIAL_HH
