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
#include <cpp/base/Dictionary.hh>

namespace ifgi {

//----------------------------------------------------------------------
// initialize ifgi
int IfgiCppRender::initialize()
{
    return 0;
}

//----------------------------------------------------------------------
// add a material to the scene
void IfgiCppRender::add_material(boost::python::object mat) const
{
    // convert to the extracted object
    boost::python::extract< boost::python::dict > cppmat_ext(mat);
    if(!cppmat_ext.check()){
        throw std::runtime_error(
            "IfgiCppRender::add_material: type error: material is not a dictionary.");
    }

    boost::python::dict cppdict = cppmat_ext();
    boost::python::list keylist = cppdict.keys();

    int const len = boost::python::len(keylist);
    std::cout << "len(keylist) = " << len << std::endl;
    Dictionary dict;
    for(int i = 0; i < len; ++i){
        // operator[] is in python::boost::object
        std::string keystr =
            boost::python::extract< std::string >(boost::python::str(keylist[i]));
        std::string valstr =
            boost::python::extract< std::string >(
                boost::python::str(cppdict[keylist[i]]));
        std::cout << "key:[" << keystr << "]->[" << valstr << "]" << std::endl;

        dict.set(keystr, valstr);
    }
    // TODO: push this material to C++ ifgi renderer core
}

//----------------------------------------------------------------------
/// get material name list
/// \return list of material name
// object get_material_name_list() const
// {
//     boost::python::list mat_name_list;

//     return mat_name_list;
// }


// /// pass a python object, but this should be a python dictionary.
// /// \param[in] pydict a dictionary
// void pass_dict(object pydict) const {
//     extract< dict > cppdict_ext(pydict);
//     if(!cppdict_ext.check()){
//         throw std::runtime_error(
//             "IfgiCppRender::pass_dict: type error: not a python dict.");
//     }

//     dict cppdict = cppdict_ext();
//     list keylist = cppdict.keys();

//     // careful with boost name. there already have a conflict.
//     int const len = boost::python::len(keylist);
//     std::cout << "len(keylist) = " << len << std::endl;
//     for(int i = 0; i < len; ++i){
//         // operator[] is in python::boost::object
//         std::string keystr = extract< std::string >(str(keylist[i]));
//         std::string valstr = extract< std::string >(str(cppdict[keylist[i]]));
//         std::cout << "key:[" << keystr << "]->[" << valstr << "]" << std::endl;
//     }
// }

// /// return a dict object.
// /// \return a dict object
// object return_dict() const {
//     dict cppdict;
//     cppdict["this"] = "work?";
//     cppdict["no"]   = "idea";
//     cppdict["number"]   = 1;

//     return cppdict;
// }

// /// return a dict object.
// /// \return a dict object
// object return_string() const {
//     return str("Incredible, this works.");
// }

} // namespace ifgi

/// importing module name is 'IfgiCppRender_mod'
BOOST_PYTHON_MODULE(ifgi_cpp_render_mod)
{
    boost::python::class_<ifgi::IfgiCppRender>("ifgi_cpp_render")
        .def("initialize",
             &ifgi::IfgiCppRender::initialize,
             "initialize ifgi C++ rendering core")
        .def("add_material",
             &ifgi::IfgiCppRender::add_material,
             "add material to C++ rendering core")
        ;
}

