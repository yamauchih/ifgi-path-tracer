//----------------------------------------------------------------------
// ifgi c++ implementation
// Copyright (C) 2010-2011 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief ifgi render api for C++ implementation
#ifndef IFGI_PATH_TRACER_IFGI_CPP_API_IFGI_CPP_RENDER_MOD_HH
#define IFGI_PATH_TRACER_IFGI_CPP_API_IFGI_CPP_RENDER_MOD_HH

// boost
#include <boost/python.hpp>
#include <boost/python/object.hpp>
// #include <boost/python/extract.hpp>
// #include <boost/python/list.hpp>
// #include <boost/python/dict.hpp>
// #include <boost/python/str.hpp>

// #include <stdexcept>
// #include <iostream>
#include <vector>
#include <map>

// ifgi
#include <cpp/base/Dictionary.hh>

namespace ifgi {

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
class IfgiCppRender
{
public:
    /// constructor
    IfgiCppRender()
    {
        // empty
    }
    /// destructor
    ~IfgiCppRender()
    {
        // empty
    }

    /// initialize ifgi
    /// \return 0 when succeeded
    int initialize();

    /// clear the scene
    void clear_scene();

    /// append a new scene. material and geometry will be added.
    ///
    /// \param[in] mat_dict_list  material dictionary list
    /// \param[in] geom_dict_list geometry dictionary list
    /// \param[in] camera_dict    camera dictionary
    void append_scene(boost::python::object mat_dict_list,
                      boost::python::object geom_dict_list);

    /// set camera.
    ///
    /// \param[in] camera_dict camera dictionary
    void set_camera(boost::python::object camera_dict);

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

private:


private:
    /// material dictionary vector
    std::vector< Dictionary > m_mat_dict_vec;
    /// geometry dictionary vector
    std::vector< Dictionary > m_geo_dict_vec;
    ///camera dictionary
    Dictionary m_camera_dict;
};

} // namespace ifgi

#endif // #ifndef IFGI_PATH_TRACER_IFGI_CPP_API_IFGI_CPP_RENDER_MOD_HH
