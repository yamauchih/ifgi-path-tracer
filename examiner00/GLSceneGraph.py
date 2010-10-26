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
        self.gl_camera    = GLCamera()
        self.gl_root_node = None
        self.scenegraph   = None

    # set generic scene graph
    def set_scenegraph(self, _sg):
        self.scenegraph = _sg
        
        # check self.scenegraph validity

        # create GLSceneGraph from scenegraph

        


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
        if len(self.primitive != None:
            print 'Warning. This node has a primitive.')
        self.primitive = _prim

    # append child
    def append_child(self, _child):
        if self.primitive != None:
            raise StandardError, ('Can not append a child. already had a primitive.')
        self.children.append(_child)

    # for debug
    def print_obj(self):
        pass


#
# main test
#
# if __name__ == '__main__':
