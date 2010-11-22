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
# SceneGraph traverse strategy interfgace
#
# See the example implementtaion SGTPrintStrategy
#
class SceneGraphTraverseStrategyIF(object):
    # constructor
    def __init__(self):
        pass

    # apply strategy to node before recurse
    #
    # \param[in]  _cur_node current visting node
    # \param[in]  _level    current depth
    #
    def apply_before_recurse(self, _cur_node, _level):
        assert(false)           # you need to implement this in the inherited class

    # apply strategy while visiting children
    #
    # \param[in]  _cur_node current visting node
    # \param[in]  _level    current depth
    #
    def apply_middle(self, _cur_node, _level):
        assert(false)           # you need to implement this in the inherited class

    # apply strategy after visiting (when returning from the recurse)
    #
    # \param[in]  _cur_node current visting node
    # \param[in]  _level    current depth
    #
    def apply_after_recurse(self, _cur_node, _level):
        assert(false)           # you need to implement this in the inherited class



#
# Example implementation of SceneGraphTraverseStrategyIF
#
# Print out all the nodes in the scene graph
#
class SGTPrintStrategy(SceneGraphTraverseStrategyIF):
    # constructor
    def __init__(self):
        pass

    # apply strategy to node before recurse. Implementation
    #
    # \param[in]  _cur_node current visting node
    # \param[in]  _level    current depth
    #
    def apply_before_recurse(self, _cur_node, _level):
        _cur_node.print_nodeinfo(_level)


    # apply strategy while visiting children. Implementation
    #
    # \param[in]  _cur_node current visting node
    # \param[in]  _level    current depth
    #
    def apply_middle(self, _cur_node, _level):
        pass                    # not use in this class

    # apply strategy after visiting (when returning from the recurse). Implementation
    #
    # \param[in]  _cur_node current visting node
    # \param[in]  _level    current depth
    #
    def apply_after_recurse(self, _cur_node, _level):
        pass                    # not use in this class



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

    # travertse the scenegraph. subroutine of traverse_sgnode
    #
    #  traverse scenegraph and apply _strategy to all nodes
    #
    # \param[in] _cur_node current visiting node
    # \param[in] _level    current depth of the graph from the root
    def traverse_sgnode_sub(self, _cur_node, _level, _strategy):
        _strategy.apply_before_recurse(_cur_node, _level)
        if _cur_node.primitive == None:
            # children container
            for chnode in _cur_node.children:
                _strategy.apply_middle(chnode, _level)
                self.traverse_sgnode_sub(chnode, _level + 1, _strategy)

        _strategy.apply_after_recurse(_cur_node, _level)


    # traverse the scenegraph
    #
    def traverse_sgnode(self, _cur_node, _strategy):
        level = 0
        self.traverse_sgnode_sub(_cur_node, level, _strategy)

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


    # # for debug
    def print_obj_bak(self):
        print '# SceneGraph'
        print '# SceneGraph::camera'
        self.camera.print_obj()
        if self.root_node == None:
            print 'no root_node'
            return
        self.print_sgnode(self.root_node)

    # for debug and example of usage of SceneGraphTraverseStrategyIF
    def print_obj(self):
        print '# SceneGraph'
        print '# SceneGraph::camera'
        self.camera.print_obj()
        if self.root_node == None:
            print 'no root_node'
            return
        print_strategy = SGTPrintStrategy()
        self.traverse_sgnode(self.root_node, print_strategy)





#
# Scene Graph Node
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

    print 'DEBUG:BBOX = ' + str(tmesh.get_bbox())

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
