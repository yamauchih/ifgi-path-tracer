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
    /// \param[in] mat_dict_list  material dictionary list
    /// \param[in] geom_dict_list geometry dictionary list
    /// \param[in] camera_dict    camera dictionary
    void create_scene(boost::python::object const & mat_dict_list,
                      boost::python::object const & geom_dict_list,
                      boost::python::object const & camera_dict);

    /// set camera. replaced all the data.
    ///
    /// \param[in] camera_pydict_obj camera dictionary
    void set_camera_dict(boost::python::object const & camera_pydict_obj);

    /// get camera.
    ///
    /// \return get current camera
    boost::python::object get_camera_dict() const;

private:
    /// clear scene node memory
    void clear_node_memory();

private:
    /// material dictionary vector
    std::vector< Dictionary > m_mat_dict_vec;
    /// geometry dictionary vector
    std::vector< Dictionary > m_geo_dict_vec;
    ///camera dictionary
    Dictionary m_camera_dict;

    /// the scene graph
    SceneGraph m_scene_graph;
};

} // namespace ifgi

#endif // #ifndef IFGI_PATH_TRACER_IFGI_CPP_API_IFGI_CPP_RENDER_HH
