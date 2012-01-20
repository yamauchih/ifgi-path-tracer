//----------------------------------------------------------------------
// ifgi C++ implementation
// Copyright (C) 2010-2012 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief ifgi render C++ implementation

#include "ifgi_cpp_render.hh"

#include <stdexcept>
#include <iostream>
#include <cpp/base/Exception.hh>
#include <cpp/base/ILog.hh>
#include <cpp/scene/SceneGraphNode.hh>
#include <cpp/scene/SceneDB.hh>
#include <cpp/scene/MaterialFactory.hh>
#include <cpp/scene/SGMaterialNode.hh>
#include <cpp/scene/SGPrimitiveNode.hh>
#include <cpp/scene/TriMesh.hh>

namespace ifgi {
//----------------------------------------------------------------------
// constructor
IfgiCppRender::IfgiCppRender()
    :
    m_p_mat_group_node_ref(0),
    m_p_mesh_group_node_ref(0)
{
    // empty
}

//----------------------------------------------------------------------
// destructor
IfgiCppRender::~IfgiCppRender()
{
    this->clear_scene();
}

//----------------------------------------------------------------------
// initialize ifgi
int IfgiCppRender::initialize()
{
    ILog::instance()->set_output_level(ILog::ILog_Debug);

    return 0;
}

//----------------------------------------------------------------------
// shutdown
int IfgiCppRender::shutdown()
{
    return 0;
}

//----------------------------------------------------------------------
// create a new scene.
void IfgiCppRender::create_simple_scenegraph()
{
    if(m_scene_graph.peek_root_node() != 0){
        throw Exception("The scene is not empty! Double creation?");
    }

    // create simple scenegraph structure
    SceneGraphNode * p_rootsg = new SceneGraphNode("rootsg");
    SceneDB::instance()->store_sgnode(p_rootsg);

    // "materialgroup" is a special group.
    assert(m_p_mat_group_node_ref == 0);
    m_p_mat_group_node_ref = new SceneGraphNode("materialgroup");
    SceneDB::instance()->store_sgnode(m_p_mat_group_node_ref);

    p_rootsg->append_child(m_p_mat_group_node_ref);

    // geometry group
    m_p_mesh_group_node_ref = new SceneGraphNode("meshgroup");
    SceneDB::instance()->store_sgnode(m_p_mesh_group_node_ref);

    p_rootsg->append_child(m_p_mesh_group_node_ref);
}

//----------------------------------------------------------------------
// add a material to the scene via Dictionary
void IfgiCppRender::add_material_to_scene_by_dict(Dictionary const & mat_dict)
{
    IMaterial * p_mat = new_material_factory(mat_dict);
    SGMaterialNode * p_ch_mat_sgnode =
        new SGMaterialNode("matnode::" + p_mat->get_material_name());
    p_ch_mat_sgnode->set_material(p_mat);
    SceneDB::instance()->store_sgnode(p_ch_mat_sgnode);

    // put it under the material groupnode.
    // But currently this is not used. Material lookup through the
    // SceneDB.
    assert(m_p_mat_group_node_ref != 0);
    m_p_mat_group_node_ref->append_child(p_ch_mat_sgnode);

    ILog::instance()->
        debug("IfgiCppRender::add_material_to_scene_by_dict: "
              "added material " + p_mat->get_classname() + "::" +
              p_mat->get_material_name() + "\n");
}

//----------------------------------------------------------------------
// add a trimesh to the scene. This object takes the ownership.
void IfgiCppRender::add_trimesh_to_scene(std::string const geo_name,
                                         std::string const mat_name,
                                         TriMesh * p_tmesh)
{
    Sint32 const matidx = SceneDB::instance()->get_material_index_by_name(mat_name);
    if(matidx < 0){
        ILog::instance()->warn(mat_name + " is not found in SceneDB. [" +
                               geo_name + "] has no material reference.");
    }
    p_tmesh->set_material_index(matidx);
    m_p_trimesh_vec.push_back(p_tmesh); // owner: keep the reference

    std::cout << "DEBUG: trimesh info\n"
              << p_tmesh->get_info_summary() << std::endl;

    // this class has the ownership of scenegraph nodes
    SGPrimitiveNode * p_ch_node = new SGPrimitiveNode(geo_name, p_tmesh);
    m_p_sgnode_vec.push_back(p_ch_node); // owner: keep the reference
    m_p_mesh_group_node_ref->append_child(p_ch_node);
}


//----------------------------------------------------------------------
// set camera.
void IfgiCppRender::set_camera_dict(Dictionary const & camera_dict)
{
    camera_dict.write(std::cout, "set_camera_pydict: ");
    assert(camera_dict.is_defined("cam_name"));
    m_camera.set_config_dict(camera_dict);
    m_scene_graph.set_current_camera(m_camera);
}

//----------------------------------------------------------------------
// get camera.
Dictionary IfgiCppRender::get_camera_dict() const
{
    Dictionary const cpp_dict = m_camera.get_config_dict();
    return cpp_dict;
}

//----------------------------------------------------------------------
// prepare rendering
int IfgiCppRender::prepare_rendering()
{
    // put framebuffers
    this->setup_framebuffer();

    return 0;
}

//----------------------------------------------------------------------
// render frame
int IfgiCppRender::render_n_frame(Sint32 max_frame, Sint32 save_per_frame)
{
    assert(max_frame > 0);
    assert(save_per_frame > 0);

    for(int i = 0; i < max_frame; ++i){
        this->render_single_frame();
        std::stringstream sstr;
        sstr << "frame: " << i;
        ILog::instance()->info(sstr.str());
        if((i != 0) && ((i % save_per_frame) == 0)){
            this->save_frame(i);
        }
    }
    this->save_frame(0);

    return 0;
}

//----------------------------------------------------------------------
// clear the scene
void IfgiCppRender::clear_scene()
{
    this->clear_trimesh_memory();
    this->clear_node_memory();
}

//----------------------------------------------------------------------
// clear scene node memory
void IfgiCppRender::clear_node_memory()
{
    for(std::vector< SceneGraphNode * >::iterator si = m_p_sgnode_vec.begin();
        si != m_p_sgnode_vec.end(); ++si)
    {
        delete *(si);
        *(si) = 0;
    }
    m_p_sgnode_vec.clear();
}

//----------------------------------------------------------------------
// clear trimesh memory
void IfgiCppRender::clear_trimesh_memory()
{
    for(std::vector< TriMesh * >::iterator ti = m_p_trimesh_vec.begin();
        ti != m_p_trimesh_vec.end(); ++ti)
    {
        delete *(ti);
        *(ti) = 0;
    }
    m_p_trimesh_vec.clear();
}

//----------------------------------------------------------------------
// set up framebuffer in the camera
void IfgiCppRender::setup_framebuffer()
{
    // from camera
    // Sint32 const res_x = m_camera.get_resolution_x();
    // Sint32 const res_y = m_camera.get_resolution_y();
    std::cerr << "IfgiCppRender::setup_framebuffer: NIN" << std::endl;
}

//----------------------------------------------------------------------
// render single frame.
Sint32 IfgiCppRender::render_single_frame()
{
    std::cerr << "IfgiCppRender::render_single_frame: NIN" << std::endl;
    return 1;
}

//----------------------------------------------------------------------
// save a frame
Sint32 IfgiCppRender::save_frame(Sint32 frame_count)
{
    std::cerr << "IfgiCppRender::save_frame: NIN" << std::endl;
    return 1;
}

//----------------------------------------------------------------------
} // namespace ifgi