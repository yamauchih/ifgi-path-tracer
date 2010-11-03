#!/usr/bin/env python
#
# GL scene graph
#

"""IFGI OpenGL SceneGraph"""

import Camera
import SceneGraph

#
# OpenGL scene graph
#
# This has
#   - GLCamera
#   - GLroot_node
#
class GLSceneGraph(object):
    # default constructor
    def __init__(self):
        self.gl_camera    = Camera.GLCamera()
        self.gl_root_node = None
        self.scenegraph   = None

    # set generic scene graph
    def set_scenegraph(self, _sg):
        self.scenegraph   = _sg

        self.gl_root_node = GLSceneGraphNode()
        

        # check self.scenegraph validity

        # create GLSceneGraph from scenegraph
        self.copy_sgnode_sub(self.scenegraph.root_node,
                             self.gl_root_node,
                             0)

        self.print_sgnode_sub(self.gl_root_node, 0)


    # copy scenegraph tree sub
    def copy_sgnode_sub(self, _cur_sgnode, _cur_glnode, _level):
        if _cur_sgnode.primitive != None:
            # create primitive node and set the primitive
            glsgnode = new_gl_scenegraph_primitive_node(_cur_sgnode.primitive)
            glsgnode.set_primitive(_cur_sgnode.primitive)

        else:
            for ch_sgnode in _cur_sgnode.children:
                # create and refer the sg node
                ch_glnode = GLSceneGraphNode()
                _cur_sgnode.append_child(ch_glnode)
                self.copy_sgnode_sub(ch_sgnode, ch_glnode, _level + 1)


    # for debug
    #  print out scenegraph nodes
    def print_sgnode_sub(self, cur_glnode, _level):
        cur_glnode.print_glnodeinfo(_level)
        if cur_glnode.primitive == None:
            # children container
            for chnode in cur_glnode.children:
                self.print_sgnode_sub(chnode, _level + 1)





    # for debug
    def print_obj(self):
        pass

#
# OpenGL scene graph node
#
# This has
#   - children
#   or
#   - primitive
# This is exclusive.
#
class GLSceneGraphNode(object):
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

    # print glnode info
    def print_glnodeinfo(self, _level):
        indent = '  ' * _level
        if self.primitive != None:
            print indent + '# GLSceneGraphNode:Primitive'
        else:
            print indent + '# # children = ' + str(len(self.children))




    # draw by mode
    def draw(self, _mode):
        pass



    # for debug
    def print_obj(self):
        pass

# OpenGL TriMeshNode
class GLTriMeshNode(GLSceneGraphNode):
    pass


# OpenGL scenegraph node factory
# 
def new_gl_scenegraph_primitive_node(_primitive):
    if _primitive == None:
        raise StandardError, ('Null primitive.')

    if _primitive.get_classname() == 'TriMesh':
        return GLTriMeshNode()
    else:
        print 'unsupported primitive: ' + _primitive.get_classname() 
        return None


#
# main test
#
# if __name__ == '__main__':
