//----------------------------------------------------------------------
// ifgi C++ implementation
// Copyright (C) 2010-2012 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief ifgi render C++ implementation
#ifndef IFGI_PATH_TRACER_IFGI_CPP_API_IFGI_CPP_RENDER_HH
#define IFGI_PATH_TRACER_IFGI_CPP_API_IFGI_CPP_RENDER_HH

#include <vector>
#include <map>

#include <cpp/base/Dictionary.hh>
#include <cpp/scene/SceneGraph.hh>

namespace ifgi {

class SceneGraph;
class TriMesh;
class HitRecord;
class SamplerUnitHemisphereUniform;

//----------------------------------------------------------------------
/// ifgi C++ rendering core interface
///
/// Typical usage.
/// - construct this object
/// - initialize() this object
/// - create_simple_scene()
/// - set_camera_dict() ... may call several times
/// - render()
class IfgiCppRender
{
public:
    /// constructor
    IfgiCppRender();

    /// destructor
    ~IfgiCppRender();

    /// initialize ifgi
    /// \return 0 when succeeded
    Sint32 initialize();

    /// shutdown
    /// \return shutdown state. 0 ... success
    Sint32 shutdown();

    /// clear the scene
    void clear_scene();

    /// create a simple scenegraph structure.
    ///
    /// This scene has a fixed structure. Maybe one day, I will write
    /// a flexible scene structure creation API. But for a while, I
    /// will stick to this simple structure.
    ///
    /// SceneGraph structure.
    ///
    /// SceneGraph +
    ///            +--+ SceneGraphNode: 'rootsg' root_node
    ///                              +--+ CameraNode: 'main_cam' camera
    ///                              +--+ SceneGraphNode: 'materialgroup'
    ///                                                +--+ Material: 'mat0'
    ///                                                +--+ Material: 'mat1'
    ///                                                   ...
    ///                              +--+ SceneGraphNode: 'meshgroup'
    ///                                                +--+ TriMesh: 'trimesh0'
    ///                                                +--+ TriMesh: 'trimesh1'
    ///                                                   ...
    ///
    void create_simple_scenegraph();

    /// add a material to the scene via Dictionary
    void add_material_to_scene_by_dict(Dictionary const & mat_dict);

    /// add a trimesh to the scene. This object takes the ownership.
    ///
    /// \param[in] geo_name geometry name
    /// \param[in] mat_name material name (The material should be
    /// defined before this call.)
    /// \param[in] p_tmesh a reference to the trimesh. This object
    /// takes the ownership.
    void add_trimesh_to_scene(std::string const geo_name,
                              std::string const mat_name,
                              TriMesh * p_tmesh);

    /// set camera via a Dictionary. Replaced all the data.
    ///
    /// \param[in] camera_dict camera dictionary
    void set_camera_dict(Dictionary const & camera_dict);

    /// get camera.
    ///
    /// \return get current camera as a dictionary
    Dictionary get_camera_dict() const;

    /// prepare rendering
    ///
    /// \return preparation status. 0 ... success.
    Sint32 prepare_rendering();

    /// render n frames
    ///
    /// \param[in] max_frame max number of frames to render by this call
    /// \param[in] save_per_frame save a frame each save_per_frame
    /// \return rendering status. 0 ... success
    Sint32 render_n_frame(Sint32 max_frame, Sint32 save_per_frame);

private:
    /// clear scene node memory
    void clear_node_memory();
    /// clear trimesh memory
    void clear_trimesh_memory();

    /// set up framebuffer in the camera
    void setup_framebuffer();

    /// set up sampler
    void setup_sampler();

    /// ray scene intersection
    ///
    /// \param[in] ray ray
    /// \param[out] closest_hr closest hit record. valid when return true
    /// \return true when hit something.
    bool ray_scene_intersection(Ray const & ray, HitRecord & closest_hr);

    /// compute a framebuffer color and store it
    ///
    /// \param[in] pixel_x pixel position x
    /// \param[in] pixel_x pixel position y
    /// \param[in] ray     ray
    /// \param[in] nframe  current frame number
    void compute_color(
        Sint32 pixel_x,
        Sint32 pixel_y,
        Ray & ray,
        Sint32 nframe);

    /// render single frame.
    ///
    /// \param[in] nframe current frame number
    /// \return rendering status. 0 ... success
    Sint32 render_single_frame(Sint32 nframe);

    /// save a frame
    ///
    /// \param[in] frame_count frame counter for this save.
    /// \return rendering status. 0 ... success
    Sint32 save_frame(Sint32 frame_count);

private:
    /// geometry, reference to the trimesh, vector
    std::vector< TriMesh * > m_p_trimesh_vec;
    /// reference to the scene graph nodes
    std::vector< SceneGraphNode * > m_p_sgnode_vec;
    /// the scene graph
    SceneGraph m_scene_graph;
    /// current camera
    Camera m_camera;
    /// current RGBA buffer reference
    ImageFilm *  m_p_cur_framebuffer_ref;
    /// material group node reference
    SceneGraphNode * m_p_mat_group_node_ref;
    /// mesh group node reference
    SceneGraphNode * m_p_mesh_group_node_ref;
    /// hemisphere sampler
    SamplerUnitHemisphereUniform * m_p_hemisphere_sampler;
};

} // namespace ifgi

#endif // #ifndef IFGI_PATH_TRACER_IFGI_CPP_API_IFGI_CPP_RENDER_HH
