// ==========================================================================
// Polygonal cylinder generator
// ifgi-path-tracer/cpp/geom/generator
// ==========================================================================
// Copyright (C) 2011 Yamauchi, Hitoshi Sunday Researcher
// ==========================================================================
/// \file
/// \brief Generate a (polygonal) cylinder from a center point list

#ifndef IFGI_PATH_TRACER/CPP/GEOM/GENERATOR/POLYGONAL_CYLINDER_GEN_H
#define IFGI_PATH_TRACER/CPP/GEOM/GENERATOR/POLYGONAL_CYLINDER_GEN_H

#include <vector>

/// Simple poltgonal cylinder generator.
///
/// The normal of top and bottom polygons are always z+ (0,0,1)
class Polygonal_cylinder_gen
{
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
    void append_center_point(Vector3f const & center_point, float radius);

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
    bool is_able_to_gen();

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
    bool is_face_index_valid();

    // # string representation
    // def __str__(self):
    //     return 'Polygonal_cylinder_gen: ' + \
    //         str(len(self.__center_list)) + ' centers, ' + \
    //         str(self.__n_gon) + '-gon, ' + \
    //         str(len(self.__vertex_list)) + ' vertices, ' + \
    //         str(len(self.__segment_face_list)) + ' seg tris, ' + \
    //         str(len(self.__side_face_list)) + ' side faces'
    //                            };
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
};
