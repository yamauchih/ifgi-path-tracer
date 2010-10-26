#!/usr/bin/env python
#
# scene graph
#

"""IFGI Generic SceneGraph"""

# import math
import Camera
import Primitive
import ObjReader
import ConvReader2Primitive


#
# scene graph
#
# This has
#   - camera
#   - root_node
#
class SceneGraph(object):
    # default constructor
    def __init__(self):
        self.camera       = Camera.IFGICamera()
        self.root_node    = None

    # for debug
    def print_obj(self):
        pass


#
# scene graph node
#
# This has
#   - children
#   or
#   - primitive
# This is exclusive.
#
class SceneGraphNode(object):
    # default constructor
    def __init__(self):
        self.children  = []
        self.primitive = None

    # set primitive
    def set_primitive(self, _prim):
        if len(self.children) > 0:
            raise StandardError, ('Can not set a primitive. already had children.')
        if self.primitive != None:
            print 'Warning. This node has a primitive.'
        self.primitive = _prim

    # append child
    def append_child(self, _child):
        if self.primitive != None:
            raise StandardError, ('Can not append a child. already had a primitive.')
        self.children.append(_child)

    # for debug
    def print_obj(self):
        pass



# temporal: create trimesh scenegraph from obj filename for test
#
# TODO: create a scenegraph more general
def create_one_trimeh_scenegraph(_objfname):
    # create a trimesh
    objreader = ObjReader.ObjReader()
    objreader.read(_objfname)
    tmesh = ConvReader2Primitive.conv_objreader_trimesh(objreader)
    if tmesh.is_valid() == False:
        raise StandardError, ('TriMesh is not valid.')

    # create scenegraph
    sg = SceneGraph()
    assert(sg.root_node == None)

    # create scenegraph's root node
    rootsg = SceneGraphNode()
    rootsg.set_primitive(tmesh)

    sg.root_node = rootsg

    return sg

#
# main test
#
# if __name__ == '__main__':
