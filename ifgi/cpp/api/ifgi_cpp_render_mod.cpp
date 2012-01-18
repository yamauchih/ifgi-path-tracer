//----------------------------------------------------------------------
// ifgi python api c++ implementation
// Copyright (C) 2010-2011 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief ifgi python render api for C++ implementation

#include "ifgi_cpp_render.hh"

// include boost side
// include ifgi side

/// importing module name is 'IfgiCppRender_mod'
BOOST_PYTHON_MODULE(ifgi_cpp_render_mod)
{
    boost::python::class_<ifgi::IfgiCppRender>("ifgi_cpp_render")
        .def("initialize",
             &ifgi::IfgiCppRender::initialize,
             "initialize ifgi C++ rendering core")
        .def("shutdown",
             &ifgi::IfgiCppRender::shutdown,
             "shutdown ifgi C++ rendering core")
        .def("clear_scene",
             &ifgi::IfgiCppRender::clear_scene,
             "clear the scene.")
        .def("create_scene",
             &ifgi::IfgiCppRender::create_scene,
             "create a scene. add material and geometry dict list, "
             "and a camera to the scene.")
        .def("set_camera_pydict",
             &ifgi::IfgiCppRender::set_camera_pydict,
             "set camera dictionary. Replace the camera (python dictionary).")
        .def("get_camera_pydict",
             &ifgi::IfgiCppRender::get_camera_pydict,
             "get current camera dictionary.")
        .def("prepare_rendering",
             &ifgi::IfgiCppRender::prepare_rendering,
             "prepare rendering. Call this once before render_frame() call.")
        .def("render_frame",
             &ifgi::IfgiCppRender::render_frame,
             "render frames: args: max_frame, save_per_frame.")
        ;
}

