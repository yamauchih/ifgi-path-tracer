//----------------------------------------------------------------------
// ifgi c++ implementation: DiffuseMaterial
// Copyright (C) 2010-2011 Yamauchi, Hitoshi
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
    // super(DiffuseMaterial, self).__init__(_mat_name)

    // self.__texture = _texture
    // self.__emit_color = None
    // self.set_emit_color(_emit_color)


    /// initialize by dictionary
    ///
    /// \param[in] _mat_dict material parameter dictionary
    void initialize_by_dict(Dictionary const & mat_dict);

    // mat_dict_copy = copy.deepcopy(_mat_dict);
    // /// mandatory parameters
    // mkey = ["mat_type", "mat_name", "diffuse_color"]
    // if not(ifgi_util.has_dict_all_key(mat_dict_copy, mkey)){
    //     missing_keys = ifgi_util.get_dict_missing_key(mat_dict_copy, mkey);
    //     raise StandardError, ("missing parameter of lambert material [" + 
        //                               str(missing_keys) + "]");
        // /// material type and name
        // assert(mat_dict_copy["mat_type"] == "lambert");
        // mat_dict_copy.pop("mat_type");
        // assert(mat_dict_copy["mat_name"] == this->get_material_name());
        // mat_dict_copy.pop("mat_name");

        // /// diffuse color
        // diffuse_color = mat_dict_copy["diffuse_color"]
        // this->__texture = Texture.ConstantColorTexture(numpy_util.str2array(diffuse_color));
        // mat_dict_copy.pop("diffuse_color");

        // /// optional parameters
        // if mat_dict_copy.has_key("emit_color"){
        //     emit_color = numpy_util.str2array(mat_dict_copy["emit_color"]);
        //     this->set_emit_color(emit_color);
        //     mat_dict_copy.pop("emit_color");
        //     print "DEBUG: this lambert material has emit_color ", this->__emit_color

        // if len(mat_dict_copy) > 0:
        //     print mat_dict_copy
        //     raise StandardError, ("_mat_dict has unknown parameters." + str(mat_dict_copy));


    /// set emit color
    ///
    /// \param[in] emit_color emit radiance color. When all zeros, no
    /// emit.
    void set_emit_color(Color const & emit_color);
    // this->__emit_color = None
    // zero4 = numpy.zeros(4);
    // /// None or all zeros => None
    // if (_emit_color == None) or all(_emit_color == zero4){
    //     return

    // if not(all(_emit_color >= zero4)){
    //     raise StandardError, ("emit color components must be >= 0");

    // this->__emit_color = _emit_color

    /// get texture
    /// \return reference to the texture
    ITexture * peek_texture() const;
    // ///
    // return this->__texture

public:

    /// \name implementation of IMaterial
    /// @{

    /// get class name..
    /// \return "DiffuseMaterial"
    virtual std::string get_classname();
    // ///
    // return "DiffuseMaterial"

    /// is emit light?.
    /// \return true when emit light.
    virtual bool is_emit() const;
    // ///
    // return this->__emit_color != None

    /// emitting radiance color
    ///
    /// \param[in] _hit_onb hit point orthonomal basis
    /// \param[in] _light_out_dir outgoing direction from the light
    /// \param[in] _tex_point texture 3d point (if solid)
    /// \param[in] _tex_uv    texture uv coordinate (if surface)
    /// \param[out] _out_emit_rad (output) emit radiance
    virtual void emit_radiance(//_hit_onb, _light_out_dir, _tex_point, _tex_uv
        Color & out_emit_rad
        ) const ;
    // return this->__emit_color

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
    ///
    // return this->__texture.value(_tex_uv, _tex_point)


    /// explicit brdf
    /// \param[in] hit_onb hit point orthonomal basis
    /// \param[in] out_v0  outgoing vector v0
    /// \param[in] out_v1  outgoing vector v1
    /// \param[in] tex_point texture 3d point (if solid);
    /// \param[in] tex_uv    texture uv coordinate (if surface);
    /// \param[out] out_brdf  (output) brdf
    virtual void explicit_brdf(// _hit_onb, _out_v0, _out_v1, _tex_point, _tex_uv
        Color & out_brdf
        );

    // ///
    // brdf = (1/math.pi) * this->__texture.value(_tex_uv, _tex_point);
    // return brdf


    /// explicit brdf
    /// \param[in] _hit_onb hit point orthonomal basis
    /// \param[in] _incident_dir incident direction
    /// \param[in] _hemisphere_sampler uniform sampler on a hemisphere
    /// \param[out] _v_out outgoing vector?
    ///
    /// \return outgoing direction, None if not supported
    virtual Float32_3 diffuse_direction(// _hit_onb, _incident_dir, _hemisphere_sampler
        ) const ;
    // v_on_hs = _hemisphere_sampler.get_sample();
    // v_out   = 
    //     v_on_hs[0] * _hit_onb.u() +
    //     v_on_hs[1] * _hit_onb.v() +
    //     v_on_hs[2] * _hit_onb.w();

    // /// need normalize?
    // assert(abs(numpy.linalg.norm(v_out) - 1.0) < 0.00001);

    // return v_out


    /// def specular_direction(_hit_onb, _incident_dir, _tex_point, _tex_uv,
    ///                           _rnd_seed, _tex_color, _v_out){


    /// def transmission_direction(_hit_onb, _incident_dir, _tex_point, _tex_uv,
    ///                           _rnd_seed, _ext_color, _fresnel_scale, _v_out){

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
