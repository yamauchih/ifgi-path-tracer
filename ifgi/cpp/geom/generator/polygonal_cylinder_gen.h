// ==========================================================================
// Polygonal cylinder generator
// ifgi-path-tracer/cpp/geom/generator
// ==========================================================================
// Copyright (C) 2011 Yamauchi, Hitoshi Sunday Researcher
// ==========================================================================
/// \file
/// \brief Generate a (polygonal) cylinder from a center point list

#ifndef IFGI_PATH_TRACER_CPP_GEOM_GENERATOR_POLYGONAL_CYLINDER_GEN_H
#define IFGI_PATH_TRACER_CPP_GEOM_GENERATOR_POLYGONAL_CYLINDER_GEN_H

#include <vector>
#include <string>

class Vector3f{
public:
    explicit Vector3f(float x, float y, float z){
    }
    float operator[](size_t i) const {
        return 0.0f;
    }
    float x;
    float y;
    float z;
};
class Vector3i{
public:
    explicit Vector3i(int x, int y, int z){
    }
    int operator[](size_t i) const {
        return 1;
    }
};

/// Simple polygonal cylinder generator.
///
/// The normal of top and bottom polygons are always z+ (0,0,1)
class Polygonal_cylinder_gen
{
public:
    /// std::vector of Vector3f
    typedef std::vector< Vector3f > Float32_3_vec;
    /// std::vector of Vector3i
    typedef std::vector< Vector3i > Sint32_3_vec;

public:
    /// constructor
    Polygonal_cylinder_gen();
    /// destructor
    virtual ~Polygonal_cylinder_gen();

    /// clear the input center points and generated data
    void clear();

    /// set polygon parameter
    /// \param[in] center_point polygon center point
    /// \param[in] radius       polygon radius
    /// \return true when append succeeded
    bool append_center_point(Vector3f const & center_point, float radius);

    /// set generate top and bottom triangles.
    /// \param[in] is_gen generate top and bottom triangles when True
    void set_generate_segment_tris(bool is_gen);

    /// set n of n-gon.
    /// \param[in] n_gon top and bottom polygon n-gon
    void set_n_gon(int n_gon);

    /// generate a cylinder
    void gen_cylinder();

    /// export obj file
    /// \param[in] _objfname exporting obj file name
    // bool export_obj(self, _objfname):

private:
    /// check we can generate a cylinder.
    // raise an exception if not.
    bool is_able_to_gen() const;

    /// generate vertices for the cylinder
    void gen_vertex();

    /// generate segment triangles (horizontal top/bottom of the cylinder).
    /// All triangles faces z+ direction.
    /// gen_vertex should be run before.
    void gen_segment_tris();

    /// generate cylinder side polygons
    void gen_side_polygon();

    /// check the face index's validity
    /// raise an exception when not valid
    bool is_face_index_valid() const;

    /// string representation
    /// \return string representation of this object
    std::string to_string() const;

private:
    /// segment polygon normal. basis n
    Vector3f m_poly_normal;
    /// segment polygon tangent. basis t
    Vector3f m_poly_tangent;
    /// segment polygon binomal. basis b
    Vector3f m_poly_binomal;
    /// center point vector
    std::vector< Vector3f > m_center_vec;
    /// radius vector
    std::vector< float >    m_radius_vec;
    /// n-gon. fixed for a cylinder
    int m_n_gon;
    /// switch to generate segment polygon triangles
    bool m_is_gen_segment_tris;
    /// generated vertices vector
    Float32_3_vec  m_vertex_vec;
    /// generated segment face vector
    Sint32_3_vec m_segment_face_vec;
    /// generated side face vector
    Sint32_3_vec m_side_face_vec;
};

#endif // #ifndef IFGI_PATH_TRACER_CPP_GEOM_GENERATOR_POLYGONAL_CYLINDER_GEN_H
