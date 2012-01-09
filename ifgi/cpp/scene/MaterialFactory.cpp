//----------------------------------------------------------------------
// ifgi c++ implementation: MaterialFactory.hh
// Copyright (C) 2010-2012 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief MaterialFactory.hh
#ifndef IFGI_PATH_TRACER_IFGI_CPP_SCENE_MATERIALFACTORY_HH
#define IFGI_PATH_TRACER_IFGI_CPP_SCENE_MATERIALFACTORY_HH

#include "MaterialFactory.hh"

#include <iterator>

#include <cpp/base/Dictionary.hh>
#include <cpp/base/Exception.hh>
#include <cpp/base/ILog.hh>

#include "DiffuseMaterial.hh"
#include "EnvironmentMaterial.hh"

#include "ITexture.hh"
#include "ConstantColorTexture.hh"

#include "SceneDB.hh"

namespace ifgi
{
//----------------------------------------------------------------------
/// new and store (to SceneDB) a diffuse material
/// \param[in] mat_dict material parameters for DiffuseMaterial
/// \return created a diffuse material
static DiffuseMaterial * new_store_diffuse_material(
    Dictionary const & mat_dict)
{
    Dictionary mat_dict_copy = mat_dict;

    // mandatory parameters
    char const * p_mandatory_key[] = { "mat_type",
                                       "mat_name",
                                       "diffuse_color",
                                       0};
    std::vector< std::string > undef_keys;
    if(!(is_all_key_defined(mat_dict_copy, p_mandatory_key, & undef_keys))){
        std::stringstream sstr;
        std::copy(undef_keys.begin(), undef_keys.end(),
                  std::ostream_iterator< std::string >(sstr, " "));
        throw Exception("missing parameter of lambert material [" + sstr.str() + "]");
    }

    // material type and name
    assert(mat_dict_copy.get< std::string >("mat_type") == "lambert");
    mat_dict_copy.erase("mat_type");

    std::string const mat_name_str = mat_dict_copy.get< std::string >("mat_name");
    mat_dict_copy.erase("mat_name");

    // diffuse color
    Color diffuse_color = mat_dict_copy.get< Color >("diffuse_color");
    ITexture * p_tex = new ConstantColorTexture(diffuse_color);
    SceneDB::instance()->store_texture(p_tex);
    mat_dict_copy.erase("diffuse_color");

    // optional parameters
    Color emit_color(0.0f, 0.0f, 0.0f, 1.0f);
    if(mat_dict_copy.is_defined("emit_color")){
        emit_color = mat_dict_copy.get< Color >("emit_color");
        mat_dict_copy.erase("emit_color");
        ILog::instance()->debug("DEBUG: this lambert material has emit_color "
                                + Dictionary_value(emit_color).get_string());
    }

    DiffuseMaterial * p_mat = new DiffuseMaterial(mat_name_str, p_tex, emit_color);
    SceneDB::instance()->store_material(p_mat);

    if(!(mat_dict_copy.empty())){
        std::stringstream sstr;
        mat_dict_copy.write(sstr, "Unknown: ");
        throw Exception("mat_dict has unknown parameters.\n" + sstr.str());
    }

    return p_mat;
}

//----------------------------------------------------------------------
/// new and store (to SceneDB) a environment material
/// \param[in] mat_dict material parameters for EnvironmentMaterial
/// \return created a environment material
static EnvironmentMaterial * new_store_environment_material(
    Dictionary const & mat_dict)
{
    Dictionary mat_dict_copy = mat_dict;

    // mandatory parameters
    char const * p_mandatory_key[] = { "mat_type",
                                       "mat_name",
                                       "emit_color",
                                       0};
    std::vector< std::string > undef_keys;
    if(!(is_all_key_defined(mat_dict_copy, p_mandatory_key, & undef_keys))){
        std::stringstream sstr;
        std::copy(undef_keys.begin(), undef_keys.end(),
                  std::ostream_iterator< std::string >(sstr, " "));
        throw Exception("missing parameter of environment material [" +
                        sstr.str() + "]");
    }

    // material type and name
    assert(mat_dict_copy.get< std::string >("mat_type") == "environment_constant_color");
    mat_dict_copy.erase("mat_type");

    std::string const mat_name_str = mat_dict_copy.get< std::string >("mat_name");
    mat_dict_copy.erase("mat_name");

    // emit color
    Color emit_color = mat_dict_copy.get< Color >("emit_color");
    ITexture * p_tex = new ConstantColorTexture(emit_color);
    SceneDB::instance()->store_texture(p_tex);
    mat_dict_copy.erase("emit_color");

    EnvironmentMaterial * p_mat = new EnvironmentMaterial(mat_name_str, p_tex);
    SceneDB::instance()->store_material(p_mat);

    if(!(mat_dict_copy.empty())){
        std::stringstream sstr;
        mat_dict_copy.write(sstr, "Unknown: ");
        throw Exception("mat_dict has unknown parameters.\n" + sstr.str());
    }

    return p_mat;
}

//======================================================================
// material factory
IMaterial * new_material_factory(Dictionary const & mat_dict)
{
    if(!mat_dict.is_defined("mat_type")){
        throw Exception("illegal mat_dict. material dict has no mat_type.");
    }
    if(!mat_dict.is_defined("mat_name")){
        throw Exception("illegal mat_dict. material dict has no mat_name.");
    }

    IMaterial * p_mat = 0;

    std::string const mat_type_str = mat_dict.get< std::string >("mat_type");
    std::string const mat_name_str = mat_dict.get< std::string >("mat_name");
    if(mat_type_str == "lambert"){
        p_mat = new_store_diffuse_material(mat_dict);
    }
    else if(mat_type_str == "environment_constant_color"){
        p_mat = new_store_environment_material(mat_dict);
    }
    else{
        throw Exception("Unsupported material type [" + mat_type_str + ']');
    }
    return p_mat;
}
//----------------------------------------------------------------------
} // namespace ifgi
#endif // #ifndef IFGI_PATH_TRACER_IFGI_CPP_SCENE_MATERIALFACTORY_HH
