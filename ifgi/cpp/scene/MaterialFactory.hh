//----------------------------------------------------------------------
// ifgi c++ implementation: MaterialFactory.hh
// Copyright (C) 2010-2012 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief new a material from a material information dictionary
#ifndef IFGI_PATH_TRACER_IFGI_CPP_SCENE_MATERIALFACTORY_HH
#define IFGI_PATH_TRACER_IFGI_CPP_SCENE_MATERIALFACTORY_HH

#include "IMaterial.hh"
#include "cpp/base/Dictionary.hh"

namespace ifgi
{
//----------------------------------------------------------------------
// material factory
extern IMaterial * new_material_factory(Dictionary const & mat_dict);

//----------------------------------------------------------------------
} // namespace ifgi
#endif // #ifndef IFGI_PATH_TRACER_IFGI_CPP_SCENE_MATERIALFACTORY_HH
