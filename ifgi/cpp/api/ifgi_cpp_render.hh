//----------------------------------------------------------------------
// ifgi c++ implementation
// Copyright (C) 2010-2012 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief ifgi render api for C++ implementation
#ifndef IFGI_PATH_TRACER_IFGI_CPP_API_IFGI_CPP_RENDER_HH
#define IFGI_PATH_TRACER_IFGI_CPP_API_IFGI_CPP_RENDER_HH

// boost
#include <boost/python.hpp>
#include <boost/python/object.hpp>
#include <vector>
#include <map>

// ifgi
#include <cpp/base/Dictionary.hh>
#include <cpp/scene/SceneGraph.hh>

namespace ifgi {

class SceneGraph;
class TriMesh;

//----------------------------------------------------------------------
/// append python dictionary list to cpp dictionary vector
///
/// \param[out] cpp_dictionary_vec (output) cpp dictionary vector. The
/// entry will be appended to this vector.
/// \param[in]  pydict_list python dictionary list
extern void append_pydict_list_to_dictionary_vec(
    std::vector< Dictionary > & cpp_dictionary_vec,
    boost::python::object const & pydict_list);

//----------------------------------------------------------------------
/// ifgi C++ rendering core interface
///
/// Typical usage.
/// - construct this object
/// - initialize() this object
/// - create_scene()
/// - set_camera_dict() ... may call several times
/// - render()
class IfgiCppRender
{
public:
    /// constructor
    IfgiCppRender();

    /// destructor
    ~IfgiCppRender();

    /// initialize ifgi
    /// \return 0 when succeeded
    int initialize();

    /// clear the scene
    void clear_scene();

    /// create a new scene.
    ///
    /// SceneGraph structure.
    ///
    /// SceneGraph +
    ///            +--+ SceneGraphNode: 'rootsg' root_node
    ///                              +--+ CameraNode: 'main_cam' camera
    ///                              +--+ SceneGraphNode: 'materialgroup'
    ///                                                +--+ Material: 'mat0'
    ///                                                +--+ Material: 'mat1'
    ///                                                   ...
    ///                              +--+ SceneGraphNode: 'meshgroup'
    ///                                                +--+ TriMesh: 'trimesh0'
    ///                                                +--+ TriMesh: 'trimesh1'
    ///                                                   ...
    ///
    /// \param[in] mat_dict_list  material dictionary list
    /// \param[in] geom_dict_list geometry dictionary list
    /// \param[in] camera_dict    camera dictionary
    void create_scene(boost::python::object const & mat_dict_list,
                      boost::python::object const & geom_dict_list,
                      boost::python::object const & camera_dict);

    /// set camera. replaced all the data.
    ///
    /// \param[in] camera_pydict_obj camera dictionary
    void set_camera_pydict(boost::python::object const & camera_pydict_obj);

    /// get camera.
    ///
    /// \return get current camera
    boost::python::object get_camera_pydict() const;

private:
    /// clear scene node memory
    void clear_node_memory();
    /// clear trimesh memory
    void clear_trimesh_memory();

    /// add material to the scene
    /// \param[in] p_mat_group_node material group node. All the
    /// materials are this node's children.
    /// \param[in] mat_dict_list material python dict list
    void add_material_to_scene(
        SceneGraphNode * p_mat_group_node,
        boost::python::object const & mat_dict_list);

    /// add geometry to the scene
    ///
    /// \param[in] p_mesh_group_node mesh group node. Currently all
    /// the meshes are this node's children.
    /// \param[in] geom_dict_list geometry python dict list
    void add_geometry_to_scene(
        SceneGraphNode * p_mat_group_node,
        boost::python::object const & geom_dict_list);

    /// add one primitive to the scene
    void add_one_geometry_to_scene(
        SceneGraphNode * p_mesh_group_node,
        boost::python::dict const & geom_pydict);


private:
    /// geometry, reference to the trimesh, vector
    std::vector< TriMesh * > m_p_trimesh_vec;
    /// reference to the scene graph nodes
    std::vector< SceneGraphNode * > m_p_sgnode_vec;
    /// the scene graph
    SceneGraph m_scene_graph;
    /// current camera
    Camera m_camera;
};

} // namespace ifgi

#endif // #ifndef IFGI_PATH_TRACER_IFGI_CPP_API_IFGI_CPP_RENDER_HH
