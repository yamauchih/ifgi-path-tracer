//----------------------------------------------------------------------
// ifgi c++ implementation: SceneDB.hh
// Copyright (C) 2010-2011 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief scene database. a simple object tracker.
#ifndef IFGI_PATH_TRACER_IFGI_CPP_SCENE_SCENEDB_HH
#define IFGI_PATH_TRACER_IFGI_CPP_SCENE_SCENEDB_HH

#include <vector>
#include <cpp/base/types.hh>

namespace ifgi {
//----------------------------------------------------------------------
// forward declaration
class ITexture;
class IMaterial;

/// database element tag
typedef Uint32 Tag;

//----------------------------------------------------------------------
/// scene database. a simple object tracker. singleton.
///
/// Currently there is no access and edit. This just tracks the new-ed
/// objects and when the program exits, this deletes all the tracking
/// objects.
class ScendDB {
public:
    /// get the singleton instance
    /// \return singleton instance
    static ScendDB * instance()
    {
        if(G_p_scene_db == 0){
            G_p_scene_db = new ScendDB();
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
    static ScendDB * G_p_scene_db;

public:
    /// destructor
    virtual ~ScendDB();

    /// store texture. This ScendDB owns the texture object.
    /// \param[in] p_tex pointer to a texture
    /// \return currently no use
    Tag store_texture(ITexture * p_tex);

    /// store material. This ScendDB owns the material object.
    /// \param[in] p_mat pointer to a material
    /// \return currently no use
    Tag store_material(IMaterial * p_mat);

    /// clear the memory
    /// all the pointers will be invalid.
    void clear();

private:
    /// texture vector
    std::vector< ITexture * > m_texture_vec;

    /// material vector
    std::vector< IMaterial * > m_material_vec;

private:
    /// constructor. singleton
    ScendDB();
private:
    /// copy constructor, never used.
    ScendDB(const ScendDB& _rhs);
    /// operator=, never used.
    ScendDB const & operator=(ScendDB const & rhs);
};

} // namespace ifgi
#endif // #ifndef IFGI_PATH_TRACER_IFGI_CPP_SCENE_SCENEDB_HH
