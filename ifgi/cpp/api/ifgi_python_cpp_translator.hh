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
    /// add material to the scene
    /// \param[in] mat_dict_list material python dict list
    void add_material_to_scene(
        boost::python::object const & mat_dict_list);

    /// add geometry to the scene
    ///
    /// \param[in] geom_dict_list geometry python dict list
    void add_geometry_to_scene(
        boost::python::object const & geom_dict_list);

    /// add one primitive to the scene
    ///
    /// \param[in] geom_pydict geometry python dict
    void add_one_geometry_to_scene(
        boost::python::dict const & geom_pydict);

private:
    /// rendering core reference
    IfgiCppRender * m_p_render_core;
};

} // namespace ifgi

#endif // #ifndef IFGI_PATH_TRACER_IFGI_CPP_API_IFGI_PYTHON_CPP_TRANSLATOR_HH
