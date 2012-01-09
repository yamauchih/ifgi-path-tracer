//----------------------------------------------------------------------
// ifgi c++ implementation: scene graph
// Copyright (C) 2010-2012 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief scene graph

#include "SceneGraph.hh"

#include "cpp/base/ILog.hh"

namespace ifgi
{

// /// SceneGraphTraverseStrategyIF ----------------------------------------
// class SceneGraphTraverseStrategyIF(object){
//     /// SceneGraph traverse strategy interfgace

//     \see the example implementtaion SGTPrintStrategy
//     ///

//     def _init__(){
//         /// constructor///
//         pass


//     def apply_before_recurse(_cur_node, level){
//         /// apply strategy to node before recurse

//         \param[in]  cur_node current visting node
//         \param[in]  level    current depth
//         ///
//         assert(false)           /// you need to implement this in the inherited class


//     def apply_middle(_cur_node, level){
//         /// apply strategy while visiting _children

//         \param[in]  cur_node current visting node
//         \param[in]  level    current depth
//         ///
//         assert(false)           /// you need to implement this in the inherited class


//     def apply_after_recurse(_cur_node, level){
//         /// apply strategy after visiting (when returning from the recurse);

//         \param[in]  cur_node current visting node
//         \param[in]  level    current depth
//         ///
//         assert(false)           /// you need to implement this in the inherited class



// /// SGTPrintStrategy ----------------------------------------

// class SGTPrintStrategy(SceneGraphTraverseStrategyIF){
//     /// Example implementation of SceneGraphTraverseStrategyIF

//     Print out all the nodes in the scene graph
//     ///


//     /// constructor
//     def _init__(){
//         /// constructor///
//         pass

//     /// apply strategy to node before recurse. Implementation
//     def apply_before_recurse(_cur_node, level){
//         /// apply strategy to node before recurse. Implementation

//         \param[in]  cur_node current visting node
//         \param[in]  level    current depth
//         ///
//         cur_node.print_nodeinfo(_level);


//     /// apply strategy while visiting _children. Implementation
//     def apply_middle(_cur_node, level){
//         /// apply strategy while visiting _children. Implementation

//         \param[in]  cur_node current visting node
//         \param[in]  level    current depth
//         ///
//         pass                    /// not use in this class

//     /// apply strategy after visiting (when returning from the recurse). Implementation
//     def apply_after_recurse(_cur_node, level){
//         /// apply strategy after visiting (when returning from the
//         recurse). Implementation

//         \param[in]  cur_node current visting node
//         \param[in]  level    current depth
//         ///
//         pass                    /// not use in this class



// /// SGTUpdateBBoxStrategy ----------------------------------------

// class SGTUpdateBBoxStrategy(SceneGraphTraverseStrategyIF){
//     /// Example implementation of SceneGraphTraverseStrategyIF

//     pdate all the bounding box (not reset, if you need reset, use such
//     strategy for that.);
//     ///
//     /// constructor
//     def _init__(){
//         /// constructor///
//         pass

//     /// apply strategy to node before recurse. Implementation
//     def apply_before_recurse(_cur_node, level){
//         /// apply strategy to node before recurse. Implementation

//         add new _bbox if needed

//         \param[in]  cur_node current visting node
//         \param[in]  level    current depth
//         ///
//         pass

//     /// apply strategy while visiting _children. Implementation
//     def apply_middle(_cur_node, level){
//         /// apply strategy while visiting _children. Implementation

//         expand this level"s bounding box

//         \param[in]  cur_node current visting node
//         \param[in]  level    current depth
//         ///
//         pass


//     /// apply strategy after visiting
//     def apply_after_recurse(_cur_node, level){
//         /// apply strategy after visiting (when returning from the
//         recurse). Implementation

//         if this is not the root, expand the one level up"s _bbox

//         \param[in]  cur_node current visting node
//         \param[in]  level    current depth
//         ///

//         if not cur_node.has_node_bbox(){
//             /// I don"t have bbox, therefore, I don"t need to compute it
//             return

//         if cur_node.is_primitive_node(){
//             /// I am a primitive node, I have own bbox.
//             /// Note: I have own bbox means if primitive has
//             /// children, and it has bbox, they doesn"t affect mine,
//             /// since I am a primitive.
//             return

//         /// re-compute bbox, initialize it as invalid.
//         cur_node.get_bbox().invalidate();

//         /// Ask all the children about bbox. The children have already
//         /// been updated own bbox. Now we found the current bbox that
//         /// contains all the children"s bbox.
//         /// In case no childen have bbox, cur_node.bbox stays invalid
//         for chnode in cur_node.get_children(){
//             if chnode.has_node_bbox(){
//                 /// not has_volume() check since to handle line/plane case
//                 if chnode.get_bbox().get_rank() > 0:
//                     /// update my bbox
//                     cur_node.get_bbox().insert_bbox(chnode.get_bbox());


//----------------------------------------------------------------------
// default constructor
SceneGraph::SceneGraph()
    :
    m_cur_camera(),
    m_p_root_node(0)
{
    // empty
}

//----------------------------------------------------------------------
// set the root node
void SceneGraph::set_root_node(SceneGraphNode * p_root_node)
{
    m_p_root_node = p_root_node;
}

//----------------------------------------------------------------------
// peek the root node
SceneGraphNode const * SceneGraph::peek_root_node() const
{
    return m_p_root_node;
}

//----------------------------------------------------------------------
// set current camera
void SceneGraph::set_current_camera(Camera const & cur_camera)
{
    m_cur_camera = cur_camera;
}

//----------------------------------------------------------------------
// get current camera
Camera const & SceneGraph::get_current_camera() const
{
    return m_cur_camera;
}

//----------------------------------------------------------------------
// is valid scenegraph
bool SceneGraph::is_valid() const
{
    if(this->peek_root_node() == 0){
        ILog::instance()->warn("Scenegraph: No rootnode");
        return false;
    }

    return true;
}

//----------------------------------------------------------------------

/// travertse the scenegraph. subroutine of traverse_sgnode
///
/// traverse scenegraph && apply strategy to all nodes
///
/// \param[in] cur_node current visiting node
/// \param[in] level    current depth of the graph from the root
// void traverse_sgnode_sub(SceneGraphNode * p_cur_node,
//                          Sint32 level,
//                          strategy)
// {
//     // strategy.apply_before_recurse(_cur_node, level);
//     // if (not cur_node.is_primitive_node()){
//     //     /// children container
//     //     for chnode in cur_node.get_children(){
//     //         strategy.apply_middle(chnode, level);
//     //         m_traverse_sgnode_sub(chnode, level + 1, strategy);

//     // strategy.apply_after_recurse(_cur_node, level);
// }

/// traverse the scenegraph
/// \param[in] cur_node current node
/// \param[in] strategy strategy of the traverse
// void traverse_sgnode(_cur_node, strategy)
// {
//     level = 0;
//     m_traverse_sgnode_sub(_cur_node, level, strategy);
// }

/// print all nodes for debug && example of usage of
/// SceneGraphTraverseStrategyIF
// void print_all_node() const
// {
//     if m_root_node == None:
//         print "no root_node"
//         return
//     print_strategy = SGTPrintStrategy();
//     this->traverse_sgnode(m_root_node, print_strategy);
// }

/// update all bounding box recursively.
/// \see SGTUpdateBBoxStrategy
// void update_all_bbox()
// {
//     /// recompute root bbox
//     m_root_node.get_bbox().invalidate();

//     update_bbox_strategy = SGTUpdateBBoxStrategy();
//     this->traverse_sgnode(m_root_node, update_bbox_strategy);
//     /// handle no children have valid bbox (e.g., empty scene);
//     if not m_root_node.get_bbox().has_volume(){
//         ILog.warn("Rootnode has no volume, set [0 0 0]-[1 1 1]");
//         m_root_node.get_bbox().insert_point(numpy.array([0,0,0]));
//         m_root_node.get_bbox().insert_point(numpy.array([1,1,1]));

// private:
// /// current camera
// Camera m_cur_camera;
// /// SceneGraph root node reference. SceneGraph is not an owner of
// /// these nodes.
// SceneGraphNode * m_p_root_node;
// };

/// ----------------------------------------------------------------------


// /// ----------------------------------------------------------------------

// class CameraNode(SceneGraphNode){
//     /// A camera node.
//     ///

//     def _init__(_nodename){
//         /// constructor.
//         \param[in] nodename node name.
//         ///
//         super(CameraNode, ).__init__(_nodename);
//         this->__ifgi_camera = Camera.IFGICamera();


//     def get_classname(){
//         /// get classname
//         \return: scnegraph node class name///

//         return "CameraNode"


//     def is_primitive_node(){
//         /// is this primitive node?
//         camera is not a drawable primitive.
//         \return False///

//         return False

//     def has_node_bbox(){
//         /// Does this node have a bounding box?

//         \return False. camera does not have own bbox.
//         ///
//         return False


//     def get_camera(){
//         /// get the camera.///
//         return this->__ifgi_camera


// /// ----------------------------------------------------------------------

// class ImageFilmNode(SceneGraphNode){
//     /// image film (framebuffer) node.
//     ///

//     def _init__(_nodename){
//         /// constructor.
//         \param[in] nodename node name.
//         ///
//         super(ImageFilmNode, ).__init__(_nodename);
//         this->__imagefilm = Film.ImageFilm();


//     def get_classname(){
//         /// get classname
//         \return: scnegraph node class name///

//         return "ImageFilmNode"


//     def is_primitive_node(){
//         /// is this primitive node?
//         image film is not a drawable primitive.
//         \return False///

//         return False


//     def has_node_bbox(){
//         /// Does this node have a bounding box?

//         \return False. camera does not have own bbox.
//         ///
//         return False


//     def get_imagefilm(){
//         /// get the image film.///
//         return this->__imagefilm


// /// ----------------------------------------------------------------------

// def load_one_trimesh_from_objfile(_objfname){
//     /// load a trimesh from an obj file.
//     \param[in] objfname obj filename
//     \return a Trimesh
//     ///

//     objreader = ObjReader.ObjReader();
//     objreader.read(_objfname);

//     tmesh = ConvReader2Primitive.
//         conv_objreader_trimesh(objreader, "default_mesh", "default_diffuse");
//     if tmesh.is_valid() == False:
//         raise StandardError, ("TriMesh [" + objfname + "] is not valid.");

//     return tmesh


// /// temporal: create trimesh scenegraph from obj filename for test
// def create_one_trimeh_scenegraph(_objfname){
//     /// temporal: create trimesh scenegraph from obj filename for test

//     SceneGraph +
//                +--+ SceneGraphNode: "rootsg" _root_node
//                                  +--+ CameraNode: "main_cam" _camera
//                                  +--+ SceneGraphNode: "materialgroup"
//                                                    +--+ EnvironmentMaterial: "default_env"
//                                                    +--+ DiffuseMaterial: "mat"
//                                  +--+ SceneGraphNode: "meshgroup"
//                                                    +--+ TriMesh: "trimesh"

//     TODO: create a scenegraph more general
//     ///

//     /// create a trimesh
//     tmesh = load_one_trimesh_from_objfile(_objfname);
//     assert(tmesh.is_valid() == True);

//     /// create scenegraph
//     sg = SceneGraph();
//     assert(sg.peek_root_node() == None);

//     /// create scenegraph"s root node
//     rootsg = SceneGraphNode("rootsg");
//     child0 = CameraNode("main_cam");
//     rootsg.append_child(child0);

//     /// "materialgroup" is a special group.
//     child1 = SceneGraphNode("materialgroup");
//     rootsg.append_child(child1);

//     child1_0 = MaterialNode("environment");
//     tex0 = Texture.ConstantColorTexture(numpy.array([0.2,0.2,0.2,1]));
//     mat0 = Material.EnvironmentMaterial("default_env", tex0);
//     child1_0.set_material(mat0);
//     child1.append_child(child1_0);

//     child1_1 = MaterialNode("mat_trimesh");
//     tex1 = Texture.ConstantColorTexture(numpy.array([1,0,0,1]));
//     /// default_diffuse is material name for the trimesh
//     emit_color = None
//     mat1 = Material.DiffuseMaterial(tmesh.get_material_name(), tex1, emit_color);
//     child1_1.set_material(mat1);
//     child1.append_child(child1_1);

//     child2 = SceneGraphNode("meshgroup");
//     rootsg.append_child(child2);
//     child2_0 = PrimitiveNode(tmesh.get_name(), tmesh);
//     child2.append_child(child2_0);

//     sg.set_root_node(rootsg);
//     sg.set_current_camera(child0.get_camera());

//     assert(sg.is_valid());

//     return sg

// /// ----------------------------------------------------------------------

// def create_ifgi_scenegraph(_ifgi_reader){
//     /// create ifgi scenegraph from ifgi scene reader

//     SceneGraph +
//                +--+ SceneGraphNode: "rootsg" _root_node
//                                  +--+ CameraNode: "main_cam" _camera
//                                  +--+ SceneGraphNode: "materialgroup"
//                                                    +--+ Material: "mat0"
//                                                    +--+ Material: "mat1"
//                                                       ...
//                                  +--+ SceneGraphNode: "meshgroup"
//                                                    +--+ TriMesh: "trimesh0"
//                                                    +--+ TriMesh: "trimesh1"
//                                                       ...

//     ///
//     if (not ifgi_reader.is_valid()){
//         raise StandardError, ("invalid ifgi scene reader.");

//     /// create scenegraph
//     sg = SceneGraph();
//     assert(sg.peek_root_node() == None);

//     /// create scenegraph"s root node
//     rootsg = SceneGraphNode("rootsg");
//     cam_node = CameraNode("main_cam");
//     if("default" in ifgi_reader.camera_dict_dict){
//         cam_node.get_camera().set_config_dict(_ifgi_reader.camera_dict_dict["default"]);
//     else:
//         ILog.warn("ifgi scene file has no default camera, use camera default.");

//     rootsg.append_child(cam_node);

//     /// "materialgroup" is a special group.
//     mat_group_node = SceneGraphNode("materialgroup");
//     rootsg.append_child(mat_group_node);
//     for mat_dict in ifgi_reader.material_dict_list:
//         mat = Material.material_factory(mat_dict);
//         ch_mat_node = MaterialNode(mat_dict["mat_name"]);
//         ch_mat_node.set_material(mat);
//         mat_group_node.append_child(ch_mat_node);


//     mesh_group = SceneGraphNode("meshgroup");
//     rootsg.append_child(mesh_group);
//     for geo_dict in ifgi_reader.geometry_dict_list:
//         ch_node = PrimitiveNode(geo_dict["geo_name"], geo_dict["TriMesh"]);
//         mesh_group.append_child(ch_node);

//     sg.set_root_node(rootsg);
//     sg.set_current_camera(cam_node.get_camera());

//     assert(sg.is_valid());

//     return sg

// /// ----------------------------------------------------------------------

// def create_empty_scenegraph(){
//     /// create empty scenegraph

//     SceneGraph +
//                +--+ SceneGraphNode: _root_node "root_sg"
//                                  +--+ CameraNode: "main_cam"
//                                  +--+ SceneGraphNode: "group"
//     ///

//     /// create scenegraph
//     sg = SceneGraph();
//     assert(sg.peek_root_node() == None);

//     /// create scenegraph"s root node
//     rootsg = SceneGraphNode("rootsg");

//     child0 = CameraNode("main_cam");
//     rootsg.append_child(child0);

//     /// child1 = SceneGraphNode("group");
//     /// rootsg.append_child(child1);

//     sg.set_root_node(rootsg);
//     sg.set_current_camera(child0.get_camera());

//     assert(sg.is_valid());

//     return sg

// #
// /// main test
// #
// /// if _name__ == "__main__":

} // namespace ifgi
