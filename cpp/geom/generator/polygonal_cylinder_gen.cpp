// ==========================================================================
// Polygonal cylinder generator
// ifgi-path-tracer/cpp/geom/generator
// ==========================================================================
// Copyright (C) 2011 Yamauchi, Hitoshi Sunday Researcher
// ==========================================================================
/// \file
/// \brief Generate a (polygonal) cylinder from a center point list

#include "polygonal_cylinder_gen.h"

#include <cassert>
#include <cstddef>
#include <cmath>
#include <iostream>
#include <sstream>

//----------------------------------------------------------------------
// constructor
Polygonal_cylinder_gen::Polygonal_cylinder_gen()
    :
    m_poly_normal (0.0, 0.0, 1.0),
    m_poly_tangent(1.0, 0.0, 0.0),
    m_poly_binomal(0.0, 1.0, 0.0),
    // m_center_vec(),
    // m_radius_vec(),
    m_n_gon(0)
    // m_is_gen_segment_tris(false)
    // m_vertex_vec(),
    // m_segment_face_vec(),
    // m_side_face_vec()
{
    // empty
}

//----------------------------------------------------------------------
Polygonal_cylinder_gen::~Polygonal_cylinder_gen()
{
    this->clear();
}

//----------------------------------------------------------------------
// clear the input center points and generated data
void Polygonal_cylinder_gen::clear()
{
    m_center_vec.clear();
    m_radius_vec.clear();

    m_vertex_vec      .clear();
    m_segment_face_vec.clear();
    m_side_face_vec   .clear();
}

//----------------------------------------------------------------------
bool Polygonal_cylinder_gen::append_center_point(
    Vector3f const & center_point, float radius)
{
    assert(radius > 0.0);
    // sanity check. without this check still generates cylinders,
    // but, may be looked broken
    size_t list_sz = m_center_vec.size();
    if ((list_sz > 0) &&  (m_center_vec.at(list_sz - 1)[2] >= center_point[2])){
        std::cerr << "z values must be acendent order. "
            // FIXME
                  << (m_center_vec[list_sz - 1].x) << ", " << center_point.x
                  << std::endl;
        return false;
    }

    m_center_vec.push_back(center_point);
    m_radius_vec.push_back(radius);

    return true;
}

//----------------------------------------------------------------------

void Polygonal_cylinder_gen::set_generate_segment_tris(bool is_gen)
{
    m_is_gen_segment_tris = is_gen;
}

//----------------------------------------------------------------------

void Polygonal_cylinder_gen::set_n_gon(int n_gon)
{
    assert(n_gon >= 3);

    m_n_gon = n_gon;
}

//----------------------------------------------------------------------

void Polygonal_cylinder_gen::gen_cylinder()
{
    assert(this->is_able_to_gen());

    this->gen_vertex();
    if (m_is_gen_segment_tris){
        this->gen_segment_tris();
    }
    this->gen_side_polygon();
}

//----------------------------------------------------------------------

// def Polygonal_cylinder_gen::export_obj(self, _objfname)
// {
//     assert(self.__is_face_index_valid());

//     if ((_objfname == None) or (len(_objfname) == 0))
//         raise StandardError, ('empty obj output file name.');

//     objf = open(_objfname, 'w');

//     // output mesh info
//     vtx_count  = len(m_vertex_vec);
//     face_count = len(m_side_face_vec) + len(m_segment_face_vec);
//     if (vtx_count == 0){
//         raise StandardError, ('no vertices.');
//     }
//     objf.write('# ' + str(vtx_count) + ' ' + str(face_count) + ' 0\n');

//     // vertices
//     for(v in m_vertex_vec){
//         objf.write('v ' + str(v[0]) + ' ' + str(v[1]) + ' ' + str(v[2]) + '\n');
//     }

//     // top and bottom faces
//     for (f in m_segment_face_vec){
//         objf.write('f ' + str(f[0]+1) + ' ' + str(f[1]+1) + ' ' + str(f[2]+1) + '\n');
//     }

//     // side faces
//     for (f in m_side_face_vec){
//         objf.write('f ' + str(f[0]+1) + ' ' + str(f[1]+1) + ' ' + str(f[2]+1) + '\n');
//     }
// }

//----------------------------------------------------------------------

bool Polygonal_cylinder_gen::is_able_to_gen() const
{
    if (m_n_gon < 3){
        std::cerr << "n-gon should be at least n >= 3." << std::endl;
        return false;
    }
    if (m_center_vec.size() < 2) {
        std::cerr << "The number of center points must be > 1." << std::endl;
        return false;
    }
    return true;
}

//----------------------------------------------------------------------

void Polygonal_cylinder_gen::gen_vertex()
{
    m_vertex_vec.clear();
    double const step_angle = (2 * M_PI) / static_cast< double >(m_n_gon);

    for(int seg = 0; seg < m_center_vec.size(); ++seg){
        for(int i = 0; i < m_n_gon; ++i){
            double const rad  = m_radius_vec[seg];
            Vector3f const cp = m_center_vec[seg];
            Vector3f vtx_point(0.0, 0.0, 0.0);
            vtx_point.x = rad * cos(i * step_angle) + cp[0];
            vtx_point.y = rad * sin(i * step_angle) + cp[1];
            vtx_point.z = cp[2];
            m_vertex_vec.push_back(vtx_point);
        }
    }
}

//----------------------------------------------------------------------

void Polygonal_cylinder_gen::gen_segment_tris()
{
    assert((m_vertex_vec.size()) == (m_center_vec.size() * m_n_gon));

    m_segment_face_vec.clear();
    int const n = m_n_gon;
    for(int seg = 0; seg < m_center_vec.size(); ++seg){
        // base index of current processing segment triangles
        int const n_seg = seg * n;
        for(int i = 1; i < ((n + 1) - 2); ++i){
            Vector3i const fidx(0 + n_seg, i + n_seg, i + 1 + n_seg);
            m_segment_face_vec.push_back(fidx);
        }
    }
}

//----------------------------------------------------------------------

void Polygonal_cylinder_gen::gen_side_polygon()
{
    int const seg_count = m_center_vec.size();
    assert(seg_count >= 2);

    m_side_face_vec.clear();
    int const n = m_n_gon;

    for(int seg = 0; seg < (seg_count - 1); ++seg){
        int const bidx = seg * n;
        for(int i = 0; i < (n - 1); ++i){
            Vector3i const f1(bidx + i, bidx + i + 1, bidx + n + i + 1);
            Vector3i const f2(bidx + i, bidx + n + i + 1, bidx + n + i);
            m_side_face_vec.push_back(f1);
            m_side_face_vec.push_back(f2);
        }
        // the last quad of this segment
        Vector3i const last_f1(bidx + n - 1, bidx + 0, bidx + n);
        Vector3i const last_f2(bidx + n - 1, bidx + n, bidx + (2 * n - 1));
    }
}

//----------------------------------------------------------------------

bool Polygonal_cylinder_gen::is_face_index_valid() const
{
    int const vsize = m_vertex_vec.size();

    for(std::vector< Vector3f >::const_iterator vi = m_segment_face_vec.begin();
        vi != m_segment_face_vec.end(); ++vi)
    {
        for(int i = 0; i < 3; ++i){
            int const fidx = (*vi)[i];
            if((fidx < 0) || (fidx >= vsize)){
                std::cerr << "segment face list has invalid face index."
                          << std::endl;
                return false;
            }
        }
    }

    for(std::vector< Vector3f >::const_iterator vi = m_side_face_vec.begin();
        vi != m_side_face_vec.end(); ++vi)
    {
        for(int i = 0; i < 3; ++i){
            int const fidx = (*vi)[i];
            if((fidx < 0) || (fidx >= vsize)){
                std::cerr << "side face list has invalid face index."
                          << std::endl;
                return false;
            }
        }
    }
}

//----------------------------------------------------------------------
// string representation
std::string Polygonal_cylinder_gen::to_string() const
{
    std::stringstream sstr;
    sstr << "Polygonal_cylinder_gen: "
         << m_center_vec.size()       << " centers, "
         << m_n_gon                   << "-gon, "
         << m_vertex_vec.size()       << " vertices, "
         << m_segment_face_vec.size() << " seg tris, "
         << m_side_face_vec.size()    << " side faces";
    return sstr.str();
}

//----------------------------------------------------------------------
