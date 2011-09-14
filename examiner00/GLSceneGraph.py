#!/usr/bin/env python
#
# Copyright (C) 2010-2011 Yamauchi, Hitoshi
#

"""GLSceneGraph module
\file
\brief OpenGL scene graph module"""

from OpenGL import GL, GLU
from PyQt4  import QtCore, QtGui
from ifgi.base      import numpy_util, Listener
from ifgi.base.ILog import ILog
from ifgi.scene import Camera, SceneGraph
import math, numpy, copy
import QtWidgetIO

import DrawMode, GLUtil

# ----------------------------------------------------------------------

class GLSceneGraph(SceneGraph.SceneGraph):
    """OpenGL scene graph
    This has
      - GLroot_node
      - GLCamera node
      - GLLight  node
      - GLSceneGraph node (group)
    """

    def __init__(self):
        """default constructor. (public)"""
        self.__cur_gl_camera = None
        self.__gl_root_node  = None
        self.__scenegraph    = None
        self.__name_material_dict = None


    def set_scenegraph(self, _sg):
        """set generic scene graph. (public)

        Generic scenegraph is for both OpenGL rendering and Path tracing
        rendering.

        \param[in] _sg generic scenegraph"""

        self.__scenegraph   = _sg

        self.__gl_root_node = \
            GLSceneGraphNode('GL:' + self.__scenegraph.get_root_node().get_nodename())
        assert(self.__scenegraph.is_valid())

        # create GLSceneGraph from scenegraph
        self.__create_glscenegraph(self.__scenegraph.get_root_node(),
                                   self.__gl_root_node)

        # self.__print_sgnode_sub(self.__gl_root_node, 0)


    def get_scenegraph(self):
        """get generic scene graph. (public)
        \return generic scenegraph.
        """
        return self.__scenegraph


    def get_gl_root_node(self):
        """get OpenGL scene graph's root node. (public)
        \return root node of OpenGL scenegraph.
        """
        return self.__gl_root_node


    def set_current_gl_camera(self, _glcamera):
        """set current GL camera.
        \param[in] _glcamera gl camera"""
        if (type(_glcamera) != Camera.GLCamera):
            raise StandardError('set_current_gl_camera: _glcamera is not a GLCamera')

        # shallow copy.
        self.__cur_gl_camera = _glcamera


    def get_current_gl_camera(self):
        """set current GL camera.
        \return current gl camera"""

        return self.__cur_gl_camera


    def is_valid(self):
        """is this scenegraph valid?
        Perform a simple validity test."""
        if (self.__cur_gl_camera == None):
            print 'No camera'
            return False

        if (self.__gl_root_node  == None):
            print 'No rootnode'
            return False

        if (self.__scenegraph    == None):
            print 'No scenegraph'
            return False

        return True


    def draw_traverse(self, _global_mode):
        """scenegraph draw. (public)

        \param[in] _global_mode global draw mode
        """
        self.__draw_traverse_sub(self.__gl_root_node, _global_mode)


    def print_obj(self):
        """print object for debug. (public)"""
        print 'NIN: GLSceneGraph: print_obj()'


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

    def __create_glscenegraph(self, _sg_rootnode, _gl_rootnode):
        """create GLSceneGraph from SceneGraph main routine.
        \param[in] _sg_rootnode ifgi scenegraph rootnode
        \param[in] _gl_rootnode GL scenegraph node
        """
        # Add OpenGL scenegraph specific nodes to the GL rootnode.
        # { GLLightNode, GLMaterialNode (for environment) }
        ch_gl_light_node = GLLightNode('GL:light_node')
        _gl_rootnode.append_child(ch_gl_light_node)

        environment_mat = None

        # clear material name -> material reference
        self.__name_material_dict = {}

        # handle special nodes just under the root.
        for sgnode in _sg_rootnode.get_children():
            if (type(sgnode) == SceneGraph.CameraNode):
                # handle special nodes: { CamaraNode }
                print 'Camera is detected, special handling.'
                ch_gl_camera_node = GLCameraNode(sgnode)
                _gl_rootnode.append_child(ch_gl_camera_node)
                self.set_current_gl_camera(ch_gl_camera_node.get_gl_camera())

            elif (sgnode.get_nodename() == 'materialgroup'):
                # handle special group: 'materialgroup'
                print 'SceneraphNode: materialgroup is detected, special handling.'
                for matnode in sgnode.get_children():
                    mat = matnode.get_material()
                    # material name should be unique
                    assert(not (mat.get_material_name() in self.__name_material_dict))
                    self.__name_material_dict[mat.get_material_name()] = mat
                    # check environment node exists
                    if(mat.get_classname() == 'EnvironmentMaterial'):
                        # should be only one environment material
                        assert(environment_mat == None)
                        environment_mat = mat

                print str(len(self.__name_material_dict)) + ' materials are referenced.'

        if(environment_mat != None):
            ch_gl_envmat_node = GLEnvironmentMaterialNode('GL:environment')
            ch_gl_envmat_node.set_material(environment_mat)
            _gl_rootnode.append_child(ch_gl_envmat_node)
        else:
            ILog.warn('no environment material found in the scenegraph.')


        # construct GL scenegraph from the ifgi scenegraph
        self.__create_glscenegraph_sub(_sg_rootnode, _gl_rootnode, 0)


    def __create_glscenegraph_sub(self, _cur_sgnode, _cur_glnode, _level):
        """create GLSceneGraph from SceneGraph subroutine.
        \param[in] _cur_sgnode current ifgi scenegraph node
        \param[in] _cur_glnode current GL scenegraph node
        \param[in] _level graph depth level
        """

        for ch_sgnode in _cur_sgnode.get_children():
            # create and refer the sg node
            if (type(ch_sgnode) == SceneGraph.CameraNode):
                print 'DEBUG: skip Camera.'
            elif (ch_sgnode.get_nodename() == 'materialgroup'):
                print 'DEBUG: skip materialgroup.'
            else:
                # general node
                ch_glnode = new_gl_scenegraph_node(ch_sgnode, self.__name_material_dict)
                _cur_glnode.append_child(ch_glnode)
                print 'DEBUG: append ', ch_glnode.get_classname()
                self.__create_glscenegraph_sub(ch_sgnode, ch_glnode, _level + 1)


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


    def update_all_bbox(self):
        """update all bounding box recursively.
        \see SGTUpdateBBoxStrategy
        """
        # recompute gl_root_node bbox
        self.__gl_root_node.get_bbox().invalidate()

        update_bbox_strategy = SceneGraph.SGTUpdateBBoxStrategy()
        self.traverse_sgnode(self.__gl_root_node, update_bbox_strategy)
        # handle no children have valid bbox (e.g., empty scene)
        root_bbox = self.__gl_root_node.get_bbox()
        if not root_bbox.has_volume():
            # no volume, but, there may be area.
            if (root_bbox.get_rank() >= 1):
                ILog.warn('GLSceneGraphs rootnode has no volume, but length or area')
                maxpoi = root_bbox.get_min()
                tflist = root_bbox.get_min() < root_bbox.get_max()
                for i in range(0,2):
                    if tflist[i]:
                        maxpoi[i] += 1 # expand this dimension
                self.__gl_root_node.get_bbox().insert_point(root_bbox.get_min())
                self.__gl_root_node.get_bbox().insert_point(maxpoi)
            else:
                ILog.warn('GLSceneGraphs rootnode has no volume, set [0,0,0]-[1,1,1]')
                self.__gl_root_node.get_bbox().insert_point(numpy.array([0,0,0]))
                self.__gl_root_node.get_bbox().insert_point(numpy.array([1,1,1]))



    # ------------------------------------------------------------
    # draw traverse.
    # ------------------------------------------------------------

    def __draw_traverse_sub(self, _cur_node, _global_mode):
        """draw travertse the scenegraph. subroutine of draw_traverse

        This traverse is not traverse all the nodes. (depends on
        active/deactive) So, This doesn't use strategy, but maybe it's
        possible.

        \param[in] _cur_node current visiting node
        \param[in] _global_draw_mode global draw mode
        """

        if (not _cur_node.is_node_active()):
            # node is deactivated, not call draw anymore
            return

        # prologue of draw.
        _cur_node.enter()
        _cur_node.draw(_global_mode)

        # visit children
        if len(_cur_node.get_children()) > 0:
            for ch_glnode in _cur_node.get_children():
                self.__draw_traverse_sub(ch_glnode, _global_mode)

        # epilogue for draw.
        _cur_node.leave()


# ----------------------------------------------------------------------

class GLSceneGraphNode(SceneGraph.SceneGraphNode):
    """OpenGL scene graph node. BaseNode/GroupNode.

    This has an Subject (Observer/Listener pattern).
    How node states change propagates, \see QtSceneGraphWidget
    """

    # default constructor
    def __init__(self, _nodename):
        """default constructor
        \param[in] _nodename node name
        """
        super(GLSceneGraphNode, self).__init__(_nodename)
        self.__is_debug  = False
        self.__is_active = True
        # can not have the same name method and member variable
        self.__drawmode  = DrawMode.DrawModeList.DM_GlobalMode
        self.__observer_subject = Listener.Subject('SceneGraphNode')


    def gl_enable_disable(self, _gl_function_name, _is_enable):
        """glEnable/glDisable function for the inherited nodes

        \param[in] _gl_function_name function name. ex. GL_LIGHTING
        \param[in] _is_enable GLBoolean (GL_TRUE, GL_FALSE)
        """

        if (_is_enable == GL.GL_TRUE):
            GL.glEnable(_gl_function_name)
        else:
            GL.glDisable(_gl_function_name)

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
        \return node drawmode (default DrawMode.DrawModeList.DM_GlobalMode)"""

        return self.__drawmode

    # get draw mode string
    def get_drawmode_str(self):
        """get draw mode string.

        \return draw mode string"""

        dmstr = DrawMode.get_drawmode_string(self.get_drawmode())
        return dmstr

    #------------------------------------------------------------
    # Observer/Listener
    #------------------------------------------------------------

    def get_subject(self):
        """get Listener's Subject for node state change.
        \return node subject
        """
        return self.__observer_subject


    #------------------------------------------------------------
    # configurable
    #------------------------------------------------------------

    def set_config_dict(self, _config_dict):
        """set configuration dictionary. (configSetData)
        \param[in] _config_dict configuration dictionary
        """
        raise StandardError('not reimplemented')

    def get_config_dict(self):
        """get configuration dictionary. (configGetData)
        \return configuration dictionary
        """
        raise StandardError('not reimplemented')


    #------------------------------------------------------------

    # DELETEME Used?
    def print_glnodeinfo(self, _level):
        """print glnode info. Indentation is according to the depth level

        \param[in] _level node depth level"""

        indent = '  ' * _level
        out_str = indent + '+ ' + self.get_classname() + ' '
        if self.has_node_bbox():
            out_str += 'Bbox: '
            if self.get_bbox().has_volume():
                out_str += str(self.get_bbox()) + ' '
            else:
                out_str += 'invalid volume '
        else:
            out_str += 'no bbox '


        out_str += str(len(self.get_children())) + ' children '
        print out_str


    #------------------------------------------------------------

    def enter(self):
        """enter draw. Prologue of the draw()
        Usually set up for draw. E.g., save the OpenGL states.
        """
        # print 'enter', self.get_classname()
        pass


    def leave(self):
        """leave draw. Epilogue of the draw()
        Usually clean up after draw. E.g., pop the OpenGL states.
        """
        # print 'leave', self.get_classname()
        pass


    def draw(self, _global_mode):
        """draw by mode

        \param[in] _global_mode global draw mode
        \see DrawMode"""

        # print 'empty draw()', self.get_classname(), self.get_nodename()
        pass


    def get_drawmode_list(self):
        """get draw mode of this GLSceneGraphNode

        \return return __drawmode_list, maybe None"""

        if (self.is_primitive_node()):
            return self.get_primitive().get_drawmode_list()

        return None
        # raise StandardError, (
        # 'GLSceneGraphNode.get_drawmode_list() must be implemented ' +
        # 'in derived class. classname = ' + self.get_classname())


    def get_info_html_GLSceneGraphNode(self):
        """get GLSceneGraphNode base info html text.
        \return base GL node info."""

        ret_s = '<h2>GLSceneGraphNode information</h2>\n' +\
            '<h2>General information</h2>\n' +\
            '<ul>\n' +\
            '  <li><b>Class name:</b> ' + self.get_classname()    + '\n' +\
            '  <li><b>Name:</b> '       + self.get_nodename()     + '\n' +\
            '  <li><b>Status:</b> '     + self.get_active_state() + '\n' +\
            '  <li><b>Drawmode:</b> '   + self.get_drawmode_str() + '\n'

        if self.has_node_bbox():
            ret_s += '  <li><b>bbox:</b> '
            if self.get_bbox().has_volume():
                ret_s += str(self.get_bbox()) + '\n'
            else:
                ret_s += 'invalid (no volume)' + '\n'
        else:
            ret_s += '  <li>no bbox\n'

        ret_s += '</ul>\n'

        # print 'DEBUG: get_info_html_GLSceneGraphNode\n' + ret_s

        return ret_s


    def get_info_html(self):
        """Get information html text.
        Usually, this should be overrided.
        \return base GL node info.
        """
        ret_s = self.get_info_html_GLSceneGraphNode()

        return ret_s


    def create_config_dialog(self, _tab_dialog):
        """Create configuration dialog.
        The configuration dialog is QtSimpleTabDialog.

        Design decision: Only this method in the GLSceneGraph depends
        on Qt. I could make this independent from the Qt by a domain
        specific GUI creation language and pass it as a string. But,
        that would be a small scripting language. The advantage of
        PyQt is the GUI creation scripting language. Making another
        language is not necessary. Therefore, I think this dependency
        is fine.

        \param[in] _tab_dialog a QtSimpleTabDialog
        \return True when there are some configuration. False when no
        configuration is needed for this node.
        """
        QtCore.qWarning('GLSceneGraphNode.create_config_dialog() is empty. ' +
                        'No configuration for this GLSceneGraphNode.')
        return False

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

# ----------------------------------------------------------------------

class GLCameraNode(GLSceneGraphNode, QtWidgetIO.QtWidgetIOObserverIF):
    """OpenGL camera node.

    This is a scene graph node. also QtWidgetIOObserver, means Qt GUI
    can change this state.
    """

    # default constructor
    def __init__(self, _sg_camnode):
        """constructor.
        GLCamara is created with _sg_camnode parameters.
        scenegraph camera and gl camera are not synchronized,
        when sync is needed, this should be done explicitly.

        \param[in] _sg_camnode scenegraph camera node.
        """
        # 2011-2-28(Mon) Hitoshi
        #
        # Use super. I made a mistake here to call directry,
        #
        # SceneGraph.SceneGraphNode.__init__(self,
        #                                    _sg_camnode.get_nodename())
        #
        # and this is not a real super class of this. In that case,
        # all the attribute (member) of the super class are not
        # created, then you can not call many of the members. Because,
        # for example, there is no self.__is_active attribute that is
        # created super class's __init__().
        super(GLCameraNode, self).__init__(_sg_camnode.get_nodename())

        # here new the GLCamera and own this camera.
        self.__gl_camera = Camera.GLCamera()
        # keep the reference to the scenegraph camera
        self.__ifgi_camera_ref = _sg_camnode.get_camera()
        self.__gl_camera.set_camera_param(self.__ifgi_camera_ref)

        # updated subject name (Observer/Listener)
        self.get_subject().set_subject_name('GLCameraNode')


    def get_gl_camera(self):
        """get gl camera of this node.
        \return gl camera."""
        return self.__gl_camera


    def get_classname(self):
        """get classname (shown in the SceneGraph viewer as node Type)
        Inherited from GLSceneGraphNode
        \return class name"""

        return 'GLCameraNode'

    # draw by mode
    def draw(self, _global_mode):
        """draw by mode. Camera ignore this.
        Inherited from GLSceneGraphNode
        No children
        """
        pass

    # get draw mode of this GLCameraNode
    def get_drawmode_list(self):
        """get draw mode of GLCameraNode. Camera has no draw mode.
        Inherited from GLSceneGraphNode
        \return None"""
        return None

    # get info of this node
    def get_info_html_GLCameraNode(self):
        """get GLCameraNode base info html text.
        Inherited from GLSceneGraphNode
        \return base GL node info."""

        ret_s = '<h2>GLCameraNode information</h2>\n' +\
            '<h2>General information</h2>\n' +\
            '<ul>\n' +\
            '  <li><b>Class name:</b> ' + self.get_classname()    + '\n' +\
            '  <li><b>Name:</b> '       + self.get_nodename()     + '\n' +\
            '  <li><b>Status:</b> '     + self.get_active_state() + '\n' +\
            '  <li><b>Drawmode:</b> '   + self.get_drawmode_str() + '\n' +\
            '</ul>\n'

        return ret_s


    def get_info_html(self):
        """Get information html text.
        Inherited from GLSceneGraphNode
        Usually, this should be overrided.
        \return base GL node info.
        """
        ret_s = self.get_info_html_GLCameraNode() +\
            self.__gl_camera.get_html_info()

        return ret_s

    def create_config_dialog(self, _tab_dialog):
        """Create configuration dialog for GLCameraNode.
        The configuration dialog is QtSimpleTabDialog.
        Inherited from GLSceneGraphNode

        \param[in] _tab_dialog a QtSimpleTabDialog
        \return True since this node is configurable.
        """

        cam_group = _tab_dialog.add_group('Camera')

        keylist  = self.__gl_camera.get_param_key()
        valdict  = self.__gl_camera.get_config_dict()
        typedict = self.__gl_camera.get_typename_dict()

        for key in keylist:
            typename = typedict[key]
            if((typename == 'float_3') or (typename == 'float')):
                cam_group.add(QtWidgetIO.QtLineEditWIO(),
                              key,
                              valdict[key],
                              {'LABEL': key})
            elif typename == 'enum_ProjectionMode':
                itemlist = Camera.ProjectionMode[:]
                cam_group.add(QtWidgetIO.QtComboBoxWIO(),
                              key,
                              str(valdict[key]),
                              {'LABEL': key, 'ITEMS': itemlist})
            else:
                raise StandardError('unknown typename for camera parameter.')

        # call self.update() when button is pushed (_arg is button type)
        _tab_dialog.set_button_observer(self)
        # call set_config_dict(dict) when apply button is pushed.
        _tab_dialog.set_associated_configuable_object('Camera', self)

        # set node (which has get_subject() attribute to get the
        # Listener's subject. This subject notify dialog when node
        # status is changed.
        _tab_dialog.set_subject_node(self)

        return True

    def update(self, _arg):
        """Implementation of QtWidgetIOObserverIF.update().
        """
        print 'GLCameraNode: I observe ' + _arg

    #------------------------------------------------------------
    # configurable
    #------------------------------------------------------------

    def set_config_dict(self, _config_dict):
        """set configuration dictionary. (configSetData)
        \param[in] _config_dict configuration dictionary
        """
        self.__gl_camera.set_config_dict(_config_dict)
        self.get_subject().notify_listeners(['ConfigChanged'])

    def get_config_dict(self):
        """get configuration dictionary. (configGetData)
        \return configuration dictionary
        """
        return self.__gl_camera.get_config_dict()


# ----------------------------------------------------------------------

class GLLightParameter(object):
    """OpenGL light parameter used in GLLightNode.
    This is not a scenegraph node.
    """

    def __init__(self,  _is_on, _light_id_num, _amb, _dif, _spec, _pos):
        """default constructor for OpenGL light.
        Point light only.
        The parameters are all public.
        \param[in] _is_on boolean when true the light is on
        \param[in] _light_id_num light id index number. must be [0,7]
        \param[in] _amp          ambient light intensity
        \param[in] _dif          diffuse light intensity
        \param[in] _spec         specular light intensity
        \param[in] _pos          light position (float 4)
        """
        # call base class constructor to fill the members
        super(GLLightParameter, self).__init__()

        # OpenGL light ID (GL_LIGHT0, ..., GL_LIGHT7)
        assert((_light_id_num >= 0) and (_light_id_num < 8))
        self.__gl_light_sym_list = [GL.GL_LIGHT0, GL.GL_LIGHT1, GL.GL_LIGHT2,
                                    GL.GL_LIGHT3, GL.GL_LIGHT4, GL.GL_LIGHT5,
                                    GL.GL_LIGHT6, GL.GL_LIGHT7 ]

        self.gl_light_id = self.__gl_light_sym_list[_light_id_num]
        self.is_light_on = _is_on
        self.ambient  = _amb
        self.diffuse  = _dif
        self.specular = _spec
        self.position = _pos


# ----------------------------------------------------------------------

class GLLightNode(GLSceneGraphNode):
    """OpenGL Light node.
    This is OpenGL only. These are default lights for OpenGL.
    This node has max 8 lights (OpenGL lights), 3 are on at default.
    """

    def __init__(self, _nodename):
        """default constructor.
        \param[in] _nodename this node name."""
        # call base class constructor to fill the members
        super(GLLightNode, self).__init__(_nodename)
        self.__drawmode_list = DrawMode.DrawModeList()
        # basic draw mode only
        self.__drawmode_list.add_basic_drawmode()

        # light default parameter (same as the Mathematica light)
        sqrt3 = math.sqrt(3.0)
        on_off = [True, True, True, True, False, False, False, False]
        amb_intensity     = numpy.array([0.1, 0.1, 0.1, 1.0]) # all the same
        diffuse_intensity = [
            numpy.array([0.8, 0.5, 0.5, 1.0]), # 0
            numpy.array([0.5, 0.8, 0.5, 1.0]), # 1
            numpy.array([0.5, 0.5, 0.8, 1.0]), # 2
            numpy.array([0.5, 0.5, 0.5, 1.0]), # 3
            numpy.array([0.5, 0.5, 0.5, 1.0]), # 4
            numpy.array([0.5, 0.5, 0.5, 1.0]), # 5
            numpy.array([0.5, 0.5, 0.5, 1.0]), # 6
            numpy.array([0.5, 0.5, 0.5, 1.0]) ] # 7
        specular_intensity = numpy.array([0.8, 0.8, 0.8, 1.0]) # all the same
        pos = [
            numpy.array([ 0.0,  2.0,    0.0, 0.0]), # 0
            numpy.array([-2.0,  1.0, -sqrt3, 0.0]), # 1
            numpy.array([ 2.0, -1.0, -sqrt3, 0.0]), # 2
            numpy.array([ 0.0, -1.0,  sqrt3, 0.0]), # 3
            numpy.array([ 0.0,  0.0,    0.0, 0.0]), # 4
            numpy.array([ 0.0,  0.0,    0.0, 0.0]), # 5
            numpy.array([ 0.0,  0.0,    0.0, 0.0]), # 6
            numpy.array([ 0.0,  0.0,    0.0, 0.0]) ] # 7

        # create 8 OpenGL lights
        self.__light_list = []
        for i in range(0, 8):
            lp = GLLightParameter(on_off[i],
                                  i,
                                  amb_intensity,
                                  diffuse_intensity[i],
                                  specular_intensity,
                                  pos[i])
            self.__light_list.append(lp)

        # light status (for all GL lights)
        # push state
        self.__pushed_light_node_lighting_state = GL.GL_TRUE
        # node state
        self.__is_light_node_lighting_on = GL.GL_TRUE


    def get_classname(self):
        """get classname
        Inherited from GLSceneGraphNode
        \return class name string"""

        return 'GLLightNode'

    # enter, leave, draw ----------------------------------------

    def enter(self):
        """enter the GLLight node
        Set up all the lights.
        """
        if (not self.is_node_active()):
            # node is deactivated, not call draw anymore
            return

        # push the current GL lighting state.
        # This is global effect, not for children in current implementation.
        self.__pushed_light_node_lighting_state = GL.glIsEnabled(GL.GL_LIGHTING)

        # set node state to GL
        self.gl_enable_disable(GL.GL_LIGHTING, self.__is_light_node_lighting_on)

        # set parameter for each light
        for li in self.__light_list:
            if (li.is_light_on == True):
                GL.glEnable(li.gl_light_id)
                GL.glLightfv(li.gl_light_id, GL.GL_AMBIENT,  li.ambient)
                GL.glLightfv(li.gl_light_id, GL.GL_DIFFUSE,  li.diffuse)
                GL.glLightfv(li.gl_light_id, GL.GL_SPECULAR, li.specular)
                GL.glLightfv(li.gl_light_id, GL.GL_POSITION, li.position)
            else:
                GL.glDisable(li.gl_light_id)


    def leave(self):
        """leave draw. Epilogue of the draw()
        Usually clean up after draw. E.g., pop the OpenGL states.
        """
        if (not self.is_node_active()):
            # node is deactivated, not call draw anymore
            return

        # pop the current GL state
        self.gl_enable_disable(GL.GL_LIGHTING, self.__pushed_light_node_lighting_state)


    def draw(self, _global_drawmode):
        """draw the lights.
        If node is deactivated, draw nothing.
        \param[in] _global_drawmode drawmode list ignored in this node.
        """

        if (not self.is_node_active()):
            # node is deactivated, not call draw anymore
            return


    def get_drawmode_list(self):
        """get draw mode list.
        GL Light Node shows the light position and color with a box if specified.
        Inherited from GLSceneGraphNode
        \return node drawmode (default DrawMode.DrawModeList.DM_GlobalMode)
        """
        return self.__drawmode_list


    def __draw_points(self):
        """draw light with points"""
        # NIN
        pass

    def __draw_wireframe(self):
        """draw light with wireframe"""
        # NIN
        GL.glShadeModel(GL.GL_FLAT)


    def __draw_solid_basecolor(self):
        """draw light with solid_basecolor"""
        # NIN
        GL.glDisable(GL.GL_LIGHTING)
        GL.glShadeModel(GL.GL_FLAT)
        GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL);
        GL.glBegin(GL.GL_TRIANGLES)
        vp = self.get_primitive().vertex_list
        for face in self.get_primitive().face_idx_list:
            GL.glVertex3d(vp[face[0]][0], vp[face[0]][1], vp[face[0]][2])
            GL.glVertex3d(vp[face[1]][0], vp[face[1]][1], vp[face[1]][2])
            GL.glVertex3d(vp[face[2]][0], vp[face[2]][1], vp[face[2]][2])
        GL.glEnd()


    # get info of this node
    def get_info_html(self):
        """Get information html text.
        Inherited from GLSceneGraphNode
        \return base GL node info + GLLightNode info
        """
        light_desc = '<h2>GLLightNode information</h2>\n' +\
            '<ul>\n' +\
            '  <li><b>Lighting:</b> ' + str(self.__is_light_node_lighting_on)\
            + '\n' + '</ul>\n'

        for lidx in range(0, 8):
            # for each light information
            li = self.__light_list[lidx]
            light_desc = light_desc +\
                '<h3>GL_LIGHT' +  str(lidx) + '</h3>\n'
            if li.is_light_on == False:
                light_desc = light_desc +\
                    '<ul>\n' +\
                    '  <li><b>Light:</b> off\n' +\
                    '</ul>\n'
            else:
                light_desc = light_desc +\
                    '<ul>\n' +\
                    '  <li><b>Light:</b>    on\n' +\
                    '  <li><b>ambient:</b>  '     +\
                    numpy_util.array2str(li.ambient)  + '\n' +\
                    '  <li><b>diffuse:</b>  '     +\
                    numpy_util.array2str(li.diffuse)  + '\n' +\
                    '  <li><b>specular:</b> '     +\
                    numpy_util.array2str(li.specular) + '\n' +\
                    '  <li><b>position:</b> '     +\
                    numpy_util.array2str(li.position) + '\n' +\
                    '</ul>\n'

        ret_s = self.get_info_html_GLSceneGraphNode() + light_desc

        return ret_s

    def create_config_dialog(self, _tab_dialog):
        """Create configuration dialog for GLLightNode.
        The configuration dialog is QtSimpleTabDialog.
        Inherited from GLSceneGraphNode

        \param[in] _tab_dialog a QtSimpleTabDialog
        \return True since this node is configurable.
        """

        light_root_group = _tab_dialog.add_group('GLLightNode')

        lighting_on = (True if(self.__is_light_node_lighting_on == GL.GL_TRUE) else False)

        light_root_group.add(QtWidgetIO.QtToggleButton(),
                             'light_enable',
                             lighting_on,
                             {'LABEL': 'GLLightNode: lighting on'})

        for lidx in range(0, 8):
            # for each light source
            lidxstr = str(lidx)
            light_group_name = 'L_' + lidxstr
            light_lidx_group = _tab_dialog.add_group(light_group_name)
            li = self.__light_list[lidx]
            light_lidx_group.add(QtWidgetIO.QtToggleButton(),
                                 'light_on_' + lidxstr,
                                 li.is_light_on,
                                 {'LABEL': 'Light_' + lidxstr + ' on'})
            light_lidx_group.add(QtWidgetIO.QtColorButton(),
                                 'ambient_' + lidxstr,
                                 li.ambient,
                                 {'LABEL': 'Ambient'})
            light_lidx_group.add(QtWidgetIO.QtColorButton(),
                                 'diffuse_' + lidxstr,
                                 li.diffuse,
                                 {'LABEL': 'Diffuse'})
            light_lidx_group.add(QtWidgetIO.QtColorButton(),
                                 'specular_' + lidxstr,
                                 li.specular,
                                 {'LABEL': 'Specular'})
            light_lidx_group.add(QtWidgetIO.QtLineEditWIO(),
                                 'position_' + lidxstr,
                                 numpy_util.array2str(li.position),
                                 {'LABEL': 'Position'})
            # tab is configurable: submit the tab group name
            _tab_dialog.set_associated_configuable_object(light_group_name, self)

        # call self.update() when button is pushed (_arg is button type)
        _tab_dialog.set_button_observer(self)
        # call set_config_dict(dict) when apply button is pushed.
        _tab_dialog.set_associated_configuable_object('GLLightNode', self)

        # set node (which has get_subject() attribute to get the
        # Listener's subject. This subject notify dialog when node
        # status is changed.
        _tab_dialog.set_subject_node(self)

        return True

    def update(self, _arg):
        """Implementation of QtWidgetIOObserverIF.update().
        """
        print 'GLLightNode: I observe ' + _arg

    #------------------------------------------------------------
    # configurable
    #------------------------------------------------------------

    def set_config_dict(self, _config_dict):
        """set configuration dictionary. (configSetData)
        \param[in] _config_dict configuration dictionary
        """
        # get one of the tab's config
        if _config_dict.has_key('light_enable'):
            # GLLightNode tab
            self.__is_light_node_lighting_on = \
                (GL.GL_TRUE if(_config_dict['light_enable'] == True) else GL.GL_FALSE)
        else:
            # each light tab
            for lidx in range(0, 8):
                lidxstr = str(lidx)
                if ('light_on_' + lidxstr) in _config_dict:
                    self.__light_list[lidx].is_light_on =\
                        _config_dict['light_on_' + lidxstr]
                    self.__light_list[lidx].ambient  = _config_dict['ambient_' + lidxstr]
                    self.__light_list[lidx].diffuse  = _config_dict['diffuse_' + lidxstr]
                    self.__light_list[lidx].specular = _config_dict['specular_'+ lidxstr]
                    self.__light_list[lidx].position =\
                        numpy_util.str2array(_config_dict['position_' + lidxstr])
                    break

        self.get_subject().notify_listeners(['ConfigChanged'])


    def get_config_dict(self):
        """get configuration dictionary. (configGetData)
        \return configuration dictionary
        """
        config_dict =\
            { 'light_enable': (True if (self.__is_light_node_lighting_on == GL.GL_TRUE)
                               else False) }

        # for all light sources
        for lidx in range(0, 8):
            lidxstr = str(lidx)
            li = self.__light_list[lidx]
            opt['light_on_' + lidxstr] = li.is_light_on
            opt['ambient_'  + lidxstr] = li.ambient
            opt['diffuse_'  + lidxstr] = li.diffuse
            opt['specular_' + lidxstr] = li.specular
            opt['position_' + lidxstr] = numpy_util.array2str(li.position)

        return opt


# ----------------------------------------------------------------------

class GLMaterialNode(GLSceneGraphNode):
    """OpenGL MaterialNode

    A OpenGL material node"""

    # default constructor
    def __init__(self, _nodename):
        """default constructor.
        \param[in] _nodename this node name.
        """
        # call base class constructor to fill the members
        super(GLMaterialNode, self).__init__(_nodename)

        # ifgi material (non OpenGL material)
        self.__ifgi_mat = None

        # OpenGL push state
        self.__push_current_color = numpy.array([1.0, 1.0, 1.0, 1.0])
        self.__fg_color           = numpy.array([1.0, 1.0, 1.0, 1.0])
        self.__push_emission      = numpy.array([0.0, 0.0, 0.0, 1.0])
        self.__push_diffuse       = numpy.array([0.5, 0.5, 0.5, 1.0])
        self.__push_ambient       = numpy.array([0.2, 0.2, 0.2, 1.0])
        self.__push_specular      = numpy.array([0.2, 0.2, 0.2, 1.0])
        self.__push_shininess     = 1.0

        self.__emission  = numpy.array([0.0, 0.0, 0.0, 1.0])
        self.__diffuse   = numpy.array([0.5, 0.5, 0.5, 1.0])
        self.__ambient   = numpy.array([0.2, 0.2, 0.2, 1.0])
        self.__specular  = numpy.array([0.2, 0.2, 0.2, 1.0])
        self.__shininess = 1.0


    # get classname
    def get_classname(self):
        """get classname

        \return class name string"""

        return 'GLMaterialNode'

    # get draw mode of this GLSceneGraphNode
    def get_drawmode_list(self):
        """get draw mode list of this GLSceneGraphNode
        \return None. Material node has no drawmode list
        """
        return None


    # enter, leave, draw ----------------------------------------

    def enter(self):
        """enter draw. Prologue of the draw()
        Usually set up for draw. E.g., save the OpenGL states.
        """
        self.__push_current_color = GL.glGetFloatv(GL.GL_CURRENT_COLOR)
        GL.glColor4fv(self.__fg_color)

        # FIXME: do we need GL_BACK and GL_FRONT_AND_BACK also?
        # then put them in an array.
        self.__push_emission  = GL.glGetMaterialfv(GL.GL_FRONT, GL.GL_EMISSION)
        self.__push_diffuse   = GL.glGetMaterialfv(GL.GL_FRONT, GL.GL_DIFFUSE)
        self.__push_ambient   = GL.glGetMaterialfv(GL.GL_FRONT, GL.GL_AMBIENT)
        self.__push_specular  = GL.glGetMaterialfv(GL.GL_FRONT, GL.GL_SPECULAR)
        self.__push_shininess = GL.glGetMaterialfv(GL.GL_FRONT, GL.GL_SHININESS)

        GL.glMaterialfv(GL.GL_FRONT, GL.GL_EMISSION,  self.__emission)
        GL.glMaterialfv(GL.GL_FRONT, GL.GL_DIFFUSE,   self.__diffuse)
        GL.glMaterialfv(GL.GL_FRONT, GL.GL_AMBIENT,   self.__ambient)
        GL.glMaterialfv(GL.GL_FRONT, GL.GL_SPECULAR,  self.__specular)
        GL.glMaterialf (GL.GL_FRONT, GL.GL_SHININESS, self.__shininess)

        # if (d_applyProperties&PointSize):
        #     glGetFloatv(GL_POINT_SIZE,&d_bakPointSize)
        #     glPointSize(d_pointSize)

        # if (d_applyProperties&LineWidth):
        #     glGetFloatv(GL_LINE_WIDTH,&d_bakLineWidth)
        #     glLineWidth(d_lineWidth)


        # if (d_applyProperties&LineStipple):
        #     d_bakLineStippleIsEnabled=glIsEnabled(GL_LINE_STIPPLE);
        #     glGetIntegerv(GL_LINE_STIPPLE_PATTERN,&d_bakLineStipplePattern);
        #     glGetIntegerv(GL_LINE_STIPPLE_REPEAT,&d_bakLineStippleFactor);

        #     if (d_lineStippleFactor>0):
        #         if (!d_bakLineStippleIsEnabled):
        #             glEnable(GL_LINE_STIPPLE);
        #             glLineStipple(d_lineStippleFactor,d_lineStipplePattern);

        # if (d_applyProperties & (LineAntialiasing | PointAntialiasing)):
        #     if (d_lineAntialiasing || d_pointAntialiasing):
        #         d_bakAlphaBuffer = glIsEnabled(GL_ALPHA_TEST);

        # glEnable(GL_BLEND);
        # glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

        # if (d_applyProperties&LineAntialiasing):
        #     d_bakLineAntialiasing=glIsEnabled(GL_LINE_SMOOTH);
        #     if (d_lineAntialiasing):
        #         glEnable(GL_LINE_SMOOTH);
        #     else:
        #         glDisable(GL_LINE_SMOOTH);

        # if (d_applyProperties&PointAntialiasing):
        #     d_bakPointAntialiasing=glIsEnabled(GL_POINT_SMOOTH)
        #     if (d_pointAntialiasing):
        #         glEnable(GL_POINT_SMOOTH);
        #     else:
        #         glDisable(GL_POINT_SMOOTH)

        # glGetBooleanv(GL_LIGHT_MODEL_TWO_SIDE, &d_curGlLightModelTwoSide)
        # glLightModeli(GL_LIGHT_MODEL_TWO_SIDE, GL_FALSE)

        # # polygon mode
        # if(d_polygonMode_FaceType != PM_FaceType_FOLLOW_OPENGL_STAT):
        #     // push the current mode
        #     // NOTICE:
        #     // glGetIntegerv(GL_POLYGON_MODE, ..) did not return the correct
        #     // paranmeter on d_pushedGLPolygonMode[0].
        #     // So we use only d_pushedGLPolygonMode[1].
        #     glGetIntegerv(GL_POLYGON_MODE, d_pushedGLPolygonMode);

        #     GLenum polymode[2] = { GL_FRONT, GL_FILL, };
        #     if(d_polygonMode_FaceType == PM_FaceType_FRONT):
        #         polymode[0] = GL_FRONT;
        #     elif(d_polygonMode_FaceType == PM_FaceType_BACK):
        #         polymode[0] = GL_BACK;
        #     elif(d_polygonMode_FaceType == PM_FaceType_FRONT_AND_BACK):
        #         polymode[0] = GL_FRONT_AND_BACK;
        #     else:
        #         'Error! MaterialNode::enter: No such polygon mode face type. '
	# 	'use default.'

        #     if(d_polygonMode_RasterMode == PM_RasterMode_POINT):
        #         polymode[1] = GL_POINT
        #     elif(d_polygonMode_RasterMode == PM_RasterMode_LINE):
        #         polymode[1] = GL_LINE
        #     elif (d_polygonMode_RasterMode == PM_RasterMode_FILL):
        #         polymode[1] = GL_FILL;
        #     else:
        #         'Error! MaterialNode::enter: No such polygon mode raster type. '
	# 	'use default. '

        #     glPolygonMode(polymode[0], polymode[1])

        # // culling mode
        # if(d_cullFaceMode != CullFaceMode_FOLLOW_OPENGL_STATE):
        #     // push the current mode
        #     d_pushedGLCullFaceEnable = glIsEnabled(GL_CULL_FACE)
        #     glGetIntegerv(GL_CULL_FACE_MODE, &d_pushedGLCullFaceMode)

        # if(d_cullFaceMode == CullFaceMode_Enable):
        #     glEnable(GL_CULL_FACE);
        # elif(d_cullFaceMode == CullFaceMode_Disable):
        #     glDisable(GL_CULL_FACE);
        # else:
        #     'Error! MaterialNode::enter: No such cull face mode. '
        #     'use default. '

        # if(d_cullFaceType == CullFaceType_FRONT):
        #     glCullFace(GL_FRONT);
        # elif(d_cullFaceType == CullFaceType_BACK):
        #     glCullFace(GL_BACK);
        # elif(d_cullFaceType == CullFaceType_FRONT_AND_BACK):
        #     glCullFace(GL_FRONT_AND_BACK);
        # else:
        #     'Error! MaterialNode::enter: No such cull face type. '



    def leave(self):
        """leave draw. Epilogue of the draw()
        Usually clean up after draw. E.g., pop the OpenGL states.
        """
        GL.glColor4fv(self.__push_current_color)

        # if (d_applyProperties&Material)

        GL.glMaterialfv(GL.GL_FRONT, GL.GL_DIFFUSE,    self.__push_diffuse)
        GL.glMaterialfv(GL.GL_FRONT, GL.GL_EMISSION,   self.__push_emission)
        GL.glMaterialfv(GL.GL_FRONT, GL.GL_AMBIENT,    self.__push_ambient)
        GL.glMaterialfv(GL.GL_FRONT, GL.GL_SPECULAR,   self.__push_specular)
        GL.glMaterialf (GL.GL_FRONT, GL.GL_SHININESS,  self.__push_shininess)

        # if (d_applyProperties&PointSize):
        #     glPointSize(d_bakPointSize);

        # if (d_applyProperties&LineWidth):
        #     glLineWidth(d_bakLineWidth);

        # if (d_applyProperties&LineStipple):
        #     if (d_lineStippleFactor>0):
        #         if (!d_bakLineStippleIsEnabled):
        #             glDisable(GL_LINE_STIPPLE);
        #         glLineStipple(d_bakLineStippleFactor,d_bakLineStipplePattern);

        # if (d_applyProperties & (LineAntialiasing | PointAntialiasing)):
        #     if (d_lineAntialiasing || d_pointAntialiasing):
        #         if (d_bakAlphaBuffer):
        #             glEnable(GL_ALPHA_TEST)
        #         else:
        #             glDisable(GL_ALPHA_TEST)
        #             //!! does not reconstruct AlphaFunc

        # if (d_applyProperties&LineAntialiasing):
        #     if (d_bakLineAntialiasing):
        #         glEnable(GL_LINE_SMOOTH);
        #     else:
        #         glDisable(GL_LINE_SMOOTH)

        # if (d_applyProperties&PointAntialiasing):
        #     if (d_bakPointAntialiasing):
        #         glEnable(GL_POINT_SMOOTH);
        #     else:
        #         glDisable(GL_POINT_SMOOTH);

        # glLightModeli(GL_LIGHT_MODEL_TWO_SIDE, d_curGlLightModelTwoSide);

        # if(d_polygonMode_FaceType != PM_FaceType_FOLLOW_OPENGL_STAT):
        #     // glGetIntegerv(GL_POLYGON_MODE, ..) did not get correct parameter.
        #     // So, this is workaround.
        #     // glPolygonMode(d_pushedGLPolygonMode[0], d_pushedGLPolygonMode[1]);
        #     glPolygonMode(GL_FRONT_AND_BACK, d_pushedGLPolygonMode[1]);

        # if(d_cullFaceMode != CullFaceMode_FOLLOW_OPENGL_STATE):
        #     if(d_pushedGLCullFaceEnable == GL_TRUE):
        #         glEnable(GL_CULL_FACE);
        #     else:
        #         glDisable(GL_CULL_FACE)
        #     glCullFace(d_pushedGLCullFaceMode);

        # this->checkGLError();


    def draw(self, _global_drawmode):
        """material node does nothing in draw.
        \param[in] _global_drawmode drawmode list (or-ed drawmode list bitmap)."""
        pass


    def get_info_html(self):
        """Get information html text.
        Inherited from GLSceneGraphNode
        \return GL materal node info
        """
        mat_info = self.get_info_html_GLSceneGraphNode() +\
            '<h2>GLMaterialNode information</h2>\n' +\
            '<ul>\n' +\
            '  <li><b>FG color:</b> ' +\
            numpy_util.array2str(self.__fg_color)  + '\n' +\
            '  <li><b>emission:</b> ' +\
            numpy_util.array2str(self.__emission)  + '\n' +\
            '  <li><b>diffuse:</b> ' +\
            numpy_util.array2str(self.__diffuse)  + '\n' +\
            '  <li><b>ambient:</b> ' +\
            numpy_util.array2str(self.__ambient)  + '\n' +\
            '  <li><b>specular:</b> ' +\
            numpy_util.array2str(self.__specular)  + '\n' +\
            '  <li><b>shininess:</b> ' +\
            str(self.__shininess)  + '\n' +\
            '</ul>\n'

        return mat_info


    def create_config_dialog(self, _tab_dialog):
        """Create configuration dialog for GLMaterialNode.
        The configuration dialog is QtSimpleTabDialog.
        Inherited from GLSceneGraphNode

        \param[in] _tab_dialog a QtSimpleTabDialog
        \return True since this node is configurable.
        """

        mat_group = _tab_dialog.add_group('GLMaterialNode')

        mat_group.add(QtWidgetIO.QtColorButton(),
                      'fg_color',
                      self.__fg_color,
                      {'LABEL': 'FG color'})
        mat_group.add(QtWidgetIO.QtColorButton(),
                      'emission',
                      self.__emission,
                      {'LABEL': 'emission'})
        mat_group.add(QtWidgetIO.QtColorButton(),
                      'diffuse',
                      self.__diffuse,
                      {'LABEL': 'diffuse'})
        mat_group.add(QtWidgetIO.QtColorButton(),
                      'ambient',
                      self.__ambient,
                      {'LABEL': 'ambient'})
        mat_group.add(QtWidgetIO.QtColorButton(),
                      'specular',
                      self.__specular,
                      {'LABEL': 'specular'})
        mat_group.add(QtWidgetIO.QtLineEditWIO(),
                      'shininess',
                      str(self.__shininess),
                      {'LABEL': 'shininess',
                       'TOOLTIP': 'shininess (power) valid range [1,128]'})

        # call self.update() when button is pushed (_arg is button type)
        _tab_dialog.set_button_observer(self)
        # call set_config_dict(dict) when apply button is pushed.
        _tab_dialog.set_associated_configuable_object('GLMaterialNode', self)

        # set node (which has get_subject() attribute to get the
        # Listener's subject. This subject notify dialog when node
        # status is changed.
        _tab_dialog.set_subject_node(self)

        return True

    def update(self, _arg):
        """Implementation of QtWidgetIOObserverIF.update().
        """
        print 'GLMaterialNode: I observe ' + _arg

    #------------------------------------------------------------
    # configurable
    #------------------------------------------------------------

    def set_config_dict(self, _config_dict):
        """set configuration dictionary. (configSetData)
        \param[in] _config_dict configuration dictionary for GLMaterialNode
        """
        self.__fg_color  = _config_dict['fg_color']
        self.__emission  = _config_dict['emission']
        self.__diffuse   = _config_dict['diffuse']
        self.__ambient   = _config_dict['ambient']
        self.__specular  = _config_dict['specular']
        self.__shininess = float(_config_dict['shininess'])

        if self.__shininess < 0:
            ILog.error('shininess should be >= 0. set to 0.')
            self.__shininess = 0
        if self.__shininess > 128:
            ILog.error('shininess should be <= 128 0. set to 128.')
            self.__shininess = 128

        # NIN: FIXME. Update the real material not only OpenGL's material

        self.get_subject().notify_listeners(['ConfigChanged'])


    def get_config_dict(self):
        """get configuration dictionary. (configGetData)
        \return configuration dictionary of GLMaterialNode
        """
        config_dict = {'fg_color':  self.__fg_color,
                       'emission':  self.__emission,
                       'diffuse':   self.__diffuse,
                       'ambient':   self.__ambient,
                       'specular':  self.__specular,
                       'shininess': str(self.__shininess)} # LineEdit need str()
        return config_dict


    #------------------------------------------------------------
    # ifgi material
    #------------------------------------------------------------

    def set_material(self, _mat):
        """set ifgi material
        \param[in] _mat ifgi material
        """
        self.__ifgi_mat = _mat
        preview_dict = self.__ifgi_mat.get_gl_preview_dict()
        # print preview_dict
        self.set_config_dict(preview_dict)

# ----------------------------------------------------------------------

class GLEnvironmentMaterialNode(GLSceneGraphNode):
    """OpenGL EnvironmentMaterialNode

    A OpenGL environment material node
    FIXME currently only support constant color environment."""

    def __init__(self, _nodename):
        """default constructor.
        \param[in] _nodename this node name.
        """
        # call base class constructor to fill the members
        super(GLEnvironmentMaterialNode, self).__init__(_nodename)

        # ifgi material (non OpenGL material)
        self.__ifgi_mat = None

        # OpenGL push state
        self.__push_clear_color  = numpy.array([0.0, 0.0, 0.0, 1.0])

        # constant background color (for constant color background)
        self.__const_bg_color    = numpy.array([0.0, 0.0, 0.0, 1.0])


    def get_classname(self):
        """get classname

        \return class name string"""

        return 'GLEnvironmentMaterialNode'


    def get_drawmode_list(self):
        """get draw mode list of this GLSceneGraphNode
        \return None. Material node has no drawmode list
        """
        return None


    # enter, leave, draw ----------------------------------------

    def enter(self):
        """enter draw. Prologue of the draw()
        Usually set up for draw. E.g., save the OpenGL states.
        """
        self.__push_clear_color = GL.glGetFloatv(GL.GL_COLOR_CLEAR_VALUE)
        GL.glClearColor(self.__const_bg_color[0], self.__const_bg_color[1],
                        self.__const_bg_color[2], self.__const_bg_color[3])

        # really clear the color buffer. Because of this, this node
        # should be the first one to draw.
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)


    def leave(self):
        """leave draw. Epilogue of the draw()
        Usually clean up after draw. E.g., pop the OpenGL states.
        """
        GL.glClearColor(self.__push_clear_color[0], self.__push_clear_color[1],
                        self.__push_clear_color[2], self.__push_clear_color[3])


    def draw(self, _global_drawmode):
        """material node does nothing in draw.
        \param[in] _global_drawmode drawmode list (or-ed drawmode list bitmap)."""
        pass


    def get_info_html(self):
        """Get information html text.
        Inherited from GLSceneGraphNode
        \return GL materal node info
        """
        mat_info = self.get_info_html_GLSceneGraphNode() +\
            '<h2>GLEnvironmentMaterialNode information</h2>\n' +\
            '<ul>\n' +\
            '  <li><b>constant background color:</b> ' +\
            numpy_util.array2str(self.__const_bg_color)  + '\n' +\
            '</ul>\n'

        return mat_info


    def create_config_dialog(self, _tab_dialog):
        """Create configuration dialog for GLEnvironmentMaterialNode.
        The configuration dialog is QtSimpleTabDialog.
        Inherited from GLSceneGraphNode

        \param[in] _tab_dialog a QtSimpleTabDialog
        \return True since this node is configurable.
        """

        mat_group = _tab_dialog.add_group('GLEnvironmentMaterialNode')

        mat_group.add(QtWidgetIO.QtColorButton(),
                      'const_bg_color',
                      self.__const_bg_color,
                      {'LABEL': 'constant BG color'})

        # call self.update() when button is pushed (_arg is button type)
        _tab_dialog.set_button_observer(self)
        # call set_config_dict(dict) when apply button is pushed.
        _tab_dialog.set_associated_configuable_object('GLEnvironmentMaterialNode', self)

        # set node (which has get_subject() attribute to get the
        # Listener's subject. This subject notify dialog when node
        # status is changed.
        _tab_dialog.set_subject_node(self)

        return True

    def update(self, _arg):
        """Implementation of QtWidgetIOObserverIF.update().
        """
        print 'GLEnvironmentMaterialNode: I observe ' + _arg

    #------------------------------------------------------------
    # configurable
    #------------------------------------------------------------

    def set_config_dict(self, _config_dict):
        """set configuration dictionary. (configSetData)
        \param[in] _config_dict configuration dictionary for GLEnvironmentMaterialNode
        """
        self.__const_bg_color  = _config_dict['const_bg_color']
        self.get_subject().notify_listeners(['ConfigChanged'])


    def get_config_dict(self):
        """get configuration dictionary. (configGetData)
        \return configuration dictionary of GLEnvironmentMaterialNode
        """
        config_dict = {'const_bg_color':  self.__const_bg_color}
        return config_dict


    #------------------------------------------------------------
    # ifgi material
    #------------------------------------------------------------

    def set_material(self, _mat):
        """set ifgi material
        \param[in] _mat ifgi material
        """
        self.__ifgi_mat = _mat
        print self.__ifgi_mat.get_classname()
        assert(self.__ifgi_mat.get_classname() == 'EnvironmentMaterial')

        preview_dict = self.__ifgi_mat.get_gl_preview_dict()
        # print preview_dict
        self.set_config_dict(preview_dict)


# ----------------------------------------------------------------------

class GLTriMeshNode(GLSceneGraphNode):
    """OpenGL TriMeshNode

    A triangle mesh node"""

    # default constructor
    def __init__(self, _nodename):
        """default constructor.
        \param[in] _nodename this node name."""
        # call base class constructor to fill the members
        super(GLTriMeshNode, self).__init__(_nodename)

        # primitive node
        self.__primitive = None

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

        # lighting for points, wireframe, flat shading, Gouraud, texture
        self.__is_enabled_light_points  = GL.GL_FALSE
        self.__is_enabled_light_lines   = GL.GL_FALSE
        self.__is_enabled_light_flat    = GL.GL_TRUE
        self.__is_enabled_light_gouraud = GL.GL_TRUE
        self.__is_enabled_light_texture = GL.GL_TRUE


    # get classname
    def get_classname(self):
        """get classname

        \return class name string"""

        return 'GLTriMeshNode'

    # ------------------------------------------------------------
    # primitive node implementation
    # This is needed since GLTriMeshNode(SceneGraph.SceneGraphNode),
    # instead of GLTriMeshNode(SceneGraph.PrimitiveNode)
    # I thought this inheritance is overkill, but, is it right?
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


    def get_bbox(self):
        """get bounding box of this node
        \return bounding box
        """
        assert(self.__primitive != None)
        return self.__primitive.get_bbox()


    def set_bbox(self, _bbox):
        """assign bbox value.
        set the bbox object. (bbox is cloned before set.)
        \param _bbox bounding box to be assigned.
        """
        assert(self.__primitive != None)
        self.__primitive.set_bbox(_bbox)


    # ----------------------------------------------------------------------

    def get_drawmode_list(self):
        """get draw mode list of this GLSceneGraphNode

        \return drawmode list of this node"""

        return self.__drawmode_list


    def enter(self):
        """enter draw. Prologue of the draw()
        push the gl state that draw might change
        """

        self.__bg_color4f      = GL.glGetFloatv(GL.GL_COLOR_CLEAR_VALUE)

        self.__current_color4f = GL.glGetFloatv(GL.GL_CURRENT_COLOR)
        self.__shade_model     = GL.glGetIntegerv(GL.GL_SHADE_MODEL)
        self.__is_enabled_lighting   = GL.glIsEnabled(GL.GL_LIGHTING)
        self.__is_enabled_depthtest  = GL.glIsEnabled(GL.GL_DEPTH_TEST)
        self.__is_enabled_offsetfill = GL.glIsEnabled(GL.GL_POLYGON_OFFSET_FILL)


    def leave(self):
        """leave draw. Epilogue of the draw()
        pop the gl state
        """

        GL.glColor4fv(self.__current_color4f)
        GL.glShadeModel(self.__shade_model)
        self.gl_enable_disable(GL.GL_LIGHTING,   self.__is_enabled_lighting)
        self.gl_enable_disable(GL.GL_DEPTH_TEST, self.__is_enabled_depthtest)
        self.gl_enable_disable(GL.GL_POLYGON_OFFSET_FILL,
                               self.__is_enabled_offsetfill)



    def draw(self, _global_drawmode):
        """draw the attached triangle mesh.
        If node is deactivated, draw nothing.
        \param[in] _global_drawmode drawmode list (or-ed drawmode list bitmap)."""

        if (not self.is_node_active()):
            # node is deactivated, not call draw anymore
            return

        # check this node's drawmode. Is it local?
        _drawmode = self.get_drawmode();
        if (_drawmode == DrawMode.DrawModeList.DM_GlobalMode):
            _drawmode = _global_drawmode


        if ((_drawmode & DrawMode.DrawModeList.DM_BBox) != 0):
            self.__draw_bbox()

        if ((_drawmode & DrawMode.DrawModeList.DM_Points) != 0):
            self.gl_enable_disable(GL.GL_LIGHTING, self.__is_enabled_light_points)
            self.__draw_points()

        if ((_drawmode & DrawMode.DrawModeList.DM_Wireframe) != 0):
            self.gl_enable_disable(GL.GL_LIGHTING, self.__is_enabled_light_lines)
            self.__draw_wireframe()

        if ((_drawmode & DrawMode.DrawModeList.DM_Hiddenline) != 0):
            self.gl_enable_disable(GL.GL_LIGHTING, self.__is_enabled_light_lines)
            self.__draw_hiddenline()

        if ((_drawmode & DrawMode.DrawModeList.DM_Solid_Basecolor) != 0):
            self.gl_enable_disable(GL.GL_LIGHTING, GL.GL_FALSE) # always light off
            self.__draw_solid_basecolor()

        if ((_drawmode & DrawMode.DrawModeList.DM_Solid_Flat) != 0):
            self.gl_enable_disable(GL.GL_LIGHTING, self.__is_enabled_light_flat)
            self.__draw_flat_shading()

        if ((_drawmode & DrawMode.DrawModeList.DM_Solid_Gouraud) != 0):
            self.gl_enable_disable(GL.GL_LIGHTING, self.__is_enabled_light_gouraud)
            self.__draw_solid_gouraud()

        if ((_drawmode & DrawMode.DrawModeList.DM_Solid_Texture) != 0):
            self.gl_enable_disable(GL.GL_LIGHTING, self.__is_enabled_light_texture)
            self.__draw_solid_texture()



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
        GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL);

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
            # FIXME: normal is always generated, may slow for python
            v1 = vp[face[1]] - vp[face[0]]
            v2 = vp[face[2]] - vp[face[0]]
            n  = numpy.cross(v1, v2)
            n  /= numpy.linalg.norm(n)
            GL.glNormal3fv(n)
            GL.glVertex3d(vp[face[0]][0], vp[face[0]][1], vp[face[0]][2])
            GL.glVertex3d(vp[face[1]][0], vp[face[1]][1], vp[face[1]][2])
            GL.glVertex3d(vp[face[2]][0], vp[face[2]][1], vp[face[2]][2])
        GL.glEnd()

    # draw solid_gouraud
    def __draw_solid_gouraud(self):
        """draw solid_gouraud"""
        GL.glShadeModel(GL.GL_SMOOTH)

        # vp reference
        vp = self.get_primitive().vertex_list
        vn = self.get_primitive().normal_list

        GL.glBegin(GL.GL_TRIANGLES)
        face_count   = len(self.get_primitive().face_idx_list)
        normal_count = len(self.get_primitive().normal_idx_list)

        if ((vn != None) and (face_count != normal_count)):
            ILog.error('This mesh has vertex normal, but they does not match ' +\
                           'the vertex size. ' +\
                           'Cannot render Gouraud shading without normals.')

        if ((vn != None) and (face_count == normal_count)):
            # vertex normal registered
            for idx in xrange(0, face_count):
                face   = self.get_primitive().face_idx_list[idx]
                normal = self.get_primitive().normal_idx_list[idx]
                GL.glNormal3fv(normal[0])
                GL.glVertex3d(vp[face[0]][0], vp[face[0]][1], vp[face[0]][2])
                GL.glNormal3fv(normal[1])
                GL.glVertex3d(vp[face[1]][0], vp[face[1]][1], vp[face[1]][2])
                GL.glNormal3fv(normal[2])
                GL.glVertex3d(vp[face[2]][0], vp[face[2]][1], vp[face[2]][2])

        else:
            # no vertex normal
            for face in self.get_primitive().face_idx_list:
                GL.glVertex3d(vp[face[0]][0], vp[face[0]][1], vp[face[0]][2])
                GL.glVertex3d(vp[face[1]][0], vp[face[1]][1], vp[face[1]][2])
                GL.glVertex3d(vp[face[2]][0], vp[face[2]][1], vp[face[2]][2])

        GL.glEnd()



    # draw solid_texture
    def __draw_solid_texture(self):
        """draw solid_texture"""
        GL.glShadeModel(GL.GL_FLAT)
        print 'NIN: __draw_solid_texture'


    # ----------------------------------------------------------------------

    def get_info_html(self):
        """Get information html text.
        Inherited from GLSceneGraphNode
        \return base GL node info + GLTriMeshNode info
        """
        tmesh_desc = self.get_info_html_GLSceneGraphNode() +\
            '<h2>GLTriMeshNoded information</h2>\n'

        if self.__primitive == None:
            tmesh_desc += 'No primitive\n'
            return tmesh_desc

        tmesh = self.__primitive

        tmesh_desc += '<ul>\n'

        tmesh_desc += '  <li><b>Primitive class:</b>' + tmesh.get_classname() +'\n'

        tmesh_desc +=\
            '  <li><b># of vertices:</b>' + str(len(tmesh.vertex_list)) + '\n' +\
            '  <li><b># of faces:</b>'    + str(len(tmesh.face_idx_list)) + '\n'

        if (tmesh.texcoord_list == []):
            tmesh_desc += '  <li>no texture coordinates\n'
        else:
            tmesh_desc += \
                '  <li><b># of texcoords:</b>'    +\
                str(len(tmesh.texcoord_list)) + '\n' +\
                '  <li><b># of texcoord idx:</b>' +\
                str(len(tmesh.texcoord_idx_list)) + '\n'

        if (tmesh.normal_list == []):
            tmesh_desc += '  <li>no normals\n'
        else:
            tmesh_desc += \
                '  <li><b># of normals:</b>'    + str(len(tmesh.normal_list)) + '\n' +\
                '  <li><b># of normal idx:</b>' + str(len(tmesh.normal_idx_list)) + '\n'

        tmesh_desc += '  <li><b>bbox:</b>' + str(tmesh.bbox) + '\n'
        tmesh_desc += '<\ul>\n'

        return tmesh_desc


    def create_config_dialog(self, _tab_dialog):
        """Create configuration dialog for GLTriMeshNode.
        The configuration dialog is QtSimpleTabDialog.
        Inherited from GLSceneGraphNode

        \param[in] _tab_dialog a QtSimpleTabDialog
        \return True since this node is configurable.
        """

        return False

# ----------------------------------------------------------------------

def new_gl_scenegraph_node(_sgnode, _name_mat_dict):
    """OpenGL scenegraph node factory

    Supported ifgi nodes:
      - ScengraphNode:     translated to a GLSceneGraphNode
      - Primitive.TriMesh: translated to a GLTriMeshNode

    \param[in] _sgnode generic scenegraph node
    \param[in] _name_mat_dict material name -> material reference dict
    """

    if _sgnode.is_primitive_node():
        if _sgnode.get_primitive().get_classname() == 'TriMesh':
            assert(_sgnode.get_primitive().get_name() != None)

            gltmeshnode = GLTriMeshNode(_sgnode.get_primitive().get_name())
            gltmeshnode.set_primitive(_sgnode.get_primitive())

            assert(gltmeshnode.get_primitive() != None)
            assert(_sgnode.get_primitive().get_material_name() != 0)
            matname = _sgnode.get_primitive().get_material_name()
            glmatnode = GLMaterialNode(matname)

            # material should be in the dict
            assert(matname in  _name_mat_dict)
            glmatnode.set_material(_name_mat_dict[matname])
            glmatnode.append_child(gltmeshnode)
            print 'Added GLMaterialNode --- GLTriMeshNode'
            return glmatnode
        else:
            print 'unsupported primitive: ' + _sgnode.get_primitive().get_classname()
            return None
    else:
        return GLSceneGraphNode('GL:' + _sgnode.get_nodename())


# ----------------------------------------------------------------------

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

# ----------------------------------------------------------------------

def create_gl_scenegraph(_ifgi_reader):
    """create GL scenegraph from ifgi scene reader

    SceneGraph +
               +--+ SceneGraphNode: 'rootsg' __root_node
                    +--+ CameraNode: 'main_cam' __camera
                    +--+ SceneGraphNode: 'meshgroup'
                         +--+ Material: 'mat0'
                              +--+ TriMesh: 'trimesh0'
                         +--+ Material: 'mat1'
                              +--+ TriMesh: 'trimesh1'
                         ...
    """
    if (not _ifgi_reader.is_valid()):
        raise StandardError, ('invalid ifgi scene reader.')

    # create scenegraph
    glsg = GLSceneGraph()

    # create scenegraph's root node
    rootsg = SceneGraphNode('rootsg')
    cam_node = CameraNode('main_cam')
    rootsg.append_child(cam_node)

    # 'materialgroup' is a special group.
    mat_group_node = SceneGraphNode('materialgroup')
    rootsg.append_child(mat_group_node)
    for mat_dict in _ifgi_reader.material_list:
        mat = Material.material_factory(mat_dict)
        ch_mat_node = MaterialNode(mat_dict['mat_name'])
        ch_mat_node.set_material(mat)
        mat_group_node.append_child(ch_mat_node)


    mesh_group = SceneGraphNode('meshgroup')
    rootsg.append_child(mesh_group)
    for geo_dict in _ifgi_reader.geometry_list:
        ch_node = PrimitiveNode(geo_dict['geo_name'], geo_dict['TriMesh'])
        mesh_group.append_child(ch_node)

    sg.set_root_node(rootsg)
    sg.set_current_camera(cam_node.get_camera())

    assert(sg.is_valid())

    return sg

# ----------------------------------------------------------------------

#
# main test
#
# if __name__ == '__main__':
