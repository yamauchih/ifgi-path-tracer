//----------------------------------------------------------------------
// ifgi c++ implementation
// Copyright (C) 2010-2011 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief ifgi render api for C++ implementation

#include "ifgi_cpp_render_mod.hh"

// boost side
#include <stdexcept>
#include <iostream>
#include <boost/python/extract.hpp>
#include <boost/python/list.hpp>
#include <boost/python/dict.hpp>
#include <boost/python/str.hpp>

// ifgi side


namespace ifgi {

//----------------------------------------------------------------------
/// convert cpp Dictionary to python dict
///
/// \param[in] cpp_dict cpp Dictionary
/// \return python dictionary, but all the value elements are python
/// strings
boost::python::object get_pydict_from_cpp_dictionary(Dictionary const & cpp_dict)
{
    boost::python::dict pydict;
    for(Dictionary::const_iterator di = cpp_dict.begin(); di != cpp_dict.end(); ++di)
    {
        pydict[di->first] = di->second.get_string();
    }

    return pydict;
}

//----------------------------------------------------------------------
/// convert python dict to cpp Dictionary
///
/// \param[in] pydict python dict
/// \return cpp dictionary, but all the value elements are python
/// strings
Dictionary get_cpp_dictionary_from_pydict(boost::python::dict const & pydict)
{
    boost::python::list keylist = pydict.keys();
    Dictionary ret_cpp_dict;

    int const keylen = boost::python::len(keylist);
    for(int i = 0; i <  keylen; ++i){
        std::string const keystr =
            boost::python::extract< std::string >(boost::python::str(keylist[i]));
        std::cout << "DEBUG: list[" << i << "]" << std::endl;

        // get value as a string
        std::string valstr =
            boost::python::extract< std::string >(
                boost::python::str(pydict[keylist[i]]));
        std::cout << "DEBUG:   key:[" << keystr << "]->[" << valstr << "]" << std::endl;

        ret_cpp_dict.set(keystr, valstr);
    }
    return ret_cpp_dict;
}

//----------------------------------------------------------------------
// append python dictionary list to cpp dictionary vector
void append_pydict_list_to_dictionary_vec(
    std::vector< Dictionary > & cpp_dictionary_vec,
    boost::python::object const & pydict_list)
{
    // convert to the extracted object: list
    boost::python::extract< boost::python::list > cpp_list_ext(pydict_list);
    if(!cpp_list_ext.check()){
        throw std::runtime_error(
            "append_pydict_list_to_dictionary_vec: type error: "
            "pydict_list is not a list.");
    }

    boost::python::list cpp_dict_list = cpp_list_ext();
    int const len = boost::python::len(cpp_dict_list);
    // std::cout << "len(dict_list) = " << len << std::endl;
    for(int i = 0; i < len; ++i){
        boost::python::dict pydict =
            boost::python::extract< boost::python::dict >(cpp_dict_list[i]);
        Dictionary const converted_cppdict = get_cpp_dictionary_from_pydict(pydict);
        converted_cppdict.write(std::cout, "DEBUG: CPP Dictionary: ");
        cpp_dictionary_vec.push_back(converted_cppdict);
    }
}

//----------------------------------------------------------------------
// initialize ifgi
int IfgiCppRender::initialize()
{
    this->clear_scene();
    return 0;
}

//----------------------------------------------------------------------
// clear the scene
void IfgiCppRender::clear_scene()
{
    m_mat_dict_vec.clear();
    m_geo_dict_vec.clear();
    m_camera_dict.clear();
}

//----------------------------------------------------------------------
// append a new scene. material and geometry will be added.
void IfgiCppRender::append_scene(boost::python::object mat_dict_list,
                                 boost::python::object geom_dict_list)
{
    append_pydict_list_to_dictionary_vec(m_mat_dict_vec, mat_dict_list);
    append_pydict_list_to_dictionary_vec(m_geo_dict_vec, geom_dict_list);
}

//----------------------------------------------------------------------
// set camera.
void IfgiCppRender::set_camera_dict(boost::python::object camera_pydict_obj)
{
    // object -> extractor
    boost::python::extract< boost::python::dict > cpp_pydict_ext(camera_pydict_obj);
    if(!cpp_pydict_ext.check()){
        throw std::runtime_error("set_camera_dict: type error: "
                                 "camera_pydict_obj is not a dict.");
    }
    Dictionary const cpp_cam_dict = get_cpp_dictionary_from_pydict(cpp_pydict_ext());

    cpp_cam_dict.write(std::cout, "CPPCAM:");
    m_camera_dict.clear();
    m_camera_dict.insert_all(cpp_cam_dict);
}

//----------------------------------------------------------------------
// get camera.
boost::python::object IfgiCppRender::get_camera_dict() const
{
    return get_pydict_from_cpp_dictionary(m_camera_dict);
}

//----------------------------------------------------------------------
// /// return a string object.
// /// \return a string object
// object return_string() const {
//     return str("Incredible, this works.");
// }

//----------------------------------------------------------------------
} // namespace ifgi

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
        .def("append_scene",
             &ifgi::IfgiCppRender::append_scene,
             "append material and geometry dict list to the scene.")
        .def("set_camera_dict",
             &ifgi::IfgiCppRender::set_camera_dict,
             "set camera dictionary. Replace the camera (python dictionary).")
        .def("get_camera_dict",
             &ifgi::IfgiCppRender::get_camera_dict,
             "get current camera dictionary.")
        ;
}

