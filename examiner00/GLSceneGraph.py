#!/usr/bin/env python

"""GLSceneGraph module
\file
\brief OpenGL scene graph module"""

from OpenGL import GL
from OpenGL import GLU

import Camera
import DrawMode
import SceneGraph
import GLUtil

# OpenGL scene graph
class GLSceneGraph(SceneGraph.SceneGraph):
    """OpenGL scene graph
    This has
      - GLCamera
      - GLroot_node
    """

    # public: ------------------------------------------------------------

    # default constructor
    def __init__(self):
        """default constructor. (public)"""
        self.__gl_camera    = Camera.GLCamera()
        self.__gl_root_node = None
        self.__scenegraph   = None

    # set generic scene graph.
    def set_scenegraph(self, _sg):
        """set generic scene graph. (public)

        Generic scenegraph is for both OpenGL rendering and Path tracing
        rendering.

        \param[in] _sg generic scenegraph"""

        self.__scenegraph   = _sg

        self.__gl_root_node = GLSceneGraphNode('gl_rootnode')

        # check self.__scenegraph validity

        # create GLSceneGraph from scenegraph
        self.__copy_sgnode_sub(self.__scenegraph.get_root_node(),
                               self.__gl_root_node,
                               0)

        self.__print_sgnode_sub(self.__gl_root_node, 0)

    # get generic scene graph.
    def get_scenegraph(self):
        """get generic scene graph. (public)
        \return generic scenegraph.
        """
        return self.__scenegraph

    # get OpenGL scene graph root.
    def get_gl_root_node(self):
        """get OpenGL scene graph's root node. (public)
        \return root node of OpenGL scenegraph.
        """
        return self.__gl_root_node


    # scenegraph draw
    def draw(self, _global_mode):
        """scenegraph draw. (public)

        \param[in] _global_mode global draw mode"""

        self.__gl_root_node.draw(_global_mode)


    # print object for debug
    def print_obj(self):
        """print object for debug. (public)"""
        print 'NIN: GLSceneGraph: print_obj()'

    # collect all __drawmode_list list
    def collect_drawmode_list(self):
        """collect all __drawmode_list list. (public)
        traverse with SceneGraphTraverseStrategyIF strategy
        \see SceneGraphTraverseStrategyIF"""

        collect_drawmode_strategy = GLSGTCollectDrawmodeStrategy()
        self.traverse_sgnode(self.__gl_root_node, collect_drawmode_strategy)
        # print 'DEBUG: collect draw mode done.'
        # collect_drawmode_strategy.drawmodelist.print_obj()
        return collect_drawmode_strategy.get_drawmode_list()

    # private: ------------------------------------------------------------

    # copy scenegraph tree subroutine
    def __copy_sgnode_sub(self, _cur_sgnode, _cur_glnode, _level):
        """copy scenegraph tree subroutine. (private)
        \param[in] _cur_sgnode current visiting (generic) scenegraph node
        \param[in] _cur_glnode current visiting OpenGL scenegraph node
        \param[in] _level      current depth level"""

        if _cur_sgnode.is_primitive_node() == True:
            # create primitive node and set the primitive
            print 'DEBUG: Create primitive and set'
            gl_prim_node = new_gl_scenegraph_primitive_node(
                _cur_sgnode.get_primitive())
            print 'DEBUG: Created: ' + gl_prim_node.get_classname()
            _cur_glnode.set_primitive(gl_prim_node)

        else:
            print 'DEBUG: Go to children'
            for ch_sgnode in _cur_sgnode.get_children():
                # create and refer the sg node
                ch_glnode = GLSceneGraphNode(ch_sgnode.get_nodename())
                _cur_glnode.append_child(ch_glnode)
                self.__copy_sgnode_sub(ch_sgnode, ch_glnode, _level + 1)

    # print out scenegraph nodes for debug (subroutine of print_sgnode)
    def __print_sgnode_sub(self, _cur_glnode, _level):
        """print out scenegraph nodes for debug. (private)
        subroutine of print_sgnode.
        \param[in] _cur_glnode currect visiting gl node
        \param[in] _level      current visiting depth"""

        _cur_glnode.print_glnodeinfo(_level)
        if (not _cur_glnode.is_primitive_node()):
            # __children container
            for chnode in _cur_glnode.get_children():
                self.__print_sgnode_sub(chnode, _level + 1)



# OpenGL scene graph node (BaseNode/GroupNode)
class GLSceneGraphNode(SceneGraph.SceneGraphNode):
    """OpenGL scene graph node. BaseNode/GroupNode.

    This has either
      - children
      - primitive
    These are exclusive."""

    # default constructor
    def __init__(self, _nodename):
        """default constructor
        \param[in] _nodename node name
        """
        SceneGraph.SceneGraphNode.__init__(self, _nodename)
        self.__is_debug  = False
        self.__is_active = True
        # can not have the same name method and member variable
        self.__drawmode  = DrawMode.DrawModeList.DM_GlobalMode

    # get classname (shown in the SceneGraph viewer as node Type)
    def get_classname(self):
        """get classname (shown in the SceneGraph viewer as node Type)
        \return class name"""

        return 'GLSceneGraphNode'

    # set node active (shown in the SceneGraph viewer as Status)
    def set_node_active(self, _is_active):
        """set node active (shown in the SceneGraph viewer as Status)
        \param[in] _is_active when True, node status is active,
        otherwise deactivated."""

        self.__is_active = _is_active

    # set node active (shown in the SceneGraph viewer as Status)
    def is_node_active(self):
        """set node active (shown in the SceneGraph viewer as Status)
        \return True if this node is active"""

        return self.__is_active

    # get node active state string
    def get_active_state(self):
        """get node active state string
        \return get node active state string"""

        if self.is_node_active():
            return 'Active'
        else:
            return 'Deactivated'

    # set node global drawmode (shown in the SceneGraph viewer as Mode)
    def set_drawmode(self, _drawmode):
        """set node drawmode (shown in the SceneGraph viewer as Mode)
        \param[in] _drawmode when DrawMode.DM_GlobalMode, node
        drawmode is global, otherwise local."""

        self.__drawmode = _drawmode

    # is node global __drawmode_list (shown in the SceneGraph viewer as Mode)
    def get_drawmode(self):
        """is node global drawmode (shown in the SceneGraph viewer as Mode)
        \return when True, node drawmode is global"""

        return self.__drawmode

    # get draw mode string
    def get_drawmode_str(self):
        """get draw mode string.

        \return draw mode string"""

        dmstr = DrawMode.get_drawmode_string(self.get_drawmode())
        return dmstr

    # print glnode info. Indentation is according to the depth level
    def print_glnodeinfo(self, _level):
        """print glnode info. Indentation is according to the depth level

        \param[in] _level node depth level"""

        indent = '  ' * _level
        if (self.is_primitive_node()):
            print indent + '# ' + self.get_classname() + ':Primitive'

        print indent + '# # __children = ' + str(len(self.get_children()))


    # draw by mode
    def draw(self, _global_mode):
        """draw by mode

        \param[in] _global_mode global draw mode
        \see DrawMode"""

        # print self.get_classname() + '::draw is called with ' +\
        #     str(_global_mode)

        if (not self.is_node_active()):
            # node is deactivated, not call draw anymore
            return

        if (self.is_primitive_node()):
            # __primitive: draw itself
            self.get_primitive().draw(_global_mode)
            # print self.get_classname() + '::draw: call __primitive draw'
        elif len(self.get_children()) > 0:
            # no __primitive: draw __children
            for ch_glnode in self.get_children():
                # create and refer the sg node
                ch_glnode.draw(_global_mode)
                # print self.get_classname() + '::draw: call child draw'
        else:
            self.debug_out('Node has no __primitive, no __children')
            print self.get_classname() + '::draw: neither'

    # get draw mode of this GLSceneGraphNode
    def get_drawmode_list(self):
        """get draw mode of this GLSceneGraphNode

        \return return __drawmode_list, maybe None"""

        if (self.is_primitive_node()):
            return self.get_primitive().get_drawmode_list()

        return None
        # raise StandardError, (
        # 'GLSceneGraphNode.get_drawmode_list() must be implemented ' +
        # 'in derived class. classname = ' + self.get_classname())

    # get info of this node
    def get_info_html_GLSceneGraphNode(self):
        """get GLSceneGraphNode base info html text.
        \return base GL node info."""

        ret_s = '<h2>GLSceneGraphNode information</h2>\n' +\
            '<h2>General information</h2>\n' +\
            '<ul>\n' +\
            '  <li><b>Class name:</b> ' + self.get_classname()    + '\n' +\
            '  <li><b>Name:</b> '       + self.get_nodename()     + '\n' +\
            '  <li><b>Status:</b> '     + self.get_active_state() + '\n' +\
            '  <li><b>Drawmode:</b> '   + self.get_drawmode_str() + '\n' +\
            '</ul>\n'

        # print 'DEBUG: get_info_html_GLSceneGraphNode\n' + ret_s

        return ret_s


    # get info of this node
    def get_info_html(self):
        """Get information html text.
        Usually, this should be overrided.
        \return base GL node info.
        """
        ret_s = self.get_info_html_GLSceneGraphNode()

        return ret_s



    # print this obj for debug
    def print_obj(self):
        """print this obj for debug"""
        pass

    # set debug mode
    def set_debug_mode(self, _is_debug):
        """set debug mode

        \param[in] _is_debug when true some debug message will show up."""

        self.__is_debug = _is_debug

    # is debug mode?
    def is_debug_mode(self):
        """is debug mode?

        \return true when debug mode is on"""

        return self.__is_debug

    # debug output
    def debug_out(self, _dbgmes):
        """debug output

        \param[in] _dbgmes debug message. when debug mode is on, this is visible.
        """

        if self.__is_debug == True:
            print _dbgmes


# OpenGL TriMeshNode
class GLTriMeshNode(GLSceneGraphNode):
    """OpenGL TriMeshNode

    A triangle mesh node"""

    # default constructor
    def __init__(self, _nodename):
        """default constructor.
        \param[in] _nodename this node name."""
        # call base class constructor to fill the members
        GLSceneGraphNode.__init__(self, _nodename)
        self.__local_drawmode = 0
        self.__drawmode_list = DrawMode.DrawModeList()
        # basic draw mode only
        self.__drawmode_list.add_basic_drawmode()

        # OpenGL draw state
        self.__bg_color4f      = None
        self.__current_color4f = None
        self.__shade_model     = GL.GL_FLAT
        self.__is_enabled_lighting  = GL.GL_TRUE
        self.__is_enabled_depthtest = GL.GL_TRUE
        self.__is_enabled_offset    = GL.GL_FALSE


    # get classname
    def get_classname(self):
        """get classname

        \return class name string"""

        return 'GLTriMeshNode'

    # get draw mode of this GLSceneGraphNode
    def get_drawmode_list(self):
        """get draw mode list of this GLSceneGraphNode

        \return drawmode list of this node"""

        return self.__drawmode_list

    # draw
    def draw(self, _global_drawmode):
        """draw the attached triangle mesh.
        If node is deactivated, draw nothing.
        \param[in] _global_drawmode drawmode list (or-ed drawmode list bitmap)."""

        # print 'DEBUG: primitive is ' + self.get_primitive().get_classname()

        if (not self.is_node_active()):
            # node is deactivated, not call draw anymore
            return

        # check this node's drawmode. Is it local?
        _drawmode = self.get_drawmode();
        if (_drawmode == DrawMode.DrawModeList.DM_GlobalMode):
            _drawmode = _global_drawmode

        # push the current GL state
        self.__draw_push_gl_state()

        if ((_drawmode & DrawMode.DrawModeList.DM_BBox) != 0):
            self.__draw_bbox()

        if ((_drawmode & DrawMode.DrawModeList.DM_Points) != 0):
            self.__draw_points()

        if ((_drawmode & DrawMode.DrawModeList.DM_Wireframe) != 0):
            self.__draw_wireframe()

        if ((_drawmode & DrawMode.DrawModeList.DM_Hiddenline) != 0):
            self.__draw_hiddenline()

        if ((_drawmode & DrawMode.DrawModeList.DM_Solid_Basecolor) != 0):
            self.__draw_solid_basecolor()

        if ((_drawmode & DrawMode.DrawModeList.DM_Solid_Flat) != 0):
            self.__draw_flat_shading()

        if ((_drawmode & DrawMode.DrawModeList.DM_Solid_Gouraud) != 0):
            self.__draw_solid_gouraud()

        if ((_drawmode & DrawMode.DrawModeList.DM_Solid_Texture) != 0):
            self.__draw_solid_texture()

        # pop the current GL state
        self.__draw_pop_gl_state()


    # push the gl state that draw might change
    def __draw_push_gl_state(self):
        """push the gl state that draw might change

        Subroutine of draw()"""

        self.__bg_color4f      = GL.glGetFloatv(GL.GL_COLOR_CLEAR_VALUE)

        self.__current_color4f = GL.glGetFloatv(GL.GL_CURRENT_COLOR)
        self.__shade_model     = GL.glGetIntegerv(GL.GL_SHADE_MODEL)
        self.__is_enabled_lighting   = GL.glIsEnabled(GL.GL_LIGHTING)
        self.__is_enabled_depthtest  = GL.glIsEnabled(GL.GL_DEPTH_TEST)
        self.__is_enabled_offsetfill = GL.glIsEnabled(GL.GL_POLYGON_OFFSET_FILL)


    # pop the gl state
    def __draw_pop_gl_state(self):
        """pop the gl state

        Subroutine of draw()"""

        GL.glColor4fv(self.__current_color4f)
        GL.glShadeModel(self.__shade_model)
        self.__gl_enable_disable(GL.GL_LIGHTING,   self.__is_enabled_lighting)
        self.__gl_enable_disable(GL.GL_DEPTH_TEST, self.__is_enabled_depthtest)
        self.__gl_enable_disable(GL.GL_POLYGON_OFFSET_FILL,
                                 self.__is_enabled_offsetfill)

    # glEnable/glDisable function
    def __gl_enable_disable(self, _gl_function_name, _is_enable):
        """glEnable/glDisable function

        \param[in] _gl_function_name function name. ex. GL_LIGHTING
        \param[in] _is_enable GLBoolean (GL_TRUE, GL_FALSE)
        """

        if (_is_enable == GL.GL_TRUE):
            GL.glEnable(_gl_function_name)
        else:
            GL.glDisable(_gl_function_name)


    # draw bbox
    def __draw_bbox(self):
        """draw bbox"""

        assert(self.is_primitive_node() == True)
        # self.get_primitive().update_bbox()
        bbox = self.get_primitive().get_bbox()
        GLUtil.draw_axis_alighed_box(bbox.get_min(), bbox.get_max())


    # draw points
    def __draw_points(self):
        """draw points"""

        # no light mode NIN: self.gl_light_mode & POINTS
        GL.glDisable(GL.GL_LIGHTING)
        GL.glBegin(GL.GL_POINTS)
        # draw all points
        for vp in self.get_primitive().vertex_list:
            GL.glVertex3d(vp[0], vp[1], vp[2])
        GL.glEnd()

    # draw wireframe
    def __draw_wireframe(self):
        """draw wireframe"""
        GL.glShadeModel(GL.GL_FLAT)

        # vp reference
        vp = self.get_primitive().vertex_list
        for face in self.get_primitive().face_idx_list:
            GL.glBegin(GL.GL_LINE_LOOP)
            GL.glVertex3d(vp[face[0]][0], vp[face[0]][1], vp[face[0]][2])
            GL.glVertex3d(vp[face[1]][0], vp[face[1]][1], vp[face[1]][2])
            GL.glVertex3d(vp[face[2]][0], vp[face[2]][1], vp[face[2]][2])
            GL.glEnd()

    # draw hiddenline
    def __draw_hiddenline(self):
        """draw hiddenline

        see OpenGL book"""

        #
        # step 1: draw lines
        #
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glColor4fv(self.__current_color4f)

        # --- draw lines
        vp = self.get_primitive().vertex_list
        for face in self.get_primitive().face_idx_list:
            GL.glBegin(GL.GL_LINE_LOOP)
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
        GL.glColor4fv(self.__bg_color4f)

        GL.glEnable(GL.GL_POLYGON_OFFSET_FILL)
        GL.glBegin(GL.GL_TRIANGLES)
        vp = self.get_primitive().vertex_list
        for face in self.get_primitive().face_idx_list:
            GL.glVertex3d(vp[face[0]][0], vp[face[0]][1], vp[face[0]][2])
            GL.glVertex3d(vp[face[1]][0], vp[face[1]][1], vp[face[1]][2])
            GL.glVertex3d(vp[face[2]][0], vp[face[2]][1], vp[face[2]][2])
        GL.glEnd()          # GL.glBegin(GL.GL_TRIANGLES)

        GL.glPolygonOffset(offset0, offset1)


    # draw solid_basecolor
    def __draw_solid_basecolor(self):
        """draw solid_basecolor"""
        GL.glDisable(GL.GL_LIGHTING)
        GL.glShadeModel(GL.GL_FLAT)

        GL.glBegin(GL.GL_TRIANGLES)
        vp = self.get_primitive().vertex_list
        for face in self.get_primitive().face_idx_list:
            GL.glVertex3d(vp[face[0]][0], vp[face[0]][1], vp[face[0]][2])
            GL.glVertex3d(vp[face[1]][0], vp[face[1]][1], vp[face[1]][2])
            GL.glVertex3d(vp[face[2]][0], vp[face[2]][1], vp[face[2]][2])
        GL.glEnd()

    # draw flat shading
    def __draw_flat_shading(self):
        """draw flat shading"""
        GL.glShadeModel(GL.GL_FLAT)

        GL.glBegin(GL.GL_TRIANGLES)
        # vp reference
        vp = self.get_primitive().vertex_list
        for face in self.get_primitive().face_idx_list:
            GL.glVertex3d(vp[face[0]][0], vp[face[0]][1], vp[face[0]][2])
            GL.glVertex3d(vp[face[1]][0], vp[face[1]][1], vp[face[1]][2])
            GL.glVertex3d(vp[face[2]][0], vp[face[2]][1], vp[face[2]][2])
        GL.glEnd()

    # draw solid_gouraud
    def __draw_solid_gouraud(self):
        """draw solid_gouraud"""
        GL.glShadeModel(GL.GL_FLAT)
        print 'NIN: __draw_solid_gouraud'

    # draw solid_texture
    def __draw_solid_texture(self):
        """draw solid_texture"""
        GL.glShadeModel(GL.GL_FLAT)
        print 'NIN: __draw_solid_texture'


# OpenGL scenegraph node factory
def new_gl_scenegraph_primitive_node(_primitive):
    """OpenGL scenegraph node factory

    Supported node:
      - TriMesh: triangle mesh node (GLTriMeshNode)

    \param[in] _primitive primitive name
    """

    if _primitive == None:
        raise StandardError, ('Null primitive.')

    if _primitive.get_classname() == 'TriMesh':
        print 'DEBUG: created Trimesh Primitive'
        tmeshnode = GLTriMeshNode('testTriMesh')
        tmeshnode.set_primitive(_primitive)
        return tmeshnode
    else:
        print 'unsupported primitive: ' + _primitive.get_classname()
        return None


# collect all drawmode in the scenegraph
class GLSGTCollectDrawmodeStrategy(SceneGraph.SceneGraphTraverseStrategyIF):
    """collect all drawmode_list in the scenegraph"""

    # constructor
    def __init__(self):
        """constructor"""
        self.__drawmodelist = DrawMode.DrawModeList()

    # apply strategy to node before recurse. Implementation
    def apply_before_recurse(self, _cur_node, _level):
        """apply strategy to node before recurse. Implementation

        add new bbox if needed

        \param[in]  _cur_node current visting node
        \param[in]  _level    current depth"""
        pass

    # apply strategy while visiting children. Implementation
    def apply_middle(self, _cur_node, _level):
        """apply strategy while visiting children. Implementation

        expand this level's bounding box

        \param[in]  _cur_node current visting node
        \param[in]  _level    current depth"""

        pass


    # apply strategy after visiting
    def apply_after_recurse(self, _cur_node, _level):
        """apply strategy after visiting (when returning from the
        recurse). Implementation

        if this is not the root, expand the one level up's bbox

        \param[in]  _cur_node current visiting node
        \param[in]  _level    current depth
        """

        self.__drawmodelist.or_drawmode(_cur_node.get_drawmode_list())


    # get the result
    def get_drawmode_list(self):
        """get the drawmode list.
        \return collected drawmode list."""
        return self.__drawmodelist

#
# main test
#
# if __name__ == '__main__':
