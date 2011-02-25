#!/usr/bin/env python

"""Scene graph
\file
\brief Generic scene graph.
"""


import copy

import Camera
import Primitive
import ObjReader
import ConvReader2Primitive


# SceneGraph traverse strategy interfgace
class SceneGraphTraverseStrategyIF(object):
    """SceneGraph traverse strategy interfgace

    \see the example implementtaion SGTPrintStrategy
    """

    # constructor
    def __init__(self):
        """constructor"""
        pass

    # apply strategy to node before recurse
    def apply_before_recurse(self, _cur_node, _level):
        """apply strategy to node before recurse

        \param[in]  _cur_node current visting node
        \param[in]  _level    current depth
        """
        assert(false)           # you need to implement this in the inherited class

    # apply strategy while visiting __children
    def apply_middle(self, _cur_node, _level):
        """apply strategy while visiting __children

        \param[in]  _cur_node current visting node
        \param[in]  _level    current depth
        """
        assert(false)           # you need to implement this in the inherited class

    # apply strategy after visiting (when returning from the recurse)
    def apply_after_recurse(self, _cur_node, _level):
        """apply strategy after visiting (when returning from the recurse)

        \param[in]  _cur_node current visting node
        \param[in]  _level    current depth
        """
        assert(false)           # you need to implement this in the inherited class



# Example implementation of SceneGraphTraverseStrategyIF
class SGTPrintStrategy(SceneGraphTraverseStrategyIF):
    """Example implementation of SceneGraphTraverseStrategyIF

    Print out all the nodes in the scene graph
    """


    # constructor
    def __init__(self):
        """constructor"""
        pass

    # apply strategy to node before recurse. Implementation
    def apply_before_recurse(self, _cur_node, _level):
        """apply strategy to node before recurse. Implementation

        \param[in]  _cur_node current visting node
        \param[in]  _level    current depth
        """
        _cur_node.print_nodeinfo(_level)


    # apply strategy while visiting __children. Implementation
    def apply_middle(self, _cur_node, _level):
        """apply strategy while visiting __children. Implementation

        \param[in]  _cur_node current visting node
        \param[in]  _level    current depth
        """
        pass                    # not use in this class

    # apply strategy after visiting (when returning from the recurse). Implementation
    def apply_after_recurse(self, _cur_node, _level):
        """apply strategy after visiting (when returning from the
        recurse). Implementation

        \param[in]  _cur_node current visting node
        \param[in]  _level    current depth
        """
        pass                    # not use in this class



# Example implementation of SceneGraphTraverseStrategyIF
class SGTUpdateBBoxStrategy(SceneGraphTraverseStrategyIF):
    """Example implementation of SceneGraphTraverseStrategyIF

    pdate all the bounding box (not reset, if you need reset, use such
    strategy for that.)

    FIXME 2010-11-22(Mon)
    """
    # constructor
    def __init__(self):
        """constructor"""
        pass

    # apply strategy to node before recurse. Implementation
    def apply_before_recurse(self, _cur_node, _level):
        """apply strategy to node before recurse. Implementation

        add new __bbox if needed

        \param[in]  _cur_node current visting node
        \param[in]  _level    current depth
        """
        pass

    # apply strategy while visiting __children. Implementation
    def apply_middle(self, _cur_node, _level):
        """apply strategy while visiting __children. Implementation

        expand this level's bounding box

        \param[in]  _cur_node current visting node
        \param[in]  _level    current depth
        """
        pass


    # apply strategy after visiting
    def apply_after_recurse(self, _cur_node, _level):
        """apply strategy after visiting (when returning from the
        recurse). Implementation

        if this is not the root, expand the one level up's __bbox

        \param[in]  _cur_node current visting node
        \param[in]  _level    current depth
        """
        if _cur_node.is_primitive_node():
            # __primitive, get the __bbox from __primitive
            _cur_node.set_bbox(_cur_node.get_primitive().get_bbox())
        else:
            # This is a group node. The __children has already been
            # updated the __bbox. Now we found the __bbox that contains
            # all the __children __bbox.
            for chnode in _cur_node.get_children():
                _cur_node.get_bbox().insert_bbox(chnode.get_bbox())

# Scene graph
class SceneGraph(object):
    """Scene graph

    This has
    - __camera
    - __root_node
    """

    # default constructor
    def __init__(self):
        """default constructor"""
        self.__camera       = Camera.IFGICamera()
        self.__root_node    = None

    # set the root node
    def set_root_node(self, _root_node):
        """set the root node
        \param[in] _root_node root node
        """
        self.__root_node = _root_node

    # get the root node
    def get_root_node(self):
        """get the root node
        \return root node of this scenegraph
        """
        return self.__root_node

    # get __camera
    def get_camera(self):
        """get __camera
        \return __camera of this scenegraph
        """
        return self.__camera

    # travertse the scenegraph. subroutine of traverse_sgnode
    def __traverse_sgnode_sub(self, _cur_node, _level, _strategy):
        """travertse the scenegraph. subroutine of traverse_sgnode

        traverse scenegraph and apply _strategy to all nodes

        \param[in] _cur_node current visiting node
        \param[in] _level    current depth of the graph from the root
        """

        _strategy.apply_before_recurse(_cur_node, _level)
        if (not _cur_node.is_primitive_node()):
            # __children container
            for chnode in _cur_node.get_children():
                _strategy.apply_middle(chnode, _level)
                self.__traverse_sgnode_sub(chnode, _level + 1, _strategy)

        _strategy.apply_after_recurse(_cur_node, _level)


    # traverse the scenegraph
    def traverse_sgnode(self, _cur_node, _strategy):
        """traverse the scenegraph
        \param[in] _cur_node current node
        \param[in] _strategy strategy of the traverse
        """
        level = 0
        self.__traverse_sgnode_sub(_cur_node, level, _strategy)

    # for debug and example of usage of SceneGraphTraverseStrategyIF
    def print_all_obj(self):
        """print for debug and example of usage of
        SceneGraphTraverseStrategyIF
        """
        print '# SceneGraph'
        print '# SceneGraph::__camera'
        self.__camera.print_obj()
        if self.__root_node == None:
            print 'no __root_node'
            return
        print_strategy = SGTPrintStrategy()
        self.traverse_sgnode(self.__root_node, print_strategy)

    # update all bounding box recursively
    def update_all_bbox(self):
        """update all bounding box recursively.
        \see SGTUpdateBBoxStrategy
        """
        update_bbox_strategy = SGTUpdateBBoxStrategy()
        print 'NIN: update bounding box strategy'
        self.traverse_sgnode(self.__root_node, update_bbox_strategy)


# Scene Graph Node
class SceneGraphNode(object):
    """Scene Graph Node

    This has
      - __children
    or
      - __primitive
    This is exclusive.

    This node also has bounding box.
    If there is a __primitive, __primitive's __bbox, otherwise this __bbox.
    """

    # constructor
    def __init__(self, _nodename):
        """constructor
        \param[in] _nodename node name"""
        self.__children  = []
        self.__primitive = None
        self.__bbox      = Primitive.BBox()
        self.__nodename  = _nodename

    # set __nodename (shown in the SceneGraph viewer as Node)
    def set_nodename(self, _nodename):
        """set __nodename (shown in the SceneGraph viewer as Node)
        \param[in]: _nodename __nodename for scenegraph visualization"""

        self.__nodename = _nodename

    # get __nodename
    def get_nodename(self):
        """get __nodename
        \return: node (instance) name"""

        return self.__nodename

    # set __primitive
    def set_primitive(self, _prim):
        """set __primitive.  Node is either a __primitive node or a
        scenegraph node. Primitive node can not have __children.
        This condition is checked.

        \param[in] _prim __primitive"""
        if len(self.__children) > 0:
            raise StandardError, ('Can not set a __primitive. already had __children.')
        if self.__primitive != None:
            print 'Warning. This node has a __primitive.'
        self.__primitive = _prim

    # is this __primitive node?
    def is_primitive_node(self):
        """is this __primitive node?
        otherwise this should be a group node (has __children).
        \return True when this node is __primitive node."""

        if self.__primitive == None:
            return False
        return True

    # get __primitive
    def get_primitive(self):
        """get __primitive.
        raise exception when this is not a __primitive.
        \return __primitive when this is a __primitive node."""

        if (not self.is_primitive_node()):
            raise StandardError, ('this SceneGraphNode is not a __primitive node.')
        return self.__primitive

    # append child
    def append_child(self, _child):
        """append child
        \param[in] _child child node
        """
        if self.is_primitive_node():
            raise StandardError, ('Cannot append a child to a __primitive node.')
        self.__children.append(_child)

    # get child list
    def get_children(self):
        """get child list.
        \return list of children. may None"""
        return self.__children

    # get bounding box of this node
    def get_bbox(self):
        """get bounding box of this node
        \return bounding box
        """
        # check the consistency for debug
        if self.is_primitive_node():
            assert(self.__bbox.equal(self.__primitive.get_bbox()) == True)

        return self.__bbox

    # assign __bbox value
    def set_bbox(self, _bbox):
        """assign __bbox value.
        set the __bbox object. (_bbox is cloned before set.)
        \param _bbox bounding box to be assigned."""

        self.__bbox = copy.deepcopy(_bbox)


    # for debug
    #     def print_obj(self):
    #         pass

    # for debug
    def print_nodeinfo(self, _level):
        """print this object for debug.

        \param[in] _depth node depth"""

        indent = '  ' * _level
        if self.__primitive != None:
            print indent + '# SceneGraphNode:Primitive:' +\
                  self.__primitive.get_classname() +\
                  ' ' + str(self.__primitive.get_bbox())
        else:
            print indent + '# # __children = ' + str(len(self.__children))


# temporal: create trimesh scenegraph from obj filename for test
def create_one_trimeh_scenegraph(_objfname):
    """temporal: create trimesh scenegraph from obj filename for test

    SceneGraph +--+ ifgi __camera
               +--+ SceneGraphNode: __root_node
                                               +--+ TriMesh: __primitive

    TODO: create a scenegraph more general
    """

    # create a trimesh
    objreader = ObjReader.ObjReader()
    objreader.read(_objfname)
    tmesh = ConvReader2Primitive.conv_objreader_trimesh(objreader)
    if tmesh.is_valid() == False:
        raise StandardError, ('TriMesh is not valid.')

    # DELETEME print 'DEBUG:BBOX = ' + str(tmesh.get_bbox())

    # create scenegraph
    sg = SceneGraph()
    assert(sg.get_root_node() == None)

    # create scenegraph's root node
    rootsg = SceneGraphNode('rootsg')

    child0 = SceneGraphNode('meshgroup')
    rootsg.append_child(child0)
    child0.set_primitive(tmesh)

    sg.set_root_node(rootsg)

    return sg

# create empty scenegraph for new scene
def create_empty_scenegraph():
    """create empty scenegraph

    SceneGraph +--+ ifgi __camera
               +--+ SceneGraphNode: __root_node
    """

    # create scenegraph
    sg = SceneGraph()
    assert(sg.get_root_node() == None)

    # create scenegraph's root node
    rootsg = SceneGraphNode('rootsg')

    child0 = SceneGraphNode('group')
    rootsg.append_child(child0)

    sg.set_root_node(rootsg)

    return sg

#
# main test
#
# if __name__ == '__main__':
