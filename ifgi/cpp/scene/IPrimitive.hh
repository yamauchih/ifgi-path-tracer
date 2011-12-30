//----------------------------------------------------------------------
// ifgi c++ implementation: IPrimitive.hh
// Copyright (C) 2010-2011 Yamauchi, Hitoshi
//----------------------------------------------------------------------
/// \file
/// \brief scene element primitive interface
#ifndef IFGI_PATH_TRACER_IFGI_CPP_SCENE_IPRIMITIVE_HH
#define IFGI_PATH_TRACER_IFGI_CPP_SCENE_IPRIMITIVE_HH

namespace ifgi
{

// forward declarations
class BBox;
class Ray;
class HitRecord;

//===============================================================================

/// Primitive class. interface for a primitive.
class IPrimitive
{
public:
    /// default constructor
    IPrimitive()
    {
        // empty
    }

    /// get class name. interface method.
    /// \return class name
    virtual std::string get_classname() const = 0;

    /// set primitive associated name.
    /// \return primitive name
    virtual void set_name(std::string const & name) = 0;

    /// get primitive associated name.
    /// \return primitive name
    virtual std::string get_name() const = 0;

    /// set primitive's material name.
    /// \param[in] mat_name material name
    virtual void set_material_name(std::string & mat_name) = 0;

    /// get primitive"s material name.
    /// \return material name
    virtual std::string get_material_name() const = 0;

    /// set primitive"s material global index.
    /// material index is scene global index for fast material lookup.
    /// \param[in] mat_idx material index (for fast lookup);
    virtual void set_material_global_index(Sint32 mat_idx) = 0;

    /// get primitive"s material global index.
    /// If -1, no material is indicated.
    /// \return global material index
    virtual Sint32 get_material_global_index() const = 0;

    /// get the bounding box. interface method.
    /// \return bounding box of this primitive.
    virtual BBox const & get_bbox() = 0;

    /// can this primitive intersect with a ray?
    ///
    /// Some of primitives can not directory intersect with a ray. For
    /// example, TriMesh. These primitives need refinement first.
    virtual bool can_intersect() const = 0;

    /// compute ray intersection. interface method.
    /// \param[in]  ray a ray
    /// \param[out] a HitRecord
    /// \return true when hit
    virtual bool ray_intersect(Ray const & ray, HitRecord & hr) const = 0;
};


/// ----------------------------------------------------------------------

// class Triangle(IPrimitive){
//     /// A triangle.
//     ///

//     def _init__(){
//         /// default constructor.
//         ///
//         super(Triangle, ).__init__();
//         this->__vertex = None
//         this->__bbox   = None


//     def get_classname(){
//         return "Triangle"


//     def get_bbox(){
//         if this->__bbox == None:
//             raise StandardError, ("Invalid triangle, no bounding box.");

//         return this->__bbox


//     def can_intersect(){
//         /// can a triangle intersect with a ray? Yes.
//         ///
//         return True


//     def ray_intersect(_ray){
//         /// compute ray intersection. interface method.
//         \param[in]  ray a ray
//         \return a HitRecord. None when not hit.

//         ///
//         assert(this->__vertex != None);

//         /// Cramer"s rule based ray-triangle intersection

//         /// get s1
//         e1 = this->__vertex[1] - this->__vertex[0]
//         e2 = this->__vertex[2] - this->__vertex[0]
//         s1 = numpy.cross(_ray.get_dir(), e2);
//         div = numpy.dot(s1, e1);
//         if div == 0.0:
//             return None
//         inv_div = 1.0/div

//         /// get barycentric coord b1
//         d = ray.get_origin() - this->__vertex[0]
//         b1 = numpy.dot(d, s1) * inv_div
//         if ((b1 < 0.0) or (b1 > 1.0)){
//             return None

//         /// get barycentric coord b2
//         s2 = numpy.cross(d, e1);
//         b2 = numpy.dot(_ray.get_dir(), s2) * inv_div
//         if ((b2 < 0.0) or ((b1 + b2) > 1.0)){
//             return None

//         /// get intersection point (distance t);
//         t = numpy.dot(e2, s2) * inv_div
//         if ((t < ray.get_min_t()) or (t > ray.get_max_t())){
//             return None

//         /// print "Hit: t = " + str(t) + ", b1 = " + str(b1) + ", b2 = " + str(b2);
//         hr = HitRecord.HitRecord();
//         hr.dist = t
//         hr.intersect_pos = this->__vertex[0] + b1 * e1 + b2 * e2
//         hr.hit_primitive =
//         hr.hit_basis = OrthonomalBasis.OrthonomalBasis();
//         hr.hit_basis.init_from_uv(e1, e2) /// set normal
//         return hr


//     def set_vertex(_v0, v1, v2){
//         /// Set triangle vertices.
//         \param[in] v0 vertex 0
//         \param[in] v1 vertex 1
//         \param[in] v2 vertex 2
//         ///
//         this->__vertex = [_v0, v1, v2]
//         this->__update_bbox();


//     def _update_bbox(){
//         this->__bbox = BBox();
//         this->__bbox.insert_point(this->__vertex[0]);
//         this->__bbox.insert_point(this->__vertex[1]);
//         this->__bbox.insert_point(this->__vertex[2]);

// /// ----------------------------------------------------------------------

// class TriMesh(IPrimitive){
//     /// TriMesh: simple triangle mesh primitive
//     ///

//     def _init__(_mash_name, mat_name){
//         /// default constructor (public).///
//         super(TriMesh, ).__init__();
//         super(TriMesh, ).set_name(_mash_name);
//         super(TriMesh, ).set_material_name(_mat_name);

//         /// geometry information
//         this->vertex_list       = []
//         this->face_idx_list     = []
//         this->texcoord_list     = []
//         this->texcoord_idx_list = []
//         this->normal_list       = []
//         this->normal_idx_list   = []
//         this->bbox              = BBox();

//         /// global material index of this geometry (valid after
//         /// preprocessing);
//         this->material_index = -1


//     def get_classname(){
//         /// get class name. interface method.
//         \return class name
//         ///
//         return "TriMesh"


//     def get_bbox(){
//         /// get the bounding box. interface method.
//         \return bounding box of this primitive.
//         ///
//         return this->bbox


//     def can_intersect(){
//         /// can TriMesh primitive intersect with a ray? no.
//         This object needs refinement.
//         ///
//         return False


//     def set_data(_vlist, fidxlist, tclist, tcidxlist, nlist, nidxlist){
//         /// set data (public).

//         \param[in]  vlist     vertex list (len(_vlist) must be > 0);
//         \param[in]  fidxlist  face index list
//         \param[in]  tclist    texture coordinate list
//         \param[in]  tcidxlist texture coordinate index list
//         \param[in]  nlist     normal list
//         \param[in]  nidxlist  normal index list
//         ///
//         assert(len(_vlist) > 0) /// at least, some points must be there.
//         this->vertex_list       = vlist
//         this->face_idx_list     = fidxlist
//         this->texcoord_list     = tclist
//         this->texcoord_idx_list = tcidxlist
//         this->normal_list       = nlist
//         this->normal_idx_list   = nidxlist
//         this->update_bbox();


//     def set_material_index(_mat_idx){
//         /// set global material index.

//         \param[in] mat_idx global material index.
//         ///
//         /// FIXME: Or shall I push this information to each triangles?
//         this->material_index = mat_idx


//     def info_summary(){
//         /// summary information

//         \return summary information string
//         ///
//         ret_str =
//             "/// vertices     = " + str(len(this->vertex_list))   + "\n" +
//             "/// faces        = " + str(len(this->face_idx_list)) + "\n" +
//             "/// texcoords    = " + str(len(this->texcoord_list)) + "\n" +
//             "/// texcoord idx = " + str(len(this->texcoord_idx_list)) + "\n" +
//             "/// normal       = " + str(len(this->normal_list))   + "\n" +
//             "/// normal idx   = " + str(len(this->normal_idx_list)) + "\n" +
//             "bbox           = " + str(this->get_bbox())         + "\n" +
//             "material idx   = " + str(this->material_index);

//         return ret_str


//     def update_bbox(){
//         /// update bounding box according to current vertex list (public).
//         ///
//         this->bbox.invalidate()  /// reset the bbox
//         for pos in this->vertex_list:
//             this->bbox.insert_point(pos);


//     def is_valid(){
//         /// is this valid object? (public).
//         At least len(vertex_list) > 0
//         ///
//         if len(this->vertex_list) > 0:
//             return True
//         return False


//     def ray_intersect(_ray){
//         /// compute ray intersection. (public).
//         \param[in] ray a ray
//         \return a HitRecord. None if no hit.
//         ///
//         /// NIN: bounding box test?

//         trimesh_hr = HitRecord.HitRecord();

//         /// following init is make sure only (done in the HitRecord.__init__());
//         trimesh_hr.dist = sys.float_info.max
//         trimesh_hr.hit_primitive = None

//         for fi in this->face_idx_list:
//             tri = Triangle();
//             tri.set_vertex(this->vertex_list[fi[0]],
//                            this->vertex_list[fi[1]],
//                            this->vertex_list[fi[2]]);

//             hr = tri.ray_intersect(_ray);
//             if hr != None:
//                 if trimesh_hr.dist > hr.dist:
//                     trimesh_hr.dist = hr.dist
//                     trimesh_hr.intersect_pos = hr.intersect_pos
//                     trimesh_hr.hit_primitive = tri
//                     trimesh_hr.hit_basis = hr.hit_basis
//                     trimesh_hr.hit_material_index = this->material_index

//         if trimesh_hr.hit_primitive != None:
//             return trimesh_hr

//         return None

} // namespace ifgi
#endif // #ifndef IFGI_PATH_TRACER_IFGI_CPP_SCENE_IPRIMITIVE_HH
