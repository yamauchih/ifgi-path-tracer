//----------------------------------------------------------------------
// ifgi c++ implementation: SceneDB.hh
// Copyright (C) 2010-2011 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief scene database. a simple object tracker.
#ifndef IFGI_PATH_TRACER_IFGI_CPP_SCENE_SCENEDB_HH
#define IFGI_PATH_TRACER_IFGI_CPP_SCENE_SCENEDB_HH

#include <vector>
#include <string>
#include <map>

#include <cpp/base/types.hh>

namespace ifgi {
//----------------------------------------------------------------------
// forward declaration
class ITexture;
class IMaterial;
class SceneGraphNode;

/// database element tag
typedef Sint32 Tag;
/// invalid Tag
Tag const NULL_TAG = -1;

//----------------------------------------------------------------------
/// scene database. a simple object tracker. singleton.
///
/// Currently there is no access and edit. This just tracks the new-ed
/// objects and when the program exits, this deletes all the tracking
/// objects.
///
/// Note: A returned Tag is not a global identifier. Only valid in the
/// same kind.
class SceneDB {
public:
    /// get the singleton instance
    /// \return singleton instance
    static SceneDB * instance()
    {
        if(G_p_scene_db == 0){
            G_p_scene_db = new SceneDB();
        }
        return G_p_scene_db;
    }

    /// delete the singleton
    void delete_instance()
    {
        if(G_p_scene_db != 0){
            delete G_p_scene_db;
            G_p_scene_db = 0;
        }
    }

private:
    /// singleton instance
    static SceneDB * G_p_scene_db;

public:
    /// destructor
    virtual ~SceneDB();

    /// store texture. This SceneDB owns the texture object.
    /// \param[in] p_tex pointer to a texture
    /// \return currently no use
    Tag store_texture(ITexture * p_tex);

    /// store material. This SceneDB owns the material object.
    /// \param[in] p_mat pointer to a material
    /// \return currently no use
    Tag store_material(IMaterial * p_mat);

    /// get material index by material name
    ///
    /// \param[in] matname material name
    /// \return index of material array. -1 if not found.
    Sint32 get_material_index_by_name(std::string const & matname) const;

    /// get material by index
    ///
    /// \param[in] matidx material array index
    /// \return pointer to the material
    IMaterial * peek_material(Sint32 matidx);

    /// store scenegraph node. This SceneDB owns the scnegraph node object.
    /// \param[in] p_sgnode pointer to a scene graph node
    /// \return currently no use
    Tag store_sgnode(SceneGraphNode * p_sgnode);

    /// clear the memory
    /// all the pointers will be invalid.
    void clear();

private:
    /// texture vector
    std::vector< ITexture * > m_texture_vec;
    /// material vector
    std::vector< IMaterial * > m_material_vec;
    /// material name -> index map
    std::map< std::string, Sint32 > m_matname_idx_map;
    /// scenegraph node
    std::vector< SceneGraphNode * > m_sgnode_vec;

private:
    /// constructor. singleton
    SceneDB();
private:
    /// copy constructor, never used.
    SceneDB(const SceneDB& _rhs);
    /// operator=, never used.
    SceneDB const & operator=(SceneDB const & rhs);
};

} // namespace ifgi
#endif // #ifndef IFGI_PATH_TRACER_IFGI_CPP_SCENE_SCENEDB_HH
