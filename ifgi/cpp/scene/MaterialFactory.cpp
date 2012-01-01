//----------------------------------------------------------------------
// ifgi c++ implementation: MaterialFactory.hh
// Copyright (C) 2010-2011 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief MaterialFactory.hh
#ifndef IFGI_PATH_TRACER_IFGI_CPP_SCENE_MATERIALFACTORY_HH
#define IFGI_PATH_TRACER_IFGI_CPP_SCENE_MATERIALFACTORY_HH

#include "MaterialFactory.hh"
#include "cpp/base/Exception.hh"
#include "cpp/base/Dictionary.hh"

#include "DiffuseMaterial.hh"
#include "EnvironmentMaterial.hh"

#include "ITexture.hh"
#include "ConstantColorTexture.hh"

namespace ifgi
{
//----------------------------------------------------------------------
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

    std::string const mat_type_str = mat_dict.get("mat_type");
    std::string const mat_name_str = mat_dict.get("mat_name");
    if(mat_type_str == "lambert"){
        // texture and emit color are initialized in initialized_by_dict
        ITexture * p_tex = 0;
        Color emit_color(0.0, 0.0, 0.0, 0.0);
        p_mat = new DiffuseMaterial(mat_name_str, p_tex, emit_color);
        p_mat->initialize_by_dict(mat_dict);
    }
    else if(mat_type_str == "environment_constant_color"){
        std::cout << "NIN: new_material_factory: environment_constant_color" << std::endl;

        Color emit_color(0.0, 0.0, 0.0, 0.0); //  = mat_dict.get("emit_color");
        ITexture * p_tex = new ConstantColorTexture(emit_color);
        p_mat = new EnvironmentMaterial(mat_name_str, p_tex);
    }
    else{
        throw Exception("Unsupported material type [" + mat_type_str + ']');
    }
    return p_mat;
}

//----------------------------------------------------------------------

} // namespace ifgi
#endif // #ifndef IFGI_PATH_TRACER_IFGI_CPP_SCENE_MATERIALFACTORY_HH
