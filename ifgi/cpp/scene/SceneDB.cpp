//----------------------------------------------------------------------
// ifgi c++ implementation: SceneDB.hh
// Copyright (C) 2010-2011 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief scene database. a simple object tracker.

#include "SceneDB.hh"

#include "ITexture.hh"
#include "IMaterial.hh"

namespace ifgi {
//----------------------------------------------------------------------
// singleton instance implementation
SceneDB * SceneDB::G_p_scene_db = 0;

//----------------------------------------------------------------------
// destructor
SceneDB::~SceneDB()
{
    this->clear();
}

//----------------------------------------------------------------------
// store texture
Tag SceneDB::store_texture(ITexture * p_tex)
{
    Tag ret_tag = static_cast< Tag >(m_texture_vec.size());
    m_texture_vec.push_back(p_tex);
    return ret_tag;
}

//----------------------------------------------------------------------
// store material
Tag SceneDB::store_material(IMaterial * p_mat)
{
    Tag ret_tag = static_cast< Tag >(m_material_vec.size());
    m_material_vec.push_back(p_mat);
    return ret_tag;
}

//----------------------------------------------------------------------
// clear the memory
void SceneDB::clear()
{
    // delete textures
    for(std::vector< ITexture * >::iterator ti = m_texture_vec.begin();
        ti != m_texture_vec.end(); ++ti)
    {
        delete (*ti);
        (*ti) = 0;
    }
    m_texture_vec.clear();

    // delete materials
    for(std::vector< IMaterial * >::iterator mi = m_material_vec.begin();
        mi != m_material_vec.end(); ++mi)
    {
        delete (*mi);
        (*mi) = 0;
    }
    m_material_vec.clear();
}

//----------------------------------------------------------------------
// constructor. singleton
SceneDB::SceneDB()
{
    // empty
}

//----------------------------------------------------------------------
} // namespace ifgi
