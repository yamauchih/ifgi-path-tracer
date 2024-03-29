#!/usr/bin/env python
#
# Copyright 2011 (C) Yamauchi, Hitoshi
#

"""reader to primitive converter
\file
\brief file reader, then convert the read result to a primitive
"""

import Primitive, ObjReader

def conv_objreader_trimesh(_objreader, _mesh_name, _material_name):
    """ObjReader to TriMesh converter.
    \param[in] _objreader obj file reader
    \param[in] _mesh_name mesh name
    \param[in] _material_name mesh's material name
    """
    assert(_mesh_name     != None)
    assert(_material_name != None)

    tmesh = Primitive.TriMesh(_mesh_name, _material_name)
    tmesh.set_data(_objreader.vertex_list,
                   _objreader.face_idx_list,
                   _objreader.texcoord_list,
                   _objreader.texcoord_idx_list,
                   _objreader.normal_list,
                   _objreader.normal_idx_list
                   )
    return tmesh


#
# main test ... test_
#
# if __name__ == '__main__':
#     pass
#
