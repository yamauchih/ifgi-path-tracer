//----------------------------------------------------------------------
// ifgi c++ implementation
// Copyright (C) 2010-2012 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief ifgi render api for C++ implementation

#include "ifgi_cpp_render.hh"

// boost side
#include <stdexcept>
#include <iostream>
#include <boost/python/extract.hpp>
#include <boost/python/list.hpp>
#include <boost/python/dict.hpp>
#include <boost/python/str.hpp>

// ifgi side
#include <cpp/base/ILog.hh>
#include <cpp/scene/SceneGraphNode.hh>
#include <cpp/scene/SceneDB.hh>
#include <cpp/scene/MaterialFactory.hh>

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
        // std::cout << "DEBUG: list[" << i << "]" << std::endl;

        // get value as a string
        std::string valstr =
            boost::python::extract< std::string >(
                boost::python::str(pydict[keylist[i]]));
        // std::cout << "DEBUG:   key:[" << keystr << "]->["
        //           << valstr << "]" << std::endl;

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
        // converted_cppdict.write(std::cout, "DEBUG: CPP Dictionary: ");
        cpp_dictionary_vec.push_back(converted_cppdict);
    }
}

//----------------------------------------------------------------------
//======================================================================
//----------------------------------------------------------------------
// constructor
IfgiCppRender::IfgiCppRender()
{
    // empty
}

//----------------------------------------------------------------------
// destructor
IfgiCppRender::~IfgiCppRender()
{
    this->clear_scene();
}

//----------------------------------------------------------------------
// initialize ifgi
int IfgiCppRender::initialize()
{
    ILog::instance()->set_output_level(ILog::ILog_Debug);

    return 0;
}

//----------------------------------------------------------------------
// create a new scene.
void IfgiCppRender::create_scene(boost::python::object const & mat_dict_list,
                                 boost::python::object const & geom_dict_list,
                                 boost::python::object const & camera_dict)
{
    
    // create simple scenegraph structure
    SceneGraphNode * p_rootsg = new SceneGraphNode("rootsg");
    SceneDB::instance()->store_sgnode(p_rootsg);

    // camera
    this->set_camera_dict(camera_dict);
    // NIN
    // CameraNode *     p_cam_node = new CameraNode("main_cam");
    // if("default" in ifgi_reader.camera_dict_dict){
    //     cam_node.get_camera().set_config_dict(_ifgi_reader.camera_dict_dict["default"]);
    // else:
    //     ILog.warn("ifgi scene file has no default camera, use camera default.");
    // rootsg.append_child(cam_node);

    // "materialgroup" is a special group.
    SceneGraphNode * p_mat_group_node = new SceneGraphNode("materialgroup");
    SceneDB::instance()->store_sgnode(p_mat_group_node);

    p_rootsg->append_child(p_mat_group_node);
    this->add_material_to_scene(p_mat_group_node, mat_dict_list);
    // for mat_dict in ifgi_reader.material_dict_list:
    //     mat = Material.material_factory(mat_dict);
    //     ch_mat_node = MaterialNode(mat_dict["mat_name"]);
    //     ch_mat_node.set_material(mat);
    //     mat_group_node.append_child(ch_mat_node);

    // geometry
    // NIN FIXME
    // append_pydict_list_to_dictionary_vec(m_geo_dict_vec, geom_dict_list);
    // SceneGraphNode * p_mesh_group = new SceneGraphNode("meshgroup");
    // p_rootsg->append_child(p_mesh_group);
    // for geo_dict in ifgi_reader.geometry_dict_list:
    //     ch_node = PrimitiveNode(geo_dict["geo_name"], geo_dict["TriMesh"]);
    //     mesh_group.append_child(ch_node);
    //
    // sg.set_root_node(rootsg);
    // sg.set_current_camera(cam_node.get_camera());
}

//----------------------------------------------------------------------
// set camera.
void IfgiCppRender::set_camera_dict(boost::python::object const & camera_pydict_obj)
{
    // object -> extractor
    boost::python::extract< boost::python::dict > cpp_pydict_ext(camera_pydict_obj);
    if(!cpp_pydict_ext.check()){
        throw std::runtime_error("set_camera_dict: type error: "
                                 "camera_pydict_obj is not a dict.");
    }
    Dictionary const cpp_cam_dict = get_cpp_dictionary_from_pydict(cpp_pydict_ext());

    // cpp_cam_dict.write(std::cout, "CPPCAM:");
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
// clear the scene
void IfgiCppRender::clear_scene()
{
    m_geo_dict_vec.clear();
    m_camera_dict.clear();

    this->clear_node_memory();
}

//----------------------------------------------------------------------
// clear scene node memory
void IfgiCppRender::clear_node_memory()
{
    // NIN
}

//----------------------------------------------------------------------
// add material to the scene
void IfgiCppRender::add_material_to_scene(
    SceneGraphNode * p_mat_group_node,
    boost::python::object const & mat_dict_list)
{
    assert(p_mat_group_node != 0);

    // convert to cpp dictionary vector
    std::vector< Dictionary > mat_dict_vec;
    append_pydict_list_to_dictionary_vec(mat_dict_vec, mat_dict_list);

    for(std::vector< Dictionary >::const_iterator di = mat_dict_vec.begin();
        di != mat_dict_vec.end(); ++di)
    {
        IMaterial * p_mat = new_material_factory(*di);
        // NIN FIXME Create MaterialNode and push the p_mat inside. HEREHERE 2012-1-9(Mon)
        ILog::instance()->
            debug("IfgiCppRender::add_material_to_scene: "
                  "added material " + p_mat->get_classname() + "::" +
                  p_mat->get_material_name() + "\n");
    }
}

//----------------------------------------------------------------------
} // namespace ifgi
