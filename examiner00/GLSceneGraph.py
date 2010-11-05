#!/usr/bin/env python
#
# GL scene graph
#

"""IFGI OpenGL SceneGraph"""

import Camera
import SceneGraph

from OpenGL import GL
from OpenGL import GLU


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
            print 'DEBUG: Create primitive and set'
            gl_prim_node = new_gl_scenegraph_primitive_node(_cur_sgnode.primitive)
            print 'DEBUG: Created: ' + gl_prim_node.get_classname()
            _cur_glnode.set_primitive(gl_prim_node)

        else:
            print 'DEBUG: Go to children'
            for ch_sgnode in _cur_sgnode.children:
                # create and refer the sg node
                ch_glnode = GLSceneGraphNode()
                _cur_sgnode.append_child(ch_glnode)
                self.copy_sgnode_sub(ch_sgnode, ch_glnode, _level + 1)


    # scenegraph draw
    # \param[in] HEREHERE
    def draw(self, _global_mode):
        self.gl_root_node.draw(_global_mode)


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
        print 'NIN: GLSceneGraph: print_obj()'

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
        self.is_debug  = False

    # get classname
    def get_classname(self):
        return 'GLSceneGraphNode'

    # set primitive
    def set_primitive(self, _prim):
        if len(self.children) > 0:
            raise StandardError, ('Can not set a primitive. already had children.')
        if self.primitive != None:
            print 'Warning. This node has a primitive.'
        self.primitive = _prim
        print 'DEBUG: set_primitive: ' + self.primitive.get_classname()


    # append child
    def append_child(self, _child):
        if self.primitive != None:
            raise StandardError, ('Can not append a child. already had a primitive.')
        self.children.append(_child)

    # print glnode info
    def print_glnodeinfo(self, _level):
        indent = '  ' * _level
        if self.primitive != None:
            print indent + '# ' + self.get_classname() + ':Primitive'
        else:
            print indent + '# # children = ' + str(len(self.children))


    # draw by mode
    def draw(self, _global_mode):
        print self.get_classname() + '::draw is called with ' + str(_global_mode)

        if self.primitive != None:
            # primitive: draw itself
            self.primitive.draw(_global_mode)
            print self.get_classname() + '::draw: call primitive draw'
        elif len(self.children) > 0:
            # no primitive: draw children
            for ch_glnode in self.children:
                # create and refer the sg node
                ch_glnode.draw(_global_mode)
                print self.get_classname() + '::draw: call child draw'
        else:
            self.debug_out('Node has no primitive, no children')
            print self.get_classname() + '::draw: neither'


    # for debug
    def print_obj(self):
        pass

    # set debug mode
    # \param[in] _is_debug when true some debug message will show up.
    def set_debug_mode(self, _is_debug):
        self.is_debug = _is_debug

    # is debug mode?
    # \return true when debug mode is on
    def is_debug_mode(self):
        return self.is_debug

    # debug output
    # \param[in] _dbgmes debug message. when debug mode is on, this is visible.
    def debug_out(self, _dbgmes):
        if self.is_debug == True:
            print _dbgmes



# OpenGL TriMeshNode
class GLTriMeshNode(GLSceneGraphNode):
    # default constructor
    def __init__(self):
        # call base class constructor to fill the members
        super(GLTriMeshNode, self).__init__()
        self.local_draw_mode = 0

    # get classname
    def get_classname(self):
        return 'GLTriMeshNode'

    # draw
    def draw(self, _global_mode):
        print 'DEBUG: primitive is ' + self.primitive.get_classname()
        self.draw_flat_shading()


    # each draw: flat shading
    def draw_flat_shading(self):
        GL.glShadeModel(GL.GL_FLAT)
        GL.glBegin(GL.GL_TRIANGLES)
        # vp reference
        vp = self.primitive.vertex_list
        for face in self.primitive.face_idx_list:
            GL.glVertex3d(vp[face[0]][0], vp[face[0]][1], vp[face[0]][2])
            GL.glVertex3d(vp[face[1]][0], vp[face[1]][1], vp[face[1]][2])
            GL.glVertex3d(vp[face[2]][0], vp[face[2]][1], vp[face[2]][2])
        GL.glEnd()


# OpenGL scenegraph node factory
#
def new_gl_scenegraph_primitive_node(_primitive):
    if _primitive == None:
        raise StandardError, ('Null primitive.')

    if _primitive.get_classname() == 'TriMesh':
        print 'DEBUG: created Trimesh Primitive'
        tmeshnode = GLTriMeshNode()
        tmeshnode.set_primitive(_primitive)
        return tmeshnode
    else:
        print 'unsupported primitive: ' + _primitive.get_classname()
        return None


#
# main test
#
# if __name__ == '__main__':
