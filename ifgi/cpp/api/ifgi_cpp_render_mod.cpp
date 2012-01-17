//----------------------------------------------------------------------
// ifgi python api c++ implementation
// Copyright (C) 2010-2011 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief ifgi python render api for C++ implementation

#include "ifgi_cpp_render.hh"

// boost side
// #include <boost/python/extract.hpp>

// ifgi side

/// importing module name is 'IfgiCppRender_mod'
BOOST_PYTHON_MODULE(ifgi_cpp_render_mod)
{
    boost::python::class_<ifgi::IfgiCppRender>("ifgi_cpp_render")
        .def("initialize",
             &ifgi::IfgiCppRender::initialize,
             "initialize ifgi C++ rendering core")
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
        ;
}

