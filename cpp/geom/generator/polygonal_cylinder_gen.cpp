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

#include <cassert>

//----------------------------------------------------------------------
// constructor
Polygonal_cylinder_gen::Polygonal_cylinder_gen()
    :
    m_poly_normal (0.0, 0.0, 1.0),
    m_poly_tangent(1.0, 0.0, 0.0),
    m_poly_binomal(0.0, 1.0, 0.0),
    m_center_vec(),
    m_radius_vec(),
    m_n_gon(0),
    m_is_gen_segment_tris(false),
    m_vertex_vec(),
    m_segment_face_vec(),
    m_side_face_vec()
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
void clear()
{
    m_center_vec.clear();
    m_radius_vec.clear();

    m_vertex_vec      .clear();
    m_segment_face_vec.clear();
    m_side_face_vec   .clear();
}

//----------------------------------------------------------------------
void append_center_point(Vector3f const & center_point, float radius)
{
    assert(radius > 0.0);

    // sanity check. without this check still generates cylinders,
    // but, may be looked broken
    list_sz = len(m_center_vec)
        if (list_sz > 0):
            if (m_center_vec[list_sz - 1][2] >= _center_point[2]):
                raise StandardError, ('z values must be acendent order.' +
                                      str(m_center_vec[list_sz - 1]) + ', ' +
                                      str(_center_point))

        m_center_vec.append(_center_point)
        m_radius_vec.append(_radius)


    def set_generate_segment_tris(self, _is_gen):
        """set generate top and bottom triangles.
        \param[in] _is_gen generate top and bottom triangles when True
        """
        self.__is_gen_segment_tris = _is_gen


    def set_n_gon(self, _n):
        """set n of n-gon.
        \param[in] _n top and bottom polygon n-gon
        """
        if (_n < 3):
            raise StandardError, ('_n be >= 3, but ' + str(_n))

        m_n_gon = _n


    def gen_cylinder(self):
        """generate a cylinder
        """
        self.__is_able_to_gen()

        self.__gen_vertex()
        if (self.__is_gen_segment_tris):
            self.__gen_segment_tris()
        self.__gen_side_polygon()


    def export_obj(self, _objfname):
        """export obj file
        \param[in] _objfname exporting obj file name
        """
        # assert(self.__is_face_index_valid())

        if ((_objfname == None) or (len(_objfname) == 0)):
            raise StandardError, ('empty obj output file name.')

        objf = open(_objfname, 'w')

        # output mesh info
        vtx_count  = len(m_vertex_vec)
        face_count = len(m_side_face_vec) + len(m_segment_face_vec)
        if (vtx_count == 0):
            raise StandardError, ('no vertices.')
        objf.write('# ' + str(vtx_count) + ' ' + str(face_count) + ' 0\n')

        # vertices
        for v in m_vertex_vec:
            objf.write('v ' + str(v[0]) + ' ' + str(v[1]) + ' ' + str(v[2]) + '\n')

        # top and bottom faces
        for f in m_segment_face_vec:
            objf.write('f ' + str(f[0]+1) + ' ' + str(f[1]+1) + ' ' + str(f[2]+1) + '\n')

        # side faces
        for f in m_side_face_vec:
            objf.write('f ' + str(f[0]+1) + ' ' + str(f[1]+1) + ' ' + str(f[2]+1) + '\n')


    def __is_able_to_gen(self):
        """check we can generate a cylinder.
        raise an exception if not.
        """
        if (m_n_gon < 3) :
            raise StandardError, ('illegal n_gon setting. _n be >= 3, but ' +\
                                      str(m_n_gon))

        if (len(m_center_vec) < 2) :
            raise StandardError, ('fail. less than two center points.')


    def __gen_vertex(self):
        """generate vertices for the cylinder
        """
        m_vertex_vec.clear();
        step_angle = (2 * math.pi) / m_n_gon

        for seg in xrange(0, len(m_center_vec)):
            for i in xrange(0, m_n_gon):
                rad = m_radius_vec[seg]
                cp  = m_center_vec[seg]
                x = rad * math.cos(i * step_angle) + cp[0]
                y = rad * math.sin(i * step_angle) + cp[1]
                z = cp[2]
                m_vertex_vec.append(numpy.array([x, y, z]))


    def __gen_segment_tris(self):
        """generate segment triangles (horizontal top/bottom of the cylinder).
        All triangles faces z+ direction.
        __gen_vertex should be run before.
        """
        if ((len(m_vertex_vec)) != (len(m_center_vec) * m_n_gon)):
            raise StandardError, ('unexpected vertex list length: ' +
                                  str(len(m_vertex_vec)) + ' != ' +
                                  str(len(m_center_vec) * m_n_gon) +
                                  ' Has __gen_vertex() not called?')

        m_segment_face_vec.clear();
        n = m_n_gon
        for seg in xrange(0, len(m_center_vec)):
            n_seg = seg * n     # base index of current processing segment triangles
            for i in xrange(1, ((n + 1) - 2)):
                m_segment_face_vec.append([0 + n_seg, i + n_seg, i + 1 + n_seg])


    def __gen_side_polygon(self):
        """generate cylinder side polygons
        """
        seg_count = len(m_center_vec)
        assert(seg_count >= 2)

        m_side_face_vec.clear();
        n = m_n_gon

        for seg in xrange(0, seg_count - 1):
            bidx = seg * n
            for i in xrange(0, n - 1):
                m_side_face_vec.append([bidx + i, bidx + i + 1, bidx + n + i + 1])
                m_side_face_vec.append([bidx + i, bidx + n + i + 1, bidx + n + i])

            # the last quad of this segment
            m_side_face_vec.append([bidx + n - 1, bidx + 0, bidx + n])
            m_side_face_vec.append([bidx + n - 1, bidx + n, bidx + (2 * n - 1)])


    def __is_face_index_valid(self):
        """check the face index's validity
        raise an exception when not valid
        """
        vsize = len(m_vertex_vec)

        for fset in m_segment_face_vec:
            for i in fset:
                if (i < 0) or (i >= vsize):
                    raise StandardError, ('segment face list has invalid face index.')

        for fset in m_side_face_vec:
            for i in fset:
                if (i < 0) or (i >= vsize):
                    raise StandardError, ('side face list has invalid face index.' +
                                          str(i))



    # string representation
    def __str__(self):
        return 'Polygonal_cylinder_gen: ' + \
            str(len(m_center_vec)) + ' centers, ' + \
            str(m_n_gon) + '-gon, ' + \
            str(len(m_vertex_vec)) + ' vertices, ' + \
            str(len(m_segment_face_vec)) + ' seg tris, ' + \
            str(len(m_side_face_vec)) + ' side faces'
                               };

