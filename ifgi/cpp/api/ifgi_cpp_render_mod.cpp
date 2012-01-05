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
// test add dict list
// void IfgiCppRender::add_dict_list(boost::python::object dict_list)
// {
//     // convert to the extracted object: list
//     boost::python::extract< boost::python::list > cpp_dict_list_ext(dict_list);
//     if(!cpp_dict_list_ext.check()){
//         throw std::runtime_error(
//             "IfgiCppRender::add_dict_list: type error: "
//             "dict_list is not a list.");
//     }

//     boost::python::list cpp_dict_list = cpp_dict_list_ext();
//     int const len = boost::python::len(cpp_dict_list);
//     std::cout << "DEBUG: len(dict_list) = " << len << std::endl;
//     for(int i = 0; i < len; ++i){
//         boost::python::dict di =
//             boost::python::extract< boost::python::dict >(cpp_dict_list[i]);

//         boost::python::list keylist = di.keys();

//         int const one_len = boost::python::len(keylist);
//         for(int j = 0; j < one_len; ++j){
//             std::string const keystr =
//                 boost::python::extract< std::string >(
//                     boost::python::str(keylist[j]));
//             std::cout << "list[" << i << "]'s key[" << j << "]=["
//                       << keystr << "]" << std::endl;
//         }
//     }
// }
// DELETEME

//----------------------------------------------------------------------
// convert python dict to cpp Dictionary
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

    // // convert to the extracted object: list
    // boost::python::extract< boost::python::list > cpp_dict_list_ext(dict_list);
    // if(!cpp_dict_list_ext.check()){
    //     throw std::runtime_error(
    //         "IfgiCppRender::add_dict_list: type error: "
    //         "dict_list is not a list.");
    // }

    // boost::python::list cpp_dict_list = cpp_dict_list_ext();
    // int const len = boost::python::len(cpp_dict_list);
    // std::cout << "len(dict_list) = " << len << std::endl;
    // for(int i = 0; i < len; ++i){
    //     boost::python::dict di =
    //         boost::python::extract< boost::python::dict >(cpp_dict_list[i]);
    //     boost::python::list keylist = di.keys();

    //     int const one_len = boost::python::len(keylist);
    //     for(int j = 0; j < one_len; ++j){
    //         std::string const keystr =
    //             boost::python::extract< std::string >(
    //                 boost::python::str(keylist[j]));
    //         std::cout << "list[" << i << "]'s key[" << j << "]=["
    //                   << keystr << "]" << std::endl;
    //     }
    // }

//----------------------------------------------------------------------
// set camera.
void IfgiCppRender::set_camera(boost::python::object camera_dict)
{
}

//----------------------------------------------------------------------
// add a material to the scene
// void IfgiCppRender::add_material(boost::python::object mat)
// {
//     // convert to the extracted object
//     boost::python::extract< boost::python::dict > cppmat_ext(mat);
//     if(!cppmat_ext.check()){
//         throw std::runtime_error(
//             "IfgiCppRender::add_material: type error: material is not a dictionary.");
//     }

//     boost::python::dict cppdict = cppmat_ext();
//     boost::python::list keylist = cppdict.keys();

//     int const len = boost::python::len(keylist);
//     std::cout << "len(keylist) = " << len << std::endl;
//     Dictionary dict;
//     for(int i = 0; i < len; ++i){
//         // operator[] is in python::boost::object
//         std::string keystr =
//             boost::python::extract< std::string >(boost::python::str(keylist[i]));
//         std::string valstr =
//             boost::python::extract< std::string >(
//                 boost::python::str(cppdict[keylist[i]]));
//         std::cout << "key:[" << keystr << "]->[" << valstr << "]" << std::endl;

//         dict.set(keystr, valstr);
//     }
//     // TODO: push this material to C++ ifgi renderer core
// }

//----------------------------------------------------------------------
// test add dict list
// void IfgiCppRender::add_dict_list(boost::python::object dict_list)
// {
//     // convert to the extracted object: list
//     boost::python::extract< boost::python::list > cpp_dict_list_ext(dict_list);
//     if(!cpp_dict_list_ext.check()){
//         throw std::runtime_error(
//             "IfgiCppRender::add_dict_list: type error: "
//             "dict_list is not a list.");
//     }

//     boost::python::list cpp_dict_list = cpp_dict_list_ext();
//     int const len = boost::python::len(cpp_dict_list);
//     std::cout << "len(dict_list) = " << len << std::endl;
//     for(int i = 0; i < len; ++i){
//         boost::python::dict di =
//             boost::python::extract< boost::python::dict >(cpp_dict_list[i]);
//         boost::python::list keylist = di.keys();

//         int const one_len = boost::python::len(keylist);
//         for(int j = 0; j < one_len; ++j){
//             std::string const keystr =
//                 boost::python::extract< std::string >(
//                     boost::python::str(keylist[j]));
//             std::cout << "list[" << i << "]'s key[" << j << "]=["
//                       << keystr << "]" << std::endl;
//         }
//     }
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
        .def("set_camera",
             &ifgi::IfgiCppRender::set_camera,
             "set camera. only defined key value pairs will be updated.")
        ;
}

