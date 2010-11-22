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
    #  print out scenegraph nodes
    def print_sgnode_sub(self, _cur_node, _level):
        _cur_node.print_nodeinfo(_level)
        if _cur_node.primitive == None:
            # children container
            for chnode in _cur_node.children:
                chnode.print_nodeinfo(_level)
                self.print_sgnode_sub(chnode, _level + 1)


    # for debug
    #  print out scenegraph nodes
    def print_sgnode(self, _cur_node):
        level = 0
        self.print_sgnode_sub(_cur_node, level)


    # for debug
    def print_obj(self):
        print '# SceneGraph'
        print '# SceneGraph::camera'
        self.camera.print_obj()
        if self.root_node == None:
            print 'no root_node'
            return
        self.print_sgnode(self.root_node)



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
    #     def print_obj(self):
    #         pass

    # for debug
    #
    # \param[in] _depth node depth
    def print_nodeinfo(self, _level):
        indent = '  ' * _level
        if self.primitive != None:
            print indent + '# SceneGraphNode:Primitive:' + self.primitive.get_classname()
        else:
            print indent + '# # children = ' + str(len(self.children))


# temporal: create trimesh scenegraph from obj filename for test
#
# SceneGraph +--+ ifgi camera
#            +--+ SceneGraphNode: root_node
#                                           +--+ TriMesh: primitive
#
# TODO: create a scenegraph more general
def create_one_trimeh_scenegraph(_objfname):
    # create a trimesh
    objreader = ObjReader.ObjReader()
    objreader.read(_objfname)
    tmesh = ConvReader2Primitive.conv_objreader_trimesh(objreader)
    if tmesh.is_valid() == False:
        raise StandardError, ('TriMesh is not valid.')

    print 'DEBUG: BBOX = ' + str(tmesh.get_bbox())

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
