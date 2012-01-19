//----------------------------------------------------------------------
// ifgi python to cpp translator
// Copyright (C) 2010-2012 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief ifgi python to cpp translator
#ifndef IFGI_PATH_TRACER_IFGI_CPP_API_IFGI_PYTHON_CPP_TRANSLATOR_HH
#define IFGI_PATH_TRACER_IFGI_CPP_API_IFGI_PYTHON_CPP_TRANSLATOR_HH

// boost
#include <boost/python.hpp>
#include <boost/python/object.hpp>
#include <vector>
#include <map>

// ifgi
#include <cpp/base/Dictionary.hh>
#include <cpp/scene/SceneGraph.hh>

namespace ifgi {

// forward declaration
class IfgiCppRender;

// FIXME: necessary?
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
class IfgiPythonCppTranslator
{
public:
    /// constructor
    IfgiPythonCppTranslator();

    /// destructor
    ~IfgiPythonCppTranslator();

    /// initialize ifgi
    /// \return 0 when succeeded
    Sint32 initialize();

    /// shutdown
    /// \return shutdown state. 0 ... success
    Sint32 shutdown();

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

    /// prepare rendering
    ///
    /// \return preparation status. 0 ... success.
    Sint32 prepare_rendering();

    /// render n frames
    ///
    /// \param[in] max_frame max number of frames to render by this call
    /// \param[in] save_per_frame save a frame each save_per_frame
    /// \return rendering status. 0 ... success
    Sint32 render_n_frame(Sint32 max_frame, Sint32 save_per_frame);

private:
    /// clear scene node memory
    // void clear_node_memory();
    // /// clear trimesh memory
    // void clear_trimesh_memory();
//DELETME

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

    // /// set up framebuffer in the camera
    // void setup_framebuffer();

    // /// render single frame.
    // ///
    // /// \return rendering status. 0 ... success
    // Sint32 render_single_frame();

    // /// save a frame
    // ///
    // /// \param[in] frame_count frame counter for this save.
    // /// \return rendering status. 0 ... success
    // Sint32 save_frame(Sint32 frame_count);

private:
    // /// geometry, reference to the trimesh, vector
    // std::vector< TriMesh * > m_p_trimesh_vec;
    // /// reference to the scene graph nodes
    // std::vector< SceneGraphNode * > m_p_sgnode_vec;
    // /// the scene graph
    // SceneGraph m_scene_graph;
    // /// current camera
    // Camera m_camera;


    /// rendering core reference
    IfgiCppRender * m_p_render_core;
};

} // namespace ifgi

#endif // #ifndef IFGI_PATH_TRACER_IFGI_CPP_API_IFGI_PYTHON_CPP_TRANSLATOR_HH
