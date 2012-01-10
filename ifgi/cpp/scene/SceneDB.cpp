//----------------------------------------------------------------------
// ifgi c++ implementation: SceneDB.hh
// Copyright (C) 2010-2011 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief scene database. a simple object tracker.

#include "SceneDB.hh"

#include "ITexture.hh"
#include "IMaterial.hh"
#include "SceneGraphNode.hh"

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
    std::string const matname = p_mat->get_material_name();

    std::map< std::string, Sint32 >::const_iterator mi =
        m_matname_idx_map.find(matname);
    if(mi != m_matname_idx_map.end()){
        // the matname has already been in the map
        throw Exception("SceneDB::store_material: duplicated material name.");
        return NULL_TAG;
    }

    Sint32 const ret_idx = static_cast< Sint32 >(m_material_vec.size());
    m_matname_idx_map[matname] = ret_idx;
    m_material_vec.push_back(p_mat);

    return static_cast< Tag >(ret_idx);
}

//----------------------------------------------------------------------
// get material index by material name
Sint32 SceneDB::get_material_index_by_name(std::string const & matname) const
{
    std::map< std::string, Sint32 >::const_iterator mi =
        m_matname_idx_map.find(matname);
    if(mi != m_matname_idx_map.end()){
        return mi->second;
    }
    // not found
    return -1;
}

//----------------------------------------------------------------------
// get material by index
IMaterial * SceneDB::peek_material(Sint32 matidx)
{
    assert(matidx >= 0);
    assert(matidx < static_cast< Sint32 >(m_material_vec.size()));

    return m_material_vec[matidx];
}

//----------------------------------------------------------------------
// store scenegraph node. This SceneDB owns the scnegraph node object.
Tag SceneDB::store_sgnode(SceneGraphNode * p_sgnode)
{
    Tag ret_tag = static_cast< Tag >(m_sgnode_vec.size());
    m_sgnode_vec.push_back(p_sgnode);
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
    m_matname_idx_map.clear();

    // delete scenegraph nodes
    for(std::vector< SceneGraphNode * >::iterator si = m_sgnode_vec.begin();
        si != m_sgnode_vec.end(); ++si)
    {
        delete (*si);
        (*si) = 0;
    }
    m_sgnode_vec.clear();
}

//----------------------------------------------------------------------
// constructor. singleton
SceneDB::SceneDB()
{
    // empty
}

//----------------------------------------------------------------------
} // namespace ifgi
