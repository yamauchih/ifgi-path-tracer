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
#include <cpp/base/Exception.hh>
#include <cpp/base/ILog.hh>
#include <cpp/scene/SceneGraphNode.hh>
#include <cpp/scene/SceneDB.hh>
#include <cpp/scene/MaterialFactory.hh>
#include <cpp/scene/SGMaterialNode.hh>
#include <cpp/scene/SGPrimitiveNode.hh>
#include <cpp/scene/TriMesh.hh>

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
/// get Float32_3 from python numpy.array <type, numpy.float64>
///
/// \param[in] float32_3_obj python numpy.array <type, numpy.float64>,
/// length 3 object
/// \return Float32_3 vector
Float32_3 get_float32_3(boost::python::object const & float32_3_obj)
{
    if(boost::python::len(float32_3_obj) != 3){
        std::string const objstr =
            boost::python::extract< std::string >(
                boost::python::str(float32_3_obj));
        throw Exception("get_float32_3: arg is not a float32_3 obj [" +
                        objstr + "]");
    }

    Float32_3 vec(0.0f, 0.0f, 0.0f);
    for(int i = 0; i < 3; ++i){
        vec[i] = boost::python::extract< float >(
            float32_3_obj.attr("__getitem__")(i));
    }

    return vec;
}

//----------------------------------------------------------------------
/// get Sint32_3 from python numpy.array <type, numpy.int64>
///
/// \param[in] sint32_3_obj python numpy.array <type, numpy.int64>,
/// length 3 object
/// \return Sint32_3 vector
Sint32_3 get_sint32_3(boost::python::object const & sint32_3_obj)
{
    if(boost::python::len(sint32_3_obj) != 3){
        std::string const objstr =
            boost::python::extract< std::string >(
                boost::python::str(sint32_3_obj));
        throw Exception("get_sint32_3: arg is not a sint32_3 obj [" +
                        objstr + "]");
    }

    Sint32_3 vec(0, 0, 0);
    for(int i = 0; i < 3; ++i){
        // no conversion method of numpy.int64 is registered,
        // therefore, once converted object and call its conversion
        // attribute.
        boost::python::object int64_obj = sint32_3_obj.attr("__getitem__")(i);
        vec[i] = boost::python::extract< int >(
            int64_obj.attr("__int__")());

    }

    return vec;
}

//----------------------------------------------------------------------
/// get Float32_3 vector from python numpy.array <type, numpy.float64> list
///
/// \param[in] float32_3_list python numpy.array <type, numpy.float64>,
/// length 3 object list
/// \param[out] vec_float32_3 vector of Float32_3
void get_vector_float32_3(boost::python::list const & float32_3_list,
                          std::vector< Float32_3 > & vec_float32_3)
{
    // boost::python::extract< boost::python::list > flist_ext(float32_3_list);
    // assert(flist_ext.check());
    // boost::python::list const flist_cpp = flist_ext();
    int const len = boost::python::len(float32_3_list);
    for(int i = 0; i < len; ++i){
        Float32_3 const vec3 = get_float32_3(float32_3_list[i]);
        vec_float32_3.push_back(vec3);
    }
}

//----------------------------------------------------------------------
/// get Sint32_3 vector from python numpy.array <type, numpy.int64> list
///
/// \param[in] sint32_3_list python numpy.array <type, numpy.int64>,
/// length 3 object list
/// \param[out] vec_sint32_3 vector of Sint32_3
void get_vector_sint32_3(boost::python::list const & sint32_3_list,
                         std::vector< Sint32_3 > & vec_sint32_3)
{
    // boost::python::extract< boost::python::list > slist_ext(sint32_3_list);
    // assert(slist_ext.check());
    // boost::python::list const slist_cpp = slist_ext();
    int const len = boost::python::len(sint32_3_list);
    for(int i = 0; i < len; ++i){
        Sint32_3 const vec3 = get_sint32_3(sint32_3_list[i]);
        vec_sint32_3.push_back(vec3);
    }
}

//----------------------------------------------------------------------
/// convert python TriMesh to cpp TriMesh.
bool convert_py_trimesh_to_cpp_trimesh(boost::python::object const & pytrimesh,
                                       TriMesh * p_trimesh)
{
    assert(p_trimesh != 0);
    std::vector< Float32_3 > f32_3_vec[3];
    std::vector< Sint32_3 >  s32_3_vec[3];

    // access to the python TriMesh members

    // attribute names
    const char * p_f32_3_attr_name[] = {
        "vertex_list",
        "texcoord_list",
        "normal_list",
        0,

    };
    // attribute names
    const char * p_s32_3_attr_name[] = {
        "face_idx_list",
        "texcoord_idx_list",
        "normal_idx_list",
        0,
    };

    for(int i = 0; p_f32_3_attr_name[i] != 0; ++i){
        boost::python::object const f32_3_list = pytrimesh.attr(p_f32_3_attr_name[i]);
        boost::python::extract< boost::python::list > f32_3_ext(f32_3_list);
        if(!f32_3_ext.check()){
            throw Exception(std::string("pytrimesh has no [") +
                            p_f32_3_attr_name[i] + "]");
        }
        get_vector_float32_3(f32_3_ext(), f32_3_vec[i]);
    }

    for(int i = 0; p_s32_3_attr_name[i] != 0; ++i){
        boost::python::object const s32_3_list = pytrimesh.attr(p_s32_3_attr_name[i]);
        boost::python::extract< boost::python::list > s32_3_ext(s32_3_list);
        if(!s32_3_ext.check()){
            throw Exception(std::string("pytrimesh has no [") +
                            p_s32_3_attr_name[i] + "]");
        }
        get_vector_sint32_3(s32_3_ext(), s32_3_vec[i]);
    }

    p_trimesh->set_data(f32_3_vec[0],
                        s32_3_vec[0],
                        f32_3_vec[1],
                        s32_3_vec[1],
                        f32_3_vec[2],
                        s32_3_vec[2]);
    return true;
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
// shutdown
int IfgiCppRender::shutdown()
{
    return 0;
}

//----------------------------------------------------------------------
// create a new scene.
void IfgiCppRender::create_scene(boost::python::object const & mat_dict_list,
                                 boost::python::object const & geom_dict_list,
                                 boost::python::object const & camera_pydict)
{

    // create simple scenegraph structure
    SceneGraphNode * p_rootsg = new SceneGraphNode("rootsg");
    SceneDB::instance()->store_sgnode(p_rootsg);

    // "materialgroup" is a special group.
    SceneGraphNode * p_mat_group_node = new SceneGraphNode("materialgroup");
    SceneDB::instance()->store_sgnode(p_mat_group_node);

    p_rootsg->append_child(p_mat_group_node);
    this->add_material_to_scene(p_mat_group_node, mat_dict_list);

    // geometry
    SceneGraphNode * p_mesh_group_node = new SceneGraphNode("meshgroup");
    SceneDB::instance()->store_sgnode(p_mesh_group_node);

    p_rootsg->append_child(p_mesh_group_node);

    // HEREHERE missing material index reference. 2012-1-17(Tue)

    this->add_geometry_to_scene(p_mesh_group_node, geom_dict_list);
    m_scene_graph.set_root_node(p_rootsg);

    // camera
    this->set_camera_pydict(camera_pydict);
}

//----------------------------------------------------------------------
// set camera.
void IfgiCppRender::set_camera_pydict(
    boost::python::object const & camera_pydict_obj)
{
    // object -> extractor
    boost::python::extract< boost::python::dict > cpp_pydict_ext(camera_pydict_obj);
    if(!cpp_pydict_ext.check()){
        throw std::runtime_error("set_camera_pydict: type error: "
                                 "camera_pydict_obj is not a dict.");
    }
    // Dictionary const cpp_cam_dict = get_cpp_dictionary_from_pydict(cpp_pydict_ext());

    // // cpp_cam_dict.write(std::cout, "CPPCAM:");
    // return cpp_cam_dict;

    Dictionary const cpp_camera_dict = get_cpp_dictionary_from_pydict(cpp_pydict_ext());
    cpp_camera_dict.write(std::cout, "set_camera_pydict: ");
    assert(cpp_camera_dict.is_defined("cam_name"));
    m_camera.set_config_dict(cpp_camera_dict);
    m_scene_graph.set_current_camera(m_camera);
}

//----------------------------------------------------------------------
// get camera.
boost::python::object IfgiCppRender::get_camera_pydict() const
{
    Dictionary const cpp_dict = m_camera.get_config_dict();

    return get_pydict_from_cpp_dictionary(cpp_dict);
}

//----------------------------------------------------------------------
// prepare rendering
int IfgiCppRender::prepare_rendering()
{
    // put framebuffers
    this->setup_framebuffer();

    return 0;
}

//----------------------------------------------------------------------
// render frame
int IfgiCppRender::render_n_frame(Sint32 max_frame, Sint32 save_per_frame)
{
    assert(max_frame > 0);
    assert(save_per_frame > 0);

    for(int i = 0; i < max_frame; ++i){
        this->render_single_frame();
        std::stringstream sstr;
        sstr << "frame: " << i;
        ILog::instance()->info(sstr.str());
        if((i != 0) && ((i % save_per_frame) == 0)){
            this->save_frame(i);
        }
    }
    this->save_frame(0);

    return 0;
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
    this->clear_trimesh_memory();
    this->clear_node_memory();
}

//----------------------------------------------------------------------
// clear scene node memory
void IfgiCppRender::clear_node_memory()
{
    for(std::vector< SceneGraphNode * >::iterator si = m_p_sgnode_vec.begin();
        si != m_p_sgnode_vec.end(); ++si)
    {
        delete *(si);
        *(si) = 0;
    }
    m_p_sgnode_vec.clear();
}

//----------------------------------------------------------------------
// clear trimesh memory
void IfgiCppRender::clear_trimesh_memory()
{
    for(std::vector< TriMesh * >::iterator ti = m_p_trimesh_vec.begin();
        ti != m_p_trimesh_vec.end(); ++ti)
    {
        delete *(ti);
        *(ti) = 0;
    }
    m_p_trimesh_vec.clear();
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
        SGMaterialNode * p_ch_mat_sgnode =
            new SGMaterialNode("matnode::" + p_mat->get_material_name());
        p_ch_mat_sgnode->set_material(p_mat);
        SceneDB::instance()->store_sgnode(p_ch_mat_sgnode);

        // put it under the material groupnode.
        // But currently this is not used. Material lookup through the
        // SceneDB.
        p_mat_group_node->append_child(p_ch_mat_sgnode);

        ILog::instance()->
            debug("IfgiCppRender::add_material_to_scene: "
                  "added material " + p_mat->get_classname() + "::" +
                  p_mat->get_material_name() + "\n");
    }
}

//----------------------------------------------------------------------
// add geometry to the scene
void IfgiCppRender::add_geometry_to_scene(
    SceneGraphNode * p_mesh_group_node,
    boost::python::object const & geom_pydict_list)
{
    // convert to the extracted object: list
    boost::python::extract< boost::python::list > cpp_list_ext(geom_pydict_list);
    if(!cpp_list_ext.check()){
        throw std::runtime_error(
            "add_geometry_to_scene: type error: geom_pydict_list is not a list.");
    }

    // iterate over the list
    boost::python::list cpp_dict_list = cpp_list_ext();
    int const len = boost::python::len(cpp_dict_list);
    for(int i = 0; i < len; ++i){
        boost::python::dict geom_pydict =
            boost::python::extract< boost::python::dict >(cpp_dict_list[i]);
        // convert geom dict to scene
        this->add_one_geometry_to_scene(p_mesh_group_node, geom_pydict);
    }
}

//----------------------------------------------------------------------
// add one primitive to the scene
void IfgiCppRender::add_one_geometry_to_scene(
    SceneGraphNode * p_mesh_group_node,
    boost::python::dict const & geom_pydict)
{
    // geom_pydict entries
    //   geom_pydict["geo_name"] = "name_of_geometry"
    //   geom_pydict["material"] = "material_name"
    //   geom_pydict["geo_file_type"] = "obj"
    //   geom_pydict["geo_file_name"] = "filename"
    //   geom_pydict["TriMesh"]  = Primitive.TriMesh object

    Dictionary geom_cpp_dict = get_cpp_dictionary_from_pydict(geom_pydict);
    geom_cpp_dict.write(std::cout, "DEBUG: ");

    // check all the expected keys are there
    char const * p_mandatory_key[] = { "geo_name",
                                       "material",
                                       "geo_file_type", // currently discarded
                                       "geo_file_name", // currently discarded
                                       "TriMesh",
                                       0};
    std::vector< std::string > undef_keys;
    if(!(is_all_key_defined(geom_cpp_dict, p_mandatory_key, &undef_keys))){
        std::stringstream sstr;
        std::copy(undef_keys.begin(), undef_keys.end(),
                  std::ostream_iterator< std::string >(sstr, " "));
        throw Exception("missing keys for geom_pydict [" + sstr.str() + "]");
    }

    // this class has the ownership of trimeshes
    TriMesh * p_tmesh = new TriMesh;
    m_p_trimesh_vec.push_back(p_tmesh); // owner: keep the reference
    convert_py_trimesh_to_cpp_trimesh(geom_pydict["TriMesh"], p_tmesh);

    std::string const mat_name = geom_cpp_dict.get< std::string >("material");
    std::string const geo_name = geom_cpp_dict.get< std::string >("geo_name");
    Sint32 const matidx = SceneDB::instance()->
        get_material_index_by_name(mat_name);
    if(matidx < 0){
        ILog::instance()->warn(mat_name + " is not found in SceneDB. [" +
                               geo_name + "] has no material reference.");
    }
    p_tmesh->set_material_index(matidx);

    std::cout << "DEBUG: trimesh info\n"
              << p_tmesh->get_info_summary() << std::endl;

    // this class has the ownership of scenegraph nodes
    SGPrimitiveNode * p_ch_node = new SGPrimitiveNode(geo_name, p_tmesh);
    m_p_sgnode_vec.push_back(p_ch_node); // owner: keep the reference
    p_mesh_group_node->append_child(p_ch_node);
}

//----------------------------------------------------------------------
// set up framebuffer in the camera
void IfgiCppRender::setup_framebuffer()
{
    // from camera

    std::cerr << "IfgiCppRender::setup_framebuffer: NIN" << std::endl;
}

//----------------------------------------------------------------------
// render single frame.
Sint32 IfgiCppRender::render_single_frame()
{
    std::cerr << "IfgiCppRender::render_single_frame: NIN" << std::endl;
    return 1;
}

//----------------------------------------------------------------------
// save a frame
Sint32 IfgiCppRender::save_frame(Sint32 frame_count)
{
    std::cerr << "IfgiCppRender::save_frame: NIN" << std::endl;
    return 1;
}

//----------------------------------------------------------------------
} // namespace ifgi
