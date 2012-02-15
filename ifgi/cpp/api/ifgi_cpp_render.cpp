//----------------------------------------------------------------------
// ifgi C++ implementation
// Copyright (C) 2010-2012 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief ifgi render C++ implementation

#include "ifgi_cpp_render.hh"

#include <stdexcept>
#include <iostream>

#include <cpp/base/Exception.hh>
#include <cpp/base/ILog.hh>
#include <cpp/base/SamplerUnitHemisphereUniform.hh>
#include <cpp/base/SamplerStratifiedRegular.hh>

#include <cpp/scene/SceneGraphNode.hh>
#include <cpp/scene/SceneDB.hh>
#include <cpp/scene/MaterialFactory.hh>
#include <cpp/scene/SGMaterialNode.hh>
#include <cpp/scene/SGPrimitiveNode.hh>
#include <cpp/scene/TriMesh.hh>
#include <cpp/scene/HitRecord.hh>
#include <cpp/scene/ImageFilm.hh>


namespace ifgi {
//----------------------------------------------------------------------
// constructor
IfgiCppRender::IfgiCppRender()
    :
    m_p_cur_framebuffer_ref(0),
    m_p_mat_group_node_ref(0),
    m_p_mesh_group_node_ref(0),
    m_p_hemisphere_sampler(0)
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
void IfgiCppRender::create_simple_scenegraph()
{
    if(m_scene_graph.peek_root_node() != 0){
        throw Exception("The scene is not empty! Double creation?");
    }

    // create simple scenegraph structure
    SceneGraphNode * p_rootsg = new SceneGraphNode("rootsg");
    SceneDB::instance()->store_sgnode(p_rootsg);

    // "materialgroup" is a special group.
    assert(m_p_mat_group_node_ref == 0);
    m_p_mat_group_node_ref = new SceneGraphNode("materialgroup");
    SceneDB::instance()->store_sgnode(m_p_mat_group_node_ref);

    p_rootsg->append_child(m_p_mat_group_node_ref);

    // geometry group
    m_p_mesh_group_node_ref = new SceneGraphNode("meshgroup");
    SceneDB::instance()->store_sgnode(m_p_mesh_group_node_ref);

    p_rootsg->append_child(m_p_mesh_group_node_ref);
}

//----------------------------------------------------------------------
// add a material to the scene via Dictionary
void IfgiCppRender::add_material_to_scene_by_dict(Dictionary const & mat_dict)
{
    IMaterial * p_mat = new_material_factory(mat_dict);
    SGMaterialNode * p_ch_mat_sgnode =
        new SGMaterialNode("matnode::" + p_mat->get_material_name());
    p_ch_mat_sgnode->set_material(p_mat);
    SceneDB::instance()->store_sgnode(p_ch_mat_sgnode);

    // put it under the material groupnode.
    // But currently this is not used. Material lookup through the
    // SceneDB.
    assert(m_p_mat_group_node_ref != 0);
    m_p_mat_group_node_ref->append_child(p_ch_mat_sgnode);

    ILog::instance()->
        debug("IfgiCppRender::add_material_to_scene_by_dict: "
              "added material " + p_mat->get_classname() + "::" +
              p_mat->get_material_name() + "\n");
}

//----------------------------------------------------------------------
// add a trimesh to the scene. This object takes the ownership.
void IfgiCppRender::add_trimesh_to_scene(std::string const geo_name,
                                         std::string const mat_name,
                                         TriMesh * p_tmesh)
{
    Sint32 const matidx = SceneDB::instance()->get_material_index_by_name(mat_name);
    if(matidx < 0){
        ILog::instance()->warn(mat_name + " is not found in SceneDB. [" +
                               geo_name + "] has no material reference.");
    }
    p_tmesh->set_material_index(matidx);
    m_p_trimesh_vec.push_back(p_tmesh); // owner: keep the reference

    std::cout << "DEBUG: trimesh info\n"
              << p_tmesh->get_info_summary() << std::endl;

    // this class has the ownership of scenegraph nodes
    SGPrimitiveNode * p_ch_node = new SGPrimitiveNode(geo_name, p_tmesh);
    m_p_sgnode_vec.push_back(p_ch_node); // owner: keep the reference
    m_p_mesh_group_node_ref->append_child(p_ch_node);
}


//----------------------------------------------------------------------
// set camera.
void IfgiCppRender::set_camera_dict(Dictionary const & camera_dict)
{
    camera_dict.write(std::cout, "set_camera_pydict: ");
    assert(camera_dict.is_defined("cam_name"));
    m_camera.set_config_dict(camera_dict);
    m_scene_graph.set_current_camera(m_camera);
}

//----------------------------------------------------------------------
// get camera.
Dictionary IfgiCppRender::get_camera_dict() const
{
    Dictionary const cpp_dict = m_camera.get_config_dict();
    return cpp_dict;
}

//----------------------------------------------------------------------
// prepare rendering
int IfgiCppRender::prepare_rendering()
{
    // put framebuffers
    this->setup_framebuffer();

    // create sampler
    this->setup_sampler();

    return 0;
}

//----------------------------------------------------------------------
// render frame
int IfgiCppRender::render_n_frame(Sint32 max_frame, Sint32 save_per_frame)
{
    assert(max_frame > 0);
    assert(save_per_frame > 0);

    // std::cout << "DEBUG: waiting for a number input." << std::endl;
    // int x;
    // std::cin >> x;              // debug: wait for input
    // DELETEME

    // set the framebuffer
    Camera & current_camera = m_camera;
    ImageFilm * p_img = current_camera.peek_film("RGBA");
    assert(p_img != 0);
    m_p_cur_framebuffer_ref = p_img;

    for(int i = 0; i < max_frame; ++i){
        this->render_single_frame(i);
        std::stringstream sstr;
        sstr << "frame: " << i << "\n";
        ILog::instance()->info(sstr.str());
        if((i != 0) && ((i % save_per_frame) == 0)){
            this->save_frame(i);
        }
    }
    this->save_frame(0);

    return 0;
}

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
// set up framebuffer in the camera
void IfgiCppRender::setup_framebuffer()
{
    // from camera
    Sint32 const res_x = m_camera.get_resolution_x();
    Sint32 const res_y = m_camera.get_resolution_y();

    ImageFilm * p_rgba = new ImageFilm(Sint32_3(res_x, res_y, 4), "RGBA");
    m_camera.set_film(p_rgba);
    ILog::instance()->info("added ImageFilm: " + p_rgba->get_buffername() + "\n");
}

//----------------------------------------------------------------------
// set up sampler
void IfgiCppRender::setup_sampler()
{
    assert(m_p_hemisphere_sampler == 0);

    m_p_hemisphere_sampler = new SamplerUnitHemisphereUniform;
}

//----------------------------------------------------------------------
// ray scene intersection
bool IfgiCppRender::ray_scene_intersection(Ray const & ray, HitRecord & closest_hr)
{
    closest_hr.initialize();    // set m_dist = std::numeric_limits< Scalar >::max();
    HitRecord tmp_hr;
    for(std::vector< TriMesh * >::const_iterator tmi = m_p_trimesh_vec.begin();
        tmi != m_p_trimesh_vec.end(); ++tmi)
    {
        // DELETEME std::cout << (*tmi)->get_info_summary() << std::endl;
        if((*tmi)->ray_intersect(ray, tmp_hr)){
            // std::cout << "IfgiCppRender::ray_scene_intersection: HIT"  << std::endl;

            // hit
            if(closest_hr.m_dist > tmp_hr.m_dist){
                closest_hr = tmp_hr; // FIXME. Maybe not necessary to copy alll
            }
        }
        else{
            // std::cout << "IfgiCppRender::ray_scene_intersection: NoHit"  << std::endl;
        }
    }

    if(closest_hr.m_dist == std::numeric_limits< Scalar >::max()){
        return false;
    }
    return true;
}

//----------------------------------------------------------------------
// compute a color
void IfgiCppRender::compute_color(
    Sint32 pixel_x,
    Sint32 pixel_y,
    Ray & ray,
    Sint32 nframe)
{
    bool is_update_intensity = false;
    HitRecord hr;

    // FIXME max_path_length is here
    Sint32 const max_path_length = 10;
    ray.set_path_length(-1);
    for(Sint32 path_len = 0; path_len < max_path_length; ++path_len){
        bool const is_hit = this->ray_scene_intersection(ray, hr);
        if(is_hit){
            // std::cout << "Hit" << std::endl;

            // hit somthing, lookup material
            assert(hr.m_hit_material_index >= 0);
            IMaterial * p_mat = SceneDB::instance()->peek_material(hr.m_hit_material_index);
            assert(p_mat != 0);

            // only Lambert/Diffuse material
            Color brdf_col;      // FIXME: preallocation
            p_mat->explicit_brdf(brdf_col);
            // probability is 1/pi, here, constant importance,
            // therefore, divided by (1/pi) = multiplied by pi
            Color const refl = ray.get_reflectance() * static_cast< Scalar >(M_PI) * brdf_col;
            ray.set_reflectance(refl);

            if(p_mat->is_emit()){
                // only Lambert emittance
                // p_mat->emit_radiance(_hit_onb, light_out_dir, tex_point, tex_uv));
                Color emit_rad;
                p_mat->emit_radiance(emit_rad);
                Color const inten = ray.get_intensity() + ray.get_reflectance() * emit_rad;
                ray.set_intensity(inten);
                // hit the light source
                std::cout << "DEBUG: Hit a light source at path length = "
                          << ray.get_path_length()
                          << std::endl;
                is_update_intensity = true;
                break;
            }
            // Do not stop by reflectance criterion. (if stop, it's wrong.);
            
            // update ray information
            Scalar_3 const out_v = p_mat->diffuse_direction(hr.m_hit_onb, ray.get_dir(),
                                                            m_p_hemisphere_sampler);
            ray.set_origin(hr.m_intersect_pos);
            ray.set_dir(out_v);

            // mat = m_scene_geo_mat.material_list[hr.hit_material_index];
            // // only Lambert
            // // mat.explicit_brdf(hr.hit_basis, out_v0, out_v1, tex_point, tex_uv);
            // /// print "DEBUG: mat ref ", mat.explicit_brdf(None, None, None, None, None);

            //     // probability is 1/pi, here, constant importance,
            //     // therefore, divided by (1/pi) = multiplied by pi
            //     brdf = M_PI * mat.explicit_brdf(None, None, None, None, None);
            //     ray.reflectance = (ray.reflectance * brdf);
            //     if(mat.is_emit()){
            //         // only Lambert emittance
            //         // mat.emit_radiance(_hit_onb, light_out_dir, tex_point, tex_uv));
            //         ray.intensity = ray.intensity +
            //             (ray.reflectance * mat.emit_radiance(None, None, None, None));
            //         // hit the light source

            //         // print "DEBUG: Hit a light source at path length = ", ray.path_length
            //         //     is_update_intensity = True;
            //         break;
            //     }
            //     // Do not stop by reflectance criterion. (if stop, it"s wrong.);

            //     // update ray information
            //     out_v = mat.diffuse_direction(hr.hit_basis, ray.get_dir(),
            //                                   m_p_hemisphere_sampler);
            //     ray.set_origin(copy.deepcopy(hr.intersect_pos));
            //     ray.set_dir(copy.deepcopy(out_v));
        }
        // else{
        //     // done. hit to the environmnt.
        //     // FIXME: currently assume the environment color is always constant
        //     hit_onb = None;
        //     light_out_dir = None;
        //     tex_point = None;
        //     tex_uv = None;
        //     // print "DEBUG: ray int = ", ray.intensity, ", ref = " , ray.reflectance
        //     amb_col = m_environment_mat.ambient_response(hit_onb, light_out_dir,
        //                                                  tex_point, tex_uv);
        //     ray.intensity = ray.intensity + (ray.reflectance * amb_col);
        //     is_update_intensity = True;
        //     // print "DEBUG: hit env, amb_col = ", amb_col
        //     break;
        // }
    }

    // now we know the color
    assert(m_p_cur_framebuffer_ref != 0);
    Scalar const s_nframe = static_cast< Scalar >(nframe);
    Scalar const s_one(1.0);
    if(is_update_intensity == true){ // && (ray.path_length == 2);
        Color const col = s_nframe * m_p_cur_framebuffer_ref->get_color(pixel_x, pixel_y)
            + ray.get_intensity();
        m_p_cur_framebuffer_ref->put_color(pixel_x, pixel_y, col/(s_nframe + s_one));
    }
}

//----------------------------------------------------------------------
// render single frame.
Sint32 IfgiCppRender::render_single_frame(Sint32 nframe)
{
    Camera & current_camera = m_camera;
    // current frame buffer must be the same as the current camera's framebuffer
    // In render_n_frame().
    assert(m_p_cur_framebuffer_ref == current_camera.peek_film("RGBA"));

    Sint32 const res_x = current_camera.get_resolution_x();
    Sint32 const res_y = current_camera.get_resolution_y();
    assert(res_x > 0);
    assert(res_y > 0);

    Dictionary dict = current_camera.get_config_dict();
    // dict.write(std::cout, "Render_Single_Frame: ");
    
    // screen space sampler
    SamplerStratifiedRegular srs;
    srs.compute_sample(0, res_x - 1, 0, res_y - 1);

    assert(m_p_hemisphere_sampler != 0);

    Scalar const inv_xsz = 1.0f / static_cast< Scalar >(res_x);
    Scalar const inv_ysz = 1.0f / static_cast< Scalar >(res_y);

    Sint32 const XDIR = 0;
    Sint32 const YDIR = 1;
    Ray eye_ray;
    for(Sint32 y = 0; y < res_y; ++y){
        for(Sint32 x = 0; x < res_x; ++x){
            // get normalized coordinate
            Scalar const nx = srs.get_sample(x, y, XDIR) * inv_xsz;
            Scalar const ny = srs.get_sample(x, y, YDIR) * inv_ysz;

            // FIXME Ray preallocation
            current_camera.get_ray(nx, ny, eye_ray);

            // DELETEME
            // std::cout << "DEBUG: Ray: [" << x << " " << y << "]: "
            //           << eye_ray.to_string() << std::endl;
            this->compute_color(x, y, eye_ray, nframe);
        }
    }

    // success ... 0
    return 1;
}

//----------------------------------------------------------------------
// save a frame
Sint32 IfgiCppRender::save_frame(Sint32 frame_count)
{
    std::stringstream sstr;
    sstr << "frame_" << frame_count;
    assert(m_p_cur_framebuffer_ref != 0);
    bool ret_ppm = m_p_cur_framebuffer_ref->save_file(sstr.str() + ".ppm", "ppm");
    bool ret_gfi = m_p_cur_framebuffer_ref->save_file(sstr.str() + ".gfi", "gfi");
    if(!ret_ppm){
        std::cout << "fail to save " << sstr.str() << ".ppm" << std::endl;
    }
    if(!ret_gfi){
        std::cout << "faile to save " << sstr.str() << ".gfi" << std::endl;
    }

    return ret_ppm && ret_gfi;
}

//----------------------------------------------------------------------
} // namespace ifgi
