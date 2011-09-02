#!/usr/bin/env python
#
# Copyright 2011 (C) Yamauchi, Hitoshi
#

"""Scene graph
\file
\brief Generic scene graph.
"""

import copy, numpy

import Camera, Primitive, ObjReader, ConvReader2Primitive, Material
from ifgi.base.ILog import ILog


# SceneGraphTraverseStrategyIF ----------------------------------------

class SceneGraphTraverseStrategyIF(object):
    """SceneGraph traverse strategy interfgace

    \see the example implementtaion SGTPrintStrategy
    """

    def __init__(self):
        """constructor"""
        pass


    def apply_before_recurse(self, _cur_node, _level):
        """apply strategy to node before recurse

        \param[in]  _cur_node current visting node
        \param[in]  _level    current depth
        """
        assert(false)           # you need to implement this in the inherited class


    def apply_middle(self, _cur_node, _level):
        """apply strategy while visiting __children

        \param[in]  _cur_node current visting node
        \param[in]  _level    current depth
        """
        assert(false)           # you need to implement this in the inherited class


    def apply_after_recurse(self, _cur_node, _level):
        """apply strategy after visiting (when returning from the recurse)

        \param[in]  _cur_node current visting node
        \param[in]  _level    current depth
        """
        assert(false)           # you need to implement this in the inherited class



# SGTPrintStrategy ----------------------------------------

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



# SGTUpdateBBoxStrategy ----------------------------------------

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

        if not _cur_node.has_node_bbox():
            # I don't have bbox, therefore, I don't need to compute it
            return

        if _cur_node.is_primitive_node():
            # I am a primitive node, I have own bbox.
            # Note: I have own bbox means if primitive has
            # children, and it has bbox, they doesn't affect mine,
            # since I am a primitive.
            return

        # re-compute bbox, initialize it as invalid.
        _cur_node.get_bbox().invalidate()

        # Ask all the children about bbox. The children have already
        # been updated own bbox. Now we found the current bbox that
        # contains all the children's bbox.
        # In case no childen have bbox, _cur_node.bbox stays invalid
        for chnode in _cur_node.get_children():
            if chnode.has_node_bbox():
                if chnode.get_bbox().has_volume():
                    # update my bbox
                    _cur_node.get_bbox().insert_bbox(chnode.get_bbox())


# ----------------------------------------------------------------------

class SceneGraph(object):
    """Scene graph

    This has
    - __cur_camera   current camera
    - __root_node    for all the geometry
    """

    # default constructor
    def __init__(self):
        """default constructor"""
        self.__cur_camera  = None
        self.__root_node   = None

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

    # set current camera
    def set_current_camera(self, _cur_camera):
        """set current camera.
        \param[in] current active camera.
        """
        self.__cur_camera = _cur_camera

    # get current camera
    def get_current_camera(self):
        """get current camera.
        \return current active camera of this scenegraph
        """
        return self.__cur_camera


    # is valid scenegraph
    def is_valid(self):
        """test this scenegrapgh validity
        \return true when the scenegraph is valid."""
        if(self.get_root_node() == None):
            print 'Scenegraph: No rootnode'
            return False

        if(self.get_current_camera() == None):
            print 'Scenegraph: No camera'
            return False

        return True

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


    def traverse_sgnode(self, _cur_node, _strategy):
        """traverse the scenegraph
        \param[in] _cur_node current node
        \param[in] _strategy strategy of the traverse
        """
        level = 0
        self.__traverse_sgnode_sub(_cur_node, level, _strategy)


    def print_all_node(self):
        """print all nodes for debug and example of usage of
        SceneGraphTraverseStrategyIF
        """
        if self.__root_node == None:
            print 'no __root_node'
            return
        print_strategy = SGTPrintStrategy()
        self.traverse_sgnode(self.__root_node, print_strategy)


    def update_all_bbox(self):
        """update all bounding box recursively.
        \see SGTUpdateBBoxStrategy
        """
        # recompute root bbox
        self.__root_node.get_bbox().invalidate()

        update_bbox_strategy = SGTUpdateBBoxStrategy()
        self.traverse_sgnode(self.__root_node, update_bbox_strategy)
        # handle no children have valid bbox (e.g., empty scene)
        if not self.__root_node.get_bbox().has_volume():
            ILog.warn('Rootnode has no volume, set [0 0 0]-[1 1 1]')
            self.__root_node.get_bbox().insert_point(numpy.array([0,0,0]))
            self.__root_node.get_bbox().insert_point(numpy.array([1,1,1]))



# ----------------------------------------------------------------------

class SceneGraphNode(object):
    """Scene Graph Node. This is a base node of any scenegraph node.

    The main function of this node is a group node.

    This has children, but no primitive. (A primitive means a visible
    real objetct such as TriMesh, except bounding box.)

    This node has a bounding box.
    """

    def __init__(self, _nodename):
        """constructor
        \param[in] _nodename node name"""
        self.__children  = []
        self.__bbox      = Primitive.BBox()
        self.__nodename  = _nodename


    def get_classname(self):
        """get classname
        \return: scnegraph node class name"""

        return 'SceneGraphNode'


    def append_child(self, _child):
        """append child
        \param[in] _child child node
        """
        if self.is_primitive_node():
            raise StandardError, ('Cannot append a child to a PrimitiveNode.')
        self.__children.append(_child)


    def has_children(self):
        """has children.
        \return True when this node has any child
        """
        return not (self.__children == [])


    def children_count(self):
        """get number of children
        \return the number of children
        """
        return len(self.__children)


    def get_children(self):
        """get child list.
        \return list of children. may None"""
        return self.__children


    def set_nodename(self, _nodename):
        """set __nodename (shown in the SceneGraph viewer as Node)
        \param[in]: _nodename __nodename for scenegraph visualization"""

        self.__nodename = _nodename


    def get_nodename(self):
        """get __nodename
        \return: node (instance) name"""

        return self.__nodename


    def is_primitive_node(self):
        """is this a __primitive node?
        \return True when this node is __primitive node.
        """
        return False


    def set_primitive(self, _prim):
        """set primitive.

        This is an interface and need to be implemented if the node is
        primitive node.

        \param[in] _prim primitive"""
        raise StandardError, ('Primitive node Implementation is needed.')


    def get_primitive(self):
        """get primitive.

        This is an interface and need to be implemented if the node is
        primitive node.
        \return primitive, raise exception when this is not a primitive node."""

        raise StandardError, ('Primitive node implementation is needed.')


    def get_bbox(self):
        """get bounding box of this node
        \return bounding box
        """
        return self.__bbox


    def has_node_bbox(self):
        """Does this node have a bounding box?
        Default is True.

        \return True when the node can have a bounding box. Eg.,
        camera does not have own bbox.
        """
        return True


    def set_bbox(self, _bbox):
        """assign __bbox value.
        set the __bbox object. (_bbox is cloned before set.)
        \param _bbox bounding box to be assigned."""

        self.__bbox = copy.deepcopy(_bbox)


    def print_nodeinfo(self, _level):
        """print this object for debug.

        \param[in] _depth node depth"""

        indent = '  ' * _level
        out_str = indent + '+ ' + self.get_classname() + ':' + self.get_nodename() + ', '
        if self.has_node_bbox():
            out_str += 'Bbox: '
            if self.get_bbox().has_volume():
                out_str += str(self.get_bbox()) + ', '
            else:
                out_str += 'invalid volume, '
        else:
            out_str += 'no bbox, '

        out_str += str(len(self.get_children())) + ' children '
        print out_str


# ----------------------------------------------------------------------

class PrimitiveNode(SceneGraphNode):
    """Primitive node, a Scene Graph Node.

    This has a primitive also this can have children.

    This has reference to the material.

    This node also has bounding box.
    """

    def __init__(self, _nodename, _prim):
        """constructor
        \param[in] _nodename node name"""
        super(PrimitiveNode, self).__init__(_nodename)

        self.__primitive = _prim


    def get_classname(self):
        """get classname
        \return: scnegraph node class name"""

        return 'SceneGraphNode'


    # def set_nodename(self, _nodename):
    #     """set __nodename (shown in the SceneGraph viewer as Node)
    #     \param[in]: _nodename __nodename for scenegraph visualization"""

    #     self.__nodename = _nodename


    # def get_nodename(self):
    #     """get __nodename
    #     \return: node (instance) name"""

    #     return self.__nodename

    # Use SceneGraphNode's method
    # def append_child(self, _child):
    #     """append child
    #     \param[in] _child child node
    #     """
    #     if self.is_primitive_node():
    #         raise StandardError, ('Cannot append a child to a __primitive node.')
    #     self.__children.append(_child)

    # get child list
    # def get_children(self):
    #     """get child list.
    #     \return list of children. may None"""
    #     return self.__children


    # ------------------------------------------------------------
    # primitive node interface
    # ------------------------------------------------------------

    def is_primitive_node(self):
        """is this a primitive node?
        \return True when this node is primitive node.
        """
        # This node must have a primitive in run time
        assert(self.__primitive != None)
        return True


    def set_primitive(self, _prim):
        """set a primitive.

        Reimplemented in PrimitiveNode.

        \param[in] _prim a primitive"""
        if self.has_children():
            raise StandardError, ('Can not set a primitive. already had children.')
        if self.__primitive != None:
            print 'Warning. This node has a primitive. Override the primitive.'
        self.__primitive = _prim


    def get_primitive(self):
        """get the primitive.

        Reimplemented in PrimitiveNode.

        \return a assigned primitive.
        """
        return self.__primitive


    # ----------------------------------------------------------------------

    def has_node_bbox(self):
        """Does this node have a bounding box?
        Default is True.

        \return True when the node can have a bounding box. Eg.,
        camera does not have own bbox.
        """
        return True


    def get_bbox(self):
        """get bounding box of this node
        \return bounding box
        """
        if self.__primitive == None:
            raise StandardError, ('No primitive set [' + self.get_classname() +\
                                      ' ' + self.get_nodename() + ']')
        return self.__primitive.get_bbox()


    def set_bbox(self, _bbox):
        """assign bbox value.
        set the bbox object. (_bbox is cloned before set.)
        \param _bbox bounding box to be assigned."""

        self.__primitive.set_bbox(_bbox)


    def print_nodeinfo(self, _level):
        """print this object for debug.

        \param[in] _depth node depth"""

        indent = '  ' * _level
        print indent + '+ SceneGraphNode:Primitive:' +\
            self.__primitive.get_classname() +\
            ' ' + str(self.__primitive.get_bbox())

# ----------------------------------------------------------------------

class MaterialNode(SceneGraphNode):
    """Material node, a Scene Graph Node.

    Material node for ifgi is attached under the material group under
    the scenegraph root.
    """

    def __init__(self, _nodename):
        """constructor
        \param[in] _nodename node name"""
        super(MaterialNode, self).__init__(_nodename)
        self.__material = None


    def get_classname(self):
        """get classname
        \return: scnegraph node class name"""

        return 'MaterialNode'


    def is_primitive_node(self):
        """is this a __primitive node?
        \return False. material can not visualize without primitive.
        """
        return False


    def get_bbox(self):
        """get bounding box of this node
        \return None. material has no bounding box
        """
        return None


    def has_node_bbox(self):
        """Does this node have a bounding box?
        \return False, material has no bounding box
        """
        return False


    def set_material(self, _mat):
        """set a material.

        \param[in] _mat a material"""
        if self.has_children():
            raise StandardError, ('Can not set a primitive. already had children.')
        if self.__material != None:
            print 'Warning. override the existing matrial.'
        self.__material = _mat


    def get_material(self):
        """get the material.
        \return a assigned material.
        """
        return self.__material

# ----------------------------------------------------------------------

class CameraNode(SceneGraphNode):
    """A camera node.
    """

    def __init__(self, _nodename):
        """constructor.
        \param[in] _nodename node name.
        """
        super(CameraNode, self).__init__(_nodename)
        self.__ifgi_camera = Camera.IFGICamera()


    def get_classname(self):
        """get classname
        \return: scnegraph node class name"""

        return 'CameraNode'


    def is_primitive_node(self):
        """is this primitive node?
        camera is not a drawable primitive.
        \return False"""

        return False

    def has_node_bbox(self):
        """Does this node have a bounding box?

        \return False. camera does not have own bbox.
        """
        return False


    def get_camera(self):
        """get the camera."""
        return self.__ifgi_camera


# ----------------------------------------------------------------------

class ImageFilmNode(SceneGraphNode):
    """image film (framebuffer) node.
    """

    def __init__(self, _nodename):
        """constructor.
        \param[in] _nodename node name.
        """
        super(ImageFilmNode, self).__init__(_nodename)
        self.__imagefilm = Film.ImageFilm()


    def get_classname(self):
        """get classname
        \return: scnegraph node class name"""

        return 'ImageFilmNode'


    def is_primitive_node(self):
        """is this primitive node?
        image film is not a drawable primitive.
        \return False"""

        return False


    def has_node_bbox(self):
        """Does this node have a bounding box?

        \return False. camera does not have own bbox.
        """
        return False


    def get_imagefilm(self):
        """get the image film."""
        return self.__imagefilm


# ----------------------------------------------------------------------

def load_one_trimesh_from_objfile(_objfname):
    """load a trimesh from an obj file.
    \param[in] _objfname obj filename
    \return a Trimesh
    """

    objreader = ObjReader.ObjReader()
    objreader.read(_objfname)
    tmesh = ConvReader2Primitive.conv_objreader_trimesh(objreader)
    if tmesh.is_valid() == False:
        raise StandardError, ('TriMesh [' + _objfname + '] is not valid.')

    return tmesh


# temporal: create trimesh scenegraph from obj filename for test
def create_one_trimeh_scenegraph(_objfname):
    """temporal: create trimesh scenegraph from obj filename for test

    SceneGraph +
               +--+ SceneGraphNode: 'rootsg' __root_node
                                 +--+ CameraNode: 'main_cam' __camera
                                 +--+ SceneGraphNode: 'materialgroup'
                                                   +--+ Material: 'mat'
                                 +--+ SceneGraphNode: 'meshgroup'
                                                   +--+ TriMesh: 'trimesh'

    TODO: create a scenegraph more general
    """

    # create a trimesh
    tmesh = load_one_trimesh_from_objfile(_objfname)
    assert(tmesh.is_valid() == True)

    # create scenegraph
    sg = SceneGraph()
    assert(sg.get_root_node() == None)

    # create scenegraph's root node
    rootsg = SceneGraphNode('rootsg')
    child0 = CameraNode('main_cam')
    rootsg.append_child(child0)

    # 'materialgroup' is a special group.
    child1 = SceneGraphNode('materialgroup')
    rootsg.append_child(child1)
    child1_0 = MaterialNode('mat_trimesh')
    child1_0.set_material(Material.Material())
    child1.append_child(child1_0)

    child2 = SceneGraphNode('meshgroup')
    rootsg.append_child(child2)
    child2_0 = PrimitiveNode('trimesh', tmesh)
    child2.append_child(child2_0)

    sg.set_root_node(rootsg)
    sg.set_current_camera(child0.get_camera())

    assert(sg.is_valid())

    return sg

# ----------------------------------------------------------------------

def create_empty_scenegraph():
    """create empty scenegraph

    SceneGraph +
               +--+ SceneGraphNode: __root_node 'root_sg'
                                 +--+ CameraNode: 'main_cam'
                                 +--+ SceneGraphNode: 'group'
    """

    # create scenegraph
    sg = SceneGraph()
    assert(sg.get_root_node() == None)

    # create scenegraph's root node
    rootsg = SceneGraphNode('rootsg')

    child0 = CameraNode('main_cam')
    rootsg.append_child(child0)

    # child1 = SceneGraphNode('group')
    # rootsg.append_child(child1)

    sg.set_root_node(rootsg)
    sg.set_current_camera(child0.get_camera())

    assert(sg.is_valid())

    return sg

#
# main test
#
# if __name__ == '__main__':
