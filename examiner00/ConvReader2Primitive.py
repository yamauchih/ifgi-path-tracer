#!/usr/bin/env python
#
# reader to primitive converter
#

"""IFGI Reader to Primitive Converter"""

import Primitive
import ObjReader

#
# ObjReader to TriMesh converter
#
def conv_objreader_trimesh(_objreader):
    tmesh = Primitive.TriMesh()
    tmesh.set_data(_objreader.vertex_list,
                   _objreader.face_idx_list,
                   _objreader.texcoord_list,
                   _objreader.texcoord_idx_list,
                   _objreader.normal_list,
                   _objreader.normal_idx_list
                   )
    return tmesh


#
# main test ... test_ObjReader
#
# if __name__ == '__main__':
#     objreader = ObjReader()
#     objreader.read('../sampledata/one_tri.obj')
#
