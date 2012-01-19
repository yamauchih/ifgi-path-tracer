//----------------------------------------------------------------------
// ifgi python to cpp translator module
// Copyright (C) 2010-2012 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief ifgi python to cpp translator python boost module

#include "ifgi_python_cpp_translator.hh"

// include boost side
// include ifgi side

/// importing module name is 'ifgi_python_cpp_translator_mod'
BOOST_PYTHON_MODULE(ifgi_python_cpp_translator_mod)
{
    /// object python constructor is "ifgi_python_cpp_translator"
    /// The C++ class is ifgi::IfgiPythonCppTranslator.
    boost::python::class_<ifgi::IfgiPythonCppTranslator>("ifgi_python_cpp_translator")
        .def("initialize",
             &ifgi::IfgiPythonCppTranslator::initialize,
             "initialize ifgi C++ rendering core")
        .def("shutdown",
             &ifgi::IfgiPythonCppTranslator::shutdown,
             "shutdown ifgi C++ rendering core")
        .def("clear_scene",
             &ifgi::IfgiPythonCppTranslator::clear_scene,
             "clear the scene.")
        .def("create_scene",
             &ifgi::IfgiPythonCppTranslator::create_scene,
             "create a scene. add material and geometry dict list, "
             "and a camera to the scene.")
        .def("set_camera_pydict",
             &ifgi::IfgiPythonCppTranslator::set_camera_pydict,
             "set camera dictionary. Replace the camera (python dictionary).")
        .def("get_camera_pydict",
             &ifgi::IfgiPythonCppTranslator::get_camera_pydict,
             "get current camera dictionary.")
        .def("prepare_rendering",
             &ifgi::IfgiPythonCppTranslator::prepare_rendering,
             "prepare rendering. Call this once before render_frame() call.")
        .def("render_n_frame",
             &ifgi::IfgiPythonCppTranslator::render_n_frame,
             "render n frames: args: max_frame, save_per_frame.")
        ;
}

