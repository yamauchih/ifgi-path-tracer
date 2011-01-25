#!/usr/bin/env python

##
# \file
# \brief OpenGL scene graph module


"""IFGI OpenGL SceneGraph"""

from OpenGL import GL
from OpenGL import GLU

import Camera
import DrawMode
import SceneGraph
import GLUtil

## OpenGL scene graph
#
# This has
#   - GLCamera
#   - GLroot_node
#
class GLSceneGraph(SceneGraph.SceneGraph):
    ## default constructor
    def __init__(self):
        self.gl_camera    = Camera.GLCamera()
        self.gl_root_node = None
        self.scenegraph   = None

    ## set generic scene graph.
    #
    # Generic scenegraph is for both OpenGL render and Path tracing
    # render.
    #
    # \param[in] _sg generic scenegraph
    def set_scenegraph(self, _sg):
        self.scenegraph   = _sg

        self.gl_root_node = GLSceneGraphNode()

        # check self.scenegraph validity

        # create GLSceneGraph from scenegraph
        self.copy_sgnode_sub(self.scenegraph.root_node,
                             self.gl_root_node,
                             0)

        self.print_sgnode_sub(self.gl_root_node, 0)
        

    ## copy scenegraph tree subroutine
    #
    # \param[in] _cur_sgnode current visiting (generic) scenegraph node
    # \param[in] _cur_glnode current visiting OpenGL scenegraph node
    # \param[in] _level      current depth level
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


    ## scenegraph draw
    #
    # \param[in] _global_mode global draw mode
    def draw(self, _global_mode):
        self.gl_root_node.draw(_global_mode)


    ## print out scenegraph nodes for debug (subroutine of print_sgnode)
    #
    # \param[in] _cur_glnode currect visiting gl node
    # \param[in] _level      current visiting depth
    def print_sgnode_sub(self, _cur_glnode, _level):
        _cur_glnode.print_glnodeinfo(_level)
        if _cur_glnode.primitive == None:
            # children container
            for chnode in _cur_glnode.children:
                self.print_sgnode_sub(chnode, _level + 1)

    ## print object for debug
    def print_obj(self):
        print 'NIN: GLSceneGraph: print_obj()'

    ## collect all drawmode
    #
    # traverse with SceneGraphTraverseStrategyIF strategy
    #
    # \see SceneGraphTraverseStrategyIF
    def collect_drawmode(self):
        collect_drawmode_strategy = GLSGTCollectDrawmodeStrategy()
        self.traverse_sgnode(self.gl_root_node, collect_drawmode_strategy)
        # print 'DEBUG: collect draw mode done.'
        # collect_drawmode_strategy.drawmodelist.print_obj()
        return collect_drawmode_strategy.drawmodelist


## OpenGL scene graph node (BaseNode/GroupNode)
#
# This has either
#   - children
#   - primitive
# These are exclusive.
#
class GLSceneGraphNode(SceneGraph.SceneGraphNode):
    ## default constructor
    def __init__(self):
        self.children  = []
        self.primitive = None
        self.is_debug  = False
        self.nodename  = 'NoName'
        self.is_active = True
        self.is_global_drawmode = True

    ## set nodename (shown in the SceneGraph viewer as Node)
    #
    # \param[in] _nodename nodename for scenegraph visualization
    def set_nodename(self, _nodename):
        self.nodename = _nodename

    ## get nodename
    #
    # \return node (instance) name
    def get_nodename(self):
        return self.nodename

    ## get classname (shown in the SceneGraph viewer as node Type)
    #
    # \return class name 
    def get_classname(self):
        return 'GLSceneGraphNode'

    ## set node active (shown in the SceneGraph viewer as Status)
    #
    # \param[in] _is_active when True, node status is active,
    # otherwise deactivated
    def set_node_active(self, _is_active):
        self.is_active = _is_active

    ## set node active (shown in the SceneGraph viewer as Status)
    #
    # \return True if this node is active 
    def is_node_active(self):
        return self.is_active

    ## get node active state string
    #
    # \return get node active state string
    def get_active_state(self):
        if self.is_node_active():
            return 'Active'
        else:
            return 'Deactivated'

    ## set node global drawmode (shown in the SceneGraph viewer as Mode)
    #
    # \param[in] _is_global when True, node drawmode is global,
    # otherwise local.
    def set_global_drawmode(self, _is_global):
        self.is_global_drawmode = _is_global

    ## is node global drawmode (shown in the SceneGraph viewer as Mode)
    #
    # \return when True, node drawmode is global
    def is_global_drawmode(self):
        return self.is_global_drawmode

    ## get draw mode string
    #
    # \return draw mode string
    def get_global_drawmode_str(self):
        if self.is_global_drawmode():
            return 'Global drawmode'
        else:
            # NIN: use local draw mode combination
            return 'Local drawmode'


    # set primitive
    def set_primitive(self, _prim):
        if len(self.children) > 0:
            raise StandardError, ('Can not set a primitive. already had children.')
        # can not use is_primitive_node, this method changes the
        # primitive state
        if self.primitive != None:
            print 'Warning. This node has a primitive.'
        self.primitive = _prim
        print 'DEBUG: set_primitive: ' + self.primitive.get_classname()

    ## is this node a primitive node?
    #
    # (primitive node == no children, just a primitive)
    #
    # \return True if this node is a primitive node
    def is_primitive_node(self):
        if self.primitive != None:
            return True

        return False

    ## append child
    #
    # \param[in] _child a child will be appended to this node
    def append_child(self, _child):
        if (self.is_primitive_node()):
            raise StandardError, ('Can not append a child. already had a primitive.')
        self.children.append(_child)

    ## print glnode info. Indentation is according to the depth level
    #
    # \param _level node depth level
    def print_glnodeinfo(self, _level):
        indent = '  ' * _level
        if (self.is_primitive_node()):
            print indent + '# ' + self.get_classname() + ':Primitive'

        print indent + '# # children = ' + str(len(self.children))


    ## draw by mode
    #
    # \param[in] _global_mode global draw mode
    # \see DrawMode
    def draw(self, _global_mode):
        print self.get_classname() + '::draw is called with ' + str(_global_mode)

        if (self.is_primitive_node()):
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

    ## get draw mode of this GLSceneGraphNode
    #
    # \return return drawmode, maybe None
    def get_drawmode(self):
        if (self.is_primitive_node()):
            return self.primitive.get_drawmode()

        return None
        # raise StandardError, ('GLSceneGraphNode.get_drawmode() must be implemented ' +
        # 'in derived class. classname = ' + self.get_classname())

    ## print this obj for debug
    def print_obj(self):
        pass

    ## set debug mode
    #
    # \param[in] _is_debug when true some debug message will show up.
    def set_debug_mode(self, _is_debug):
        self.is_debug = _is_debug

    ## is debug mode?
    #
    # \return true when debug mode is on
    def is_debug_mode(self):
        return self.is_debug

    ## debug output
    #
    # \param[in] _dbgmes debug message. when debug mode is on, this is visible.
    def debug_out(self, _dbgmes):
        if self.is_debug == True:
            print _dbgmes


## OpenGL TriMeshNode
#
# A triangle mesh node
class GLTriMeshNode(GLSceneGraphNode):
    ## default constructor
    def __init__(self):
        # call base class constructor to fill the members
        super(GLTriMeshNode, self).__init__()
        self.local_drawmode = 0
        self.drawmode = DrawMode.DrawModeList()
        # basic draw mode only
        self.drawmode.add_basic_drawmode()

        # OpenGL draw state
        self.bg_color4f      = None
        self.current_color4f = None
        self.shade_model     = GL.GL_FLAT
        self.is_enabled_lighting  = GL.GL_TRUE
        self.is_enabled_depthtest = GL.GL_TRUE
        self.is_enabled_offset    = GL.GL_FALSE


    ## get classname
    #
    # \return class name string
    def get_classname(self):
        return 'GLTriMeshNode'

    ## get draw mode of this GLSceneGraphNode
    #
    # \return return drawmode
    def get_drawmode(self):
        return self.drawmode

    ## draw
    #
    # \param[in] _drawmode drawmode (or-ed drawmode bitmap)
    def draw(self, _drawmode):
        # print 'DEBUG: primitive is ' + self.primitive.get_classname()

        # push the current GL state
        self.draw_push_gl_state()

        if ((_drawmode & DrawMode.DrawModeList.DM_BBox) != 0):
            self.draw_bbox()

        if ((_drawmode & DrawMode.DrawModeList.DM_Points) != 0):
            self.draw_points()

        if ((_drawmode & DrawMode.DrawModeList.DM_Wireframe) != 0):
            self.draw_wireframe()

        if ((_drawmode & DrawMode.DrawModeList.DM_Hiddenline) != 0):
            self.draw_hiddenline()

        if ((_drawmode & DrawMode.DrawModeList.DM_Solid_Basecolor) != 0):
            self.draw_solid_basecolor()

        if ((_drawmode & DrawMode.DrawModeList.DM_Solid_Flat) != 0):
            self.draw_flat_shading()

        if ((_drawmode & DrawMode.DrawModeList.DM_Solid_Gouraud) != 0):
            self.draw_solid_gouraud()

        if ((_drawmode & DrawMode.DrawModeList.DM_Solid_Texture) != 0):
            self.draw_solid_texture()

        # pop the current GL state
        self.draw_pop_gl_state()



    ## push the gl state that draw might change
    #
    # Subroutine of draw()
    def draw_push_gl_state(self):
        self.bg_color4f      = GL.glGetFloatv(GL.GL_COLOR_CLEAR_VALUE)

        self.current_color4f = GL.glGetFloatv(GL.GL_CURRENT_COLOR)
        self.shade_model     = GL.glGetIntegerv(GL.GL_SHADE_MODEL)
        self.is_enabled_lighting   = GL.glIsEnabled(GL.GL_LIGHTING)
        self.is_enabled_depthtest  = GL.glIsEnabled(GL.GL_DEPTH_TEST)
        self.is_enabled_offsetfill = GL.glIsEnabled(GL.GL_POLYGON_OFFSET_FILL)


    ## pop the gl state
    #
    # Subroutine of draw()
    def draw_pop_gl_state(self):
        GL.glColor4fv(self.current_color4f)
        GL.glShadeModel(self.shade_model)
        self.gl_enable_disable(GL.GL_LIGHTING,   self.is_enabled_lighting)
        self.gl_enable_disable(GL.GL_DEPTH_TEST, self.is_enabled_depthtest)
        self.gl_enable_disable(GL.GL_POLYGON_OFFSET_FILL, self.is_enabled_offsetfill)

    ## glEnable/glDisable function
    #
    # \param[in] _gl_function_name function name. ex. GL_LIGHTING
    # \param[in] _is_enable GLBoolean (GL_TRUE, GL_FALSE)
    def gl_enable_disable(self, _gl_function_name, _is_enable):
        if (_is_enable == GL.GL_TRUE):
            GL.glEnable(_gl_function_name)
        else:
            GL.glDisable(_gl_function_name)


    ## draw bbox
    def draw_bbox(self):
        assert(self.is_primitive_node() == True)
        # self.primitive.update_bbox()
        bbox = self.primitive.get_bbox()
        GLUtil.draw_axis_alighed_box(bbox.get_min(), bbox.get_max())


    ## draw points
    def draw_points(self):
        # no light mode NIN: self.gl_light_mode & POINTS
        GL.glDisable(GL.GL_LIGHTING)
        GL.glBegin(GL.GL_POINTS)
        # draw all points
        for vp in self.primitive.vertex_list:
            GL.glVertex3d(vp[0], vp[1], vp[2])
        GL.glEnd()

    ## draw wireframe
    def draw_wireframe(self):
        GL.glShadeModel(GL.GL_FLAT)

        GL.glBegin(GL.GL_LINE_LOOP)
        # vp reference
        vp = self.primitive.vertex_list
        for face in self.primitive.face_idx_list:
            GL.glVertex3d(vp[face[0]][0], vp[face[0]][1], vp[face[0]][2])
            GL.glVertex3d(vp[face[1]][0], vp[face[1]][1], vp[face[1]][2])
            GL.glVertex3d(vp[face[2]][0], vp[face[2]][1], vp[face[2]][2])
        GL.glEnd()

    ## draw hiddenline
    #
    # see OpenGL book
    def draw_hiddenline(self):
        #
        # step 1: draw lines
        #
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glColor4fv(self.current_color4f)

        # --- draw lines
        GL.glBegin(GL.GL_LINE_LOOP)
        vp = self.primitive.vertex_list
        for face in self.primitive.face_idx_list:
            GL.glVertex3d(vp[face[0]][0], vp[face[0]][1], vp[face[0]][2])
            GL.glVertex3d(vp[face[1]][0], vp[face[1]][1], vp[face[1]][2])
            GL.glVertex3d(vp[face[2]][0], vp[face[2]][1], vp[face[2]][2])
        GL.glEnd()

        #
        # step 2: fill the polygon with bg color with slight offset
        #
        GL.glDisable(GL.GL_LIGHTING)

        # type(offset0) == 'numpy.float32'
        offset0 = GL.glGetFloatv(GL.GL_POLYGON_OFFSET_FACTOR)
        offset1 = GL.glGetFloatv(GL.GL_POLYGON_OFFSET_UNITS)

        GL.glEnable(GL.GL_POLYGON_OFFSET_FILL)
        GL.glPolygonOffset(1.0, 1.0)
        GL.glColor4fv(self.bg_color4f)

        GL.glEnable(GL.GL_POLYGON_OFFSET_FILL)
        GL.glBegin(GL.GL_TRIANGLES)
        vp = self.primitive.vertex_list
        for face in self.primitive.face_idx_list:
            GL.glVertex3d(vp[face[0]][0], vp[face[0]][1], vp[face[0]][2])
            GL.glVertex3d(vp[face[1]][0], vp[face[1]][1], vp[face[1]][2])
            GL.glVertex3d(vp[face[2]][0], vp[face[2]][1], vp[face[2]][2])
        GL.glEnd()          # GL.glBegin(GL.GL_TRIANGLES)

        GL.glPolygonOffset(offset0, offset1)


    ## draw solid_basecolor
    def draw_solid_basecolor(self):
        GL.glDisable(GL.GL_LIGHTING)
        GL.glShadeModel(GL.GL_FLAT)

        GL.glBegin(GL.GL_TRIANGLES)
        vp = self.primitive.vertex_list
        for face in self.primitive.face_idx_list:
            GL.glVertex3d(vp[face[0]][0], vp[face[0]][1], vp[face[0]][2])
            GL.glVertex3d(vp[face[1]][0], vp[face[1]][1], vp[face[1]][2])
            GL.glVertex3d(vp[face[2]][0], vp[face[2]][1], vp[face[2]][2])
        GL.glEnd()

    ## draw flat shading
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

    ## draw solid_gouraud
    def draw_solid_gouraud(self):
        GL.glShadeModel(GL.GL_FLAT)
        print 'NIN: draw_solid_gouraud'

    ## draw solid_texture
    def draw_solid_texture(self):
        GL.glShadeModel(GL.GL_FLAT)
        print 'NIN: draw_solid_texture'


## OpenGL scenegraph node factory
#
# Supported node:
# - TriMesh: triangle mesh node (GLTriMeshNode)
#
# \param[in] _primitive primitive name 
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


## collect all drawmode in the scenegraph
class GLSGTCollectDrawmodeStrategy(SceneGraph.SceneGraphTraverseStrategyIF):
    ## constructor
    def __init__(self):
        self.drawmodelist = DrawMode.DrawModeList()

    ## apply strategy to node before recurse. Implementation
    #
    # add new bbox if needed
    #
    # \param[in]  _cur_node current visting node
    # \param[in]  _level    current depth
    #
    def apply_before_recurse(self, _cur_node, _level):
        pass

    ## apply strategy while visiting children. Implementation
    #
    # expand this level's bounding box
    #
    # \param[in]  _cur_node current visting node
    # \param[in]  _level    current depth
    #
    def apply_middle(self, _cur_node, _level):
        pass


    ## apply strategy after visiting (when returning from the
    ## recurse). Implementation
    #
    # if this is not the root, expand the one level up's bbox
    #
    # \param[in]  _cur_node current visting node
    # \param[in]  _level    current depth
    #
    def apply_after_recurse(self, _cur_node, _level):
        self.drawmodelist.or_drawmode(_cur_node.get_drawmode())


#
# main test
#
# if __name__ == '__main__':
