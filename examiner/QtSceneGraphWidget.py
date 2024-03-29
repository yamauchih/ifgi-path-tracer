#!/usr/bin/env python
#
# Copyright (C) 2010-2011 Yamauchi, Hitoshi
#

"""QtSceneGraphWidget
\file
\brief SceneGraph inspector widget
\module QtSceneGraphWidget
"""

from PySide import QtCore, QtGui
import GLSceneGraph, DrawMode, QtUtil, QtInfoDialog, QtSimpleTabDialog

# QtSceneGraphView
class QtSceneGraphViewWidget(QtGui.QTreeView):
    """QtSceneGraphView

    Tree structured SceneGraph inspector view widget.
    Current enabled keys:
      - Ctrl+E       show node config dialog
      - Ctrl+I       show node information dialog
      - Ctrl+M       execute a command (copy, paste)
      - Return       return key pressed (popup context menu)

    Node update communication:
      - NodeDialog (= QtSimpleTabDialog) has a node/nodes.
          - emit update(_node)
          - NodeDialog is a listener of the node.
      - QtSceneGraphWidget
          - connect NodeListener::update(_event) to
          QtSceneGraphWidget::slot_node_changed_by_dialog(_event, _root_node, _node)
          - slot_node_changed_by_dialog(_event, _root_node, _node)
             - emit signal_node_changed(_event, _rootNode, _node)
          - itemPopupCallback()
             - emit signal_node_changed(_event, _root_node, _updated_node)
               when draw mode and etc. changed
          - statusPopupCallback()
             - emit signal_node_changed(_event, _root_node, _updated_node)
               when draw mode and etc. changed

      - QtExaminerWidget
          - connect QtSceneGraphWidget::signal_node_changed(
                 _event, _root_node, _updated_node) to
            QtExaminerWidget.slot_node_changed_by_dialog(
                 _event, _root_node, _updated_node)
    """
    #NIN Keys
    # - Ctrl+Insert  copy  scene node config
    # - Shift+Insert paste scene node config


    #------------------------------------------------------------
    # signal: class static
    #------------------------------------------------------------
    # signal key pressed
    # \param[in]
    signal_key_pressed = QtCore.Signal(object)
    # signal node changed
    # \param[in] object event object
    # \param[in] object updated node object
    signal_node_changed = QtCore.Signal(object, object, object)

    # constructor
    def __init__(self, _parent, _qt_scenegraph_dialog):
        """constructor

        \param[in] _parent parent Qt widget"""

        super(QtSceneGraphViewWidget, self).__init__(_parent)

        self.__sg_dialog = _qt_scenegraph_dialog

        # self.setObjectName(_name);
        # for showing the root as a collapsed sign ([+] or [-])
        self.setRootIsDecorated(True);
        self.resize(400, 300);

        self.__model = SceneGraphModel()

        # init model here
        self.setModel(self.__model)

        # init the current/selected scenegrap node
        self.__cur_tree_item = None
        assert(self.selectionModel() != None)
        qmidx = self.selectionModel().currentIndex()
        # current node is selected
        self.slot_activated(qmidx)

        # key, mouse state
        self.__key_modifier_state = None
        self.__mouse_button_state = None

        # property
        self.__is_columnsize_autoadjust = True
        self.__popupmenu              = None

        # no need to collect global drawmode list since each node
        # needs no global (like in the main window) draw mode list
        # self.__drawmode_list = None

        self.__gl_scenegraph          = None
        self.__drawmode_bitmap2action = {} # drawmode bitmap to action dictionary


        #------------------------------
        # connect slots
        #------------------------------
        # click event
        self.clicked.      connect(self.slot_clicked)
        self.doubleClicked.connect(self.slot_doubleClicked)
        self.activated.    connect(self.slot_activated)
        self.collapsed.    connect(self.slot_collapsed)
        self.expanded.     connect(self.slot_expanded)

    # update by scenegraph
    def update_scenegraph(self, _gl_scenegraph):
        """update mode and view by scenegraph.
        Import _gl_scenegraph to treeview widget.
        \param[in] _gl_scenegraph GL scenegraph
        """
        # create tree item root
        tiroot = SceneGraphNodeTreeItem(_gl_scenegraph.get_gl_root_node(),
                                        self.__model.get_scenegraph_model_root())
        # create tree item tree from the GLSceneGraph
        self.__copy_glsg_to_treeitem_sub(_gl_scenegraph.get_gl_root_node(),
                                         tiroot, 0)
        self.__model.update_tree(tiroot)

        # unselect the current item
        self.__cur_tree_item = None

        # collect drawmode from the gl scenegraph

        # no need to collect global drawmode list since each node
        # needs no global (like in the main window) draw mode list
        # self.__drawmode_list = _gl_scenegraph.collect_drawmode_list()

        self.__gl_scenegraph = _gl_scenegraph

        self.adjust_columnsize_by_contents()



    # get scenegraph (Qt) model
    def get_scenegraph_model(self):
        """get scenegraph (Qt) model
        \return the model"""

        return self.__model

    # show config dialog
    def show_config_dialog(self):
        """show config dialog for the current node.
        The current node is stored in self.__cur_tree_item.get_node()
        """
        print 'DEBUG: show config dialog'
        assert(self.__cur_tree_item != None)
        assert(self.__cur_tree_item.get_node() != None)

        # better not set the parents
        config_dialog = QtSimpleTabDialog.QtSimpleTabDialog()
        self.__sg_dialog.signal_closed.connect(config_dialog.slot_closed)

        config_dialog.setWindowModality(QtCore.Qt.NonModal)

        # create a configuration dialog depends on the each node.
        # When return false, the node is not configurable.
        if self.__cur_tree_item.get_node().create_config_dialog(config_dialog) == True:
            # connect node dialog to scenegraph widget.slot_node_changed_by_dialog()
            # first disconnect all signal -> slots. doesn't work
            # config_dialog.signal_update.disconnect()
            # second connect
            config_dialog.signal_update.connect(self.slot_node_changed_by_dialog)
            config_dialog.open()


    # show node info
    def show_nodeinfo_dialog(self):
        """show information dialog for the current node.
        The current node is stored in self.__cur_tree_item.get_node().
        """
        print 'DEBUG: show info dialog'
        # Note: if QtSceneGraphDialog is modal, then these ifo dialog
        # is also modal, even with show().
        info_dialog = QtInfoDialog.QtInfoDialog(self)
        info_dialog.setWindowModality(QtCore.Qt.NonModal)

        assert(self.__cur_tree_item != None)
        assert(self.__cur_tree_item.get_node() != None)
        info_dialog.set_html(self.__cur_tree_item.get_node().get_info_html())
        info_dialog.show()


    # global draw mode check
    def __set_global_drawmode(self, _is_use_global_drawmode):
        """set global drawmode. Note: can not turn off the global
        drawmode by this method.

        \param[in] _is_use_global_drawmode when True, use global
        drawmode. However, no effect when _is_use_global_drawmode ==
        False. If you want to turn off the global drawmode, you need
        to activate one of the local drawmode.
        """

        # if try to turn off the global drawmode, ignore
        if (not _is_use_global_drawmode):
            print '__set_global_drawmode: can not turn off global drawmode. ' + \
                'use set local drawmode.'
            self.__update_popupmenu_drawmode(DrawMode.DrawModeList.DM_GlobalMode)
            return

        # Only when global mode is off, turn on it and also turn off
        # all the local mode.
        assert(self.__cur_tree_item != None)
        assert(self.__cur_tree_item.get_node() != None)

        cur_node = self.__cur_tree_item.get_node()
        # set global drawmode
        cur_node.set_drawmode(DrawMode.DrawModeList.DM_GlobalMode)
        self.__update_popupmenu_drawmode(DrawMode.DrawModeList.DM_GlobalMode)

    # right button pressed on _glsgnode.
    def right_button_pressed(self, _glsgnode):
        """right button pressed on _glsgnode.
        Show context menu with respect to _glsgnode
        \param[in] _glsgnode GL scenegraph node."""

        # create menu every time
        self.__popupmenu = None
        self.__create_popupmenu()
        self.__create_popupmenu_drawmode(_glsgnode)
        assert(_glsgnode != None)
        self.__update_popupmenu_drawmode(_glsgnode.get_drawmode())
        self.__popupmenu.exec_(QtGui.QCursor.pos())

        # print 'DEBUG: node = ' + str(_glsgnode)


    # return pressed action will do the same to the rightButtonPressed
    def return_key_pressed(self):
        if ((self.__cur_tree_item != None) and
            (self.__cur_tree_item.get_node() != None)):
            self.right_button_pressed(self.__cur_tree_item.get_node())

    # initialize parameter option
    # def initParameter(self):

    # auto adjust column size
    def adjust_columnsize_by_contents(self):
        if(self.__is_columnsize_autoadjust):
            columns = self.header().count()
            for i in range(0, columns):
                self.resizeColumnToContents(i)


    #----------------------------------------------------------------------
    # event handler
    #----------------------------------------------------------------------

    # key press event
    def keyPressEvent(self, _qkeyev):
        """key press event: reimplemented.
        some action and also remember the modifier change (e.g., shift key).
        \param[in] _qkeyev key event"""

        self.__key_modifier_state = _qkeyev.modifiers()

        # print 'DEBUG: type = ' + str(type(self.__key_modifier_state)) +\
        #     str(isinstance(self.__key_modifier_state,
        #                    QtCore.Qt.KeyboardModifiers))
        # print 'DEBUG: ' + \
        #     QtUtil.get_key_modifier_string(self.__key_modifier_state)

        if (self.__cur_tree_item == None):
            # no item selected. In such case, ignored the key press.
            return

        assert(self.__cur_tree_item.get_node() != None)

        if (QtUtil.in_key_modifier(self.__key_modifier_state,
                                   QtCore.Qt.ControlModifier)):
            # Ctrl+
            if (_qkeyev.key() == QtCore.Qt.Key_M):
                # key M: exec command
                print 'DEBUG: Ctrl+Key_M'
                pass
            elif (_qkeyev.key() == QtCore.Qt.Key_E):
                # key E: edit config dialog
                print 'DEBUG: Ctrl+Key_E'
                self.show_config_dialog(self.__cur_tree_item.get_node())

            elif (_qkeyev.key() == QtCore.Qt.Key_Insert):
                print 'DEBUG: Ctrl+Key_Insert'
                # NIN: self.copy_scenegraph_config()
                pass
            else:
                # do nothing for other keys
                pass
        elif (QtUtil.in_key_modifier(self.__key_modifier_state,
                                     QtCore.Qt.ShiftModifier)):
            # Shift+
            if (_qkeyev.key() == QtCore.Qt.Key_Insert):
                print 'DEBUG: Shift+Key_Insert'
                # NIN: self.paste_scenegraph_config()
                pass
            else:
                # do nothing for other keys
                pass
        elif (self.__key_modifier_state == QtCore.Qt.NoModifier):
            # note using == insted of & in if
            # no modifier
            if (_qkeyev.key() == QtCore.Qt.Key_Return):
                print 'DEBUG: KEY_Return'
                self.return_key_pressed()
            else:
                # do nothing for other keys
                pass

        # call super class's event handler to process all the defaults
        super(QtSceneGraphViewWidget, self).keyPressEvent(_qkeyev)

        # remember current selected node
        cur_selected_node = None
        if (self.__cur_tree_item != None):
            cur_selected_node = self.__cur_tree_item.get_node()

        # NIN signal_key_pressed.emit(self.scenegraph_root,
        #                               cur_selected_node, _qkeyev)



    # key release
    def keyReleaseEvent(self, _qkeyev):
        """key release event: reimplemented.
        remember the modifier change (e.g., shift key).
        \param[in] _qkeyev key event"""

        # update modifiers, call super::keyReleaseEvent
        self.__key_modifier_state = _qkeyev.modifiers()
        super(QtSceneGraphViewWidget, self).keyReleaseEvent(_qkeyev)

    # mouse event
    def mousePressEvent(self, _qmouseev):
        """mouse press event: reimplemented.
        remember the mouse state and might have an action
        \param[in] _qmouseev mouse event"""

        # keep the modifiers
        self.__key_modifier_state = _qmouseev.modifiers() # inherited QInputEvent
        self.__mouse_button_state = _qmouseev.buttons()

        # call super. emit clicked() -> slot_clicked()
        super(QtSceneGraphViewWidget, self).mousePressEvent(_qmouseev);

        # print 'DEBUG: global pos = ' + str(_qmouseev.globalPos())


    # other event
    # def event(self, _qev):
    #     """other events.
    #     Filtering the other events.
    #     \param[in] _qev qt event
    #     """
    #     print 'DEBUG: qevent = ' + str(_qev)


    #----------------------------------------------------------------------
    # slot: (event receiver and action)
    #----------------------------------------------------------------------

    # slot clicked
    def slot_clicked(self, _qmidx):
        """slot clicked.
        \param[in] _qmidx clicked item model index"""

        # set the selected current tree item
        self.slot_activated(_qmidx);

        # selected and right click
        if ((self.__cur_tree_item != None) and
            (self.__mouse_button_state == QtCore.Qt.RightButton)):
            assert(self.__cur_tree_item.get_node() != None)
            self.right_button_pressed(self.__cur_tree_item.get_node());

        self.adjust_columnsize_by_contents()
        # print 'slot clicked'

    # slot double clicked
    def slot_doubleClicked(self, _qmidx):
        """slot double clicked
        \param[in] _qmidx double clicked item model index"""

        print 'slot double clicked'
        self.slot_activated(_qmidx)

        if (self.__cur_tree_item == None):
            # no selected node
            return

        glsgnode = self.__cur_tree_item.get_node()
        assert(glsgnode != None)
        # toggle the node active
        glsgnode.set_node_active(not glsgnode.is_node_active())

        # inform the data is updated to the view
        # self.scheduleDelayedItemsLayout();
        # emit node_changed(glsgnode)


    # slot activated
    def slot_activated(self, _qmidx):
        """slot activated
        \param[in] _qmidx activated item model index"""

        # print 'slot activated'
        if (_qmidx.isValid()):
            self.__cur_tree_item = _qmidx.internalPointer();
            # print 'slot activated: ' + str(type(self.__cur_tree_item))
        else:
            self.__cur_tree_item = None


    # slot collapsed
    def slot_collapsed(self, _qmidx):
        """slot collapsed
        \param[in] _qmidx collapsed item model index"""

        print 'slot collapsed'

    # slot expanded
    def slot_expanded(self, _qmidx):
        """slot expanded
        \param[in] _qmidx expanded item model index"""

        print 'slot expanded'

    def slot_node_changed_by_dialog(self, _event, _updated_node):
        """slot node changed
        \param[in] _event node change event
        \param[in] _updated_node updated scenegraph node
        """

        print 'slot node changed', _event, 'signal goes to examiner'
        self.signal_node_changed.emit(_event,
                                      self.__gl_scenegraph.get_gl_root_node(),
                                      _updated_node)




    #------------------------------------------------------------
    # private methods
    #------------------------------------------------------------

    # copy scenegraph tree subroutine
    def __copy_glsg_to_treeitem_sub(self, _cur_glsgnode, _cur_tinode, _level):
        """copy OpenGL scenegraph tree to tree item graph subroutine
        \param[in]: _cur_glsgnode current visiting OpenGL scenegraph node
        \param[in]: _cur_tinode   current visiting tree item node
        \param[in]: _level        current depth level"""

        ti_parent = _cur_tinode
        for ch_glsgnode in _cur_glsgnode.get_children():
            # print 'DEBUG: creating tree item by a scenegraph node',\
            #     ch_glsgnode.get_classname(), ch_glsgnode.get_nodename()

            # create and refer the glsg node
            ti = SceneGraphNodeTreeItem(ch_glsgnode, ti_parent)
            ti_parent.appendChild(ti)
            self.__copy_glsg_to_treeitem_sub(ch_glsgnode, ti, _level + 1)

    # activate the node. might be a public method.
    def __popup_status_activate_node(self):
        """activate a node."""
        assert(self.__cur_tree_item != None)
        assert(self.__cur_tree_item.get_node() != None)
        self.__cur_tree_item.get_node().set_node_active(True)


    # deactivate the node. might be a public method.
    def __popup_status_deactivate_node(self):
        """deactivate a node."""
        assert(self.__cur_tree_item != None)
        assert(self.__cur_tree_item.get_node() != None)
        self.__cur_tree_item.get_node().set_node_active(False)


    # create popup menu for right click
    def __create_popupmenu(self):
        """create popup menu for right click. controls (without
        drawmode)
        """
        assert(self.__popupmenu == None)
        self.__popupmenu = QtGui.QMenu()

        # status menu and submenu
        self.__popup_status_submenu = self.__popupmenu.addMenu('Status')
        self.__popup_status_activate_act = \
            QtGui.QAction('Activate', self,
                          statusTip="activate the node for OpenGL view",
                          triggered=self.__popup_status_activate_node)
        self.__popup_status_submenu.addAction(self.__popup_status_activate_act)

        self.__popup_status_deactivate_act = \
            QtGui.QAction('Deactivate', self,
                          statusTip="deactivate the node for OpenGL view",
                          triggered=self.__popup_status_deactivate_node)
        self.__popup_status_submenu.addAction(self.__popup_status_deactivate_act)

        # configuration
        self.__popupmenu_configuration_act = \
            QtGui.QAction('Configuration...', self,
                          statusTip="configure this glnode",
                          triggered=self.show_config_dialog)
        self.__popupmenu.addAction(self.__popupmenu_configuration_act)

        # info
        self.__popupmenu_info_act = \
            QtGui.QAction('Info...', self,
                          statusTip="show information of this glnode",
                          triggered=self.show_nodeinfo_dialog)
        self.__popupmenu.addAction(self.__popupmenu_info_act)

        self.__popupmenu.addSeparator()

        # global mode
        self.__popupmenu_global_drawmode_act = \
            QtGui.QAction('Global default', self,
                          statusTip="use global default when GL draw",
                          triggered=self.__set_global_drawmode,
                          checkable=True)
            # PySide 1.0.8 has a bug. Bugzilla 1062 - Unable to
            # connect to triggered[bool] signal in QAction constructor
            # with checkable=True. You will see here,
            # self.__set_global_drawmode() is called instead of
            # self.__set_global_drawmode(bool)

        self.__popupmenu_global_drawmode_act.setChecked(True) # default on
        self.__popupmenu.addAction(self.__popupmenu_global_drawmode_act)

        self.__popupmenu.addSeparator()
        # checkable local drawmodes will follow in
        # __create_popup_menu_drawmode().


    # action function when a draw mode is selected
    def __popupmenu_set_drawmode(self, _drawmode_bitmap):
        """action function when a draw mode is selected.
        \param[in] _drawmode_bitmap drawmode bitmpa that is chosen
        from the menu.
        """

        assert(self.__cur_tree_item != None)
        assert(self.__cur_tree_item.get_node() != None)
        cur_node   = self.__cur_tree_item.get_node()
        updated_dm = cur_node.get_drawmode();

        if (not (QtUtil.in_key_modifier(self.__key_modifier_state,
                                        QtCore.Qt.ShiftModifier))):
            # set draw mode (here is local only) without Shift key
            updated_dm = _drawmode_bitmap
        else:
            # set draw mode (here is local only) with Shift key

            if (updated_dm == DrawMode.DrawModeList.DM_GlobalMode):
                # if global drawmode clear the mode first
                updated_dm = 0

            assert(QtUtil.in_key_modifier(self.__key_modifier_state,
                                          QtCore.Qt.ShiftModifier))
            if ((updated_dm & _drawmode_bitmap) == 0):
                # has been turned off -> turn on
                updated_dm = updated_dm | _drawmode_bitmap
            else:
                # has been turned on -> turn off, but only this bit.
                # There is the case, all turn off, but that's ok.
                # In such case, just nothing happens.
                updated_dm = updated_dm & (~_drawmode_bitmap)

        cur_node.set_drawmode(updated_dm)
        self.__update_popupmenu_drawmode(updated_dm)
        print 'DEBUG: __popupmenu_set_drawmode: ' + str(_drawmode_bitmap) +\
            ' -> ' + str(updated_dm)



    def __create_popupmenu_drawmode(self, _glnode):
        """create popup menu's draw mode part by a right click. local
        draw mode part following the control menu creation. These
        local draw mode may depends on the GL scenegraph node.

        \param[in] _glnode a GLSceneGraph node
        """

        # Some node doesn't have local draw mode.
        if _glnode.get_drawmode_list() == None:
            return

        # local draw mode is not radio button. Each can be set/unset
        # independently. (differ from QtExaminerWidget's
        # __create_popup_menu_drawmode()).

        for dmi in _glnode.get_drawmode_list().get_mode_item_list():
            if dmi.is_avairable:
                # Using a closure. mode_closure make a closure
                # function that holds self (through this) and
                # drawmode bitmap.
                def mode_closure(this, drawmode_bitmap):
                    return (lambda: this.__popupmenu_set_drawmode(drawmode_bitmap))

                # set drawmode_bitmap to the closure (keeping this drawmode_bitmap)
                modclosure = mode_closure(self, dmi.get_bitmap())
                drawmode_act = QtGui.QAction(dmi.get_name(), self,
                                             statusTip="DrawMode: " + dmi.get_name(),
                                             triggered=modclosure,
                                             checkable=True)
                self.__drawmode_bitmap2action[dmi.get_bitmap()] = drawmode_act
                self.__popupmenu.addAction(drawmode_act)

        # if (self.__drawmode_list.find_drawmode_bitmap(self.global_drawmode) == None):
        # no such draw mode in the list, turn off
        # print 'no such draw mode in the list, turn off' +\
        #    str(self.global_drawmode)


    # update popupmenu's drawmode
    def __update_popupmenu_drawmode(self, _drawmode):
        """update popupmenu's drawmode.
        popup menu will be updated according to the _drawmode.
        \param[in] _drawmode drawmode bitmap
        """

        # clear all the local mode
        for dm in DrawMode.DrawModeList.DM_Drawmode_bitmap_key_list:
            # key in dict
            if (dm in self.__drawmode_bitmap2action):
                act = self.__drawmode_bitmap2action[dm]
                act.setChecked(False)

        # Global drawmode?
        if (_drawmode == DrawMode.DrawModeList.DM_GlobalMode):
            self.__popupmenu_global_drawmode_act.setChecked(True)
            # global drawmode only, return
            return
        else:
            self.__popupmenu_global_drawmode_act.setChecked(False)

        # set all the local mode
        for dm in DrawMode.DrawModeList.DM_Drawmode_bitmap_key_list:
            # key in dict
            if (dm in self.__drawmode_bitmap2action):
                if ((_drawmode & dm) != 0):
                    act = self.__drawmode_bitmap2action[dm]
                    act.setChecked(True)



#----------------------------------------------------------------------

# ScneGraph node, but for QTreeview's label only
class QtTreeviewLabelGLSceneGraphNode(GLSceneGraph.GLSceneGraphNode):
    """ScneGraph node, but for QTreeview's label only

    returns ['Node', 'Type', 'Status', 'Mode'] for the QTreeView label
    """

    def __init__(self):
        """default constructor, do nothing"""
        pass

    # get nodename
    def get_nodename(self):
        """get nodename.
        \return node label 'Node'"""
        return 'Node'

    # get classname (shown in the SceneGraph viewer as node Type)
    def get_classname(self):
        """get classname (shown in the SceneGraph viewer as node Type)
        \return class name label 'Type'"""

        return 'Type'

    # get node active state string
    def get_active_state(self):
        """get node active state string
        \return get node active state string label 'Status'"""
        return 'Status'

    # get draw mode string
    def get_drawmode_str(self):
        """get draw mode string
        \return draw mode string label 'Mode'"""

        return 'Mode'


# SceneGraphNode tree item.
class SceneGraphNodeTreeItem(object):
    """SceneGraphNode tree item.

    Adapter: this is a SceneGraphNode, but this pretends a TreeItem.
    """

    # constructor
    def __init__(self, _sgnode, _parent):
        """constructor
        \param[in] _sgnode a GLSceneGraphNode
        \param[in] _parent parent node (None for only root node)
        """
        self.parentItem     = _parent
        self.sceneGraphNode = _sgnode
        self.childItems     = []

    # append child
    def appendChild(self, _item):
        """append child

        \param[in] _item child tree item"""

        self.childItems.append(_item)

    # get child
    def child(self, _row):
        """get child

        \param[in] _row row position of child"""

        return self.childItems[_row]

    # get number of children
    def childCount(self):
        """get number of children
        \return number of children"""

        return len(self.childItems)

    # colomnCount
    def columnCount(self):
        """colomnCount
        \return always 4. ['Node', 'Type', 'Status', 'Mode']"""

        return 4

    # get column data string.
    def data(self, _column):
        """get column data string.

        \param[in] _column scenegraph node view column (0...3)"""

        if   (_column == 0):
            return self.sceneGraphNode.get_nodename()
        elif (_column == 1):
            return self.sceneGraphNode.get_classname()
        elif (_column == 2):
            return self.sceneGraphNode.get_active_state()
        elif (_column == 3):
            return self.sceneGraphNode.get_drawmode_str()
        else:
            raise IndexError('SceneGraphNodeTreeItem: data')
            return 'Error: IndexError'

    # get parent
    def parent(self):
        """get parent
        \return parent tree item"""
        return self.parentItem

    # get row (depth)
    def row(self):
        """get row (depth)
        \return get row (depth) size"""

        if self.parentItem:
            return self.parentItem.childItems.index(self)
        return 0

    # get scenegraph node
    # \return scenegraph node
    def get_node(self):
        """get scenegraph node
        \return scenegraph node"""

        return self.sceneGraphNode


# SceneGraph Model
class SceneGraphModel(QtCore.QAbstractItemModel):
    """SceneGraph Model

    QAbstractItemModel: suitable for any model
    """

    # constructor
    def __init__(self, _parent = None):
        """constructor
        \param[in] _parent"""

        super(SceneGraphModel, self).__init__(_parent)
        self.__root_item =\
            SceneGraphNodeTreeItem(QtTreeviewLabelGLSceneGraphNode(), None)


    # clear root item
    def clear_root_item_children(self):
        """clear root item's children
        """
        # reset root item
        self.__root_item.childItems     = []

    # get scene graph model root
    def get_scenegraph_model_root(self):
        """get scene graph model root
        \return get scene graph model root"""

        return self.__root_item

    # update model
    def update_tree(self, _tree_root):
        """update model by a tree item tree.
        \param[in] _tree_root tree item tree root
        """
        self.clear_root_item_children()
        self.__root_item.appendChild(_tree_root)


    # get numver of columns
    def columnCount(self, _parent):
        """get numver of columns

        \param[in] _parent parent tree item"""

        if _parent.isValid():
            return _parent.internalPointer().columnCount()
        else:
            return self.__root_item.columnCount()

    # get data
    def data(self, _qmidx, _role):
        """get data

        \param[in] _qmidx model index
        \param[in] _role  model role (currently DisplayRole only)
        \return tree item data (string, node data of [Node, Type,
        Status, Mode])
        """

        if not _qmidx.isValid():
            return None

        if _role != QtCore.Qt.DisplayRole:
            return None

        item = _qmidx.internalPointer()

        return item.data(_qmidx.column())

    # flag
    def flags(self, _qmidx):
        """flag

        \param[in] _qmidx model index
        \return tree item flag
        """
        if not _qmidx.isValid():
            return QtCore.Qt.NoItemFlags

        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable


    # get header data
    def headerData(self, _section, _orientation, _role):
        """get header data

        \param[in] _section
        \param[in] _orientation
        \param[in] _role
        \return header label data (string of ['Node', 'Type', 'Status',
        'Mode']), None if invalid _section, _orientation
        """

        if ((_orientation == QtCore.Qt.Horizontal) and
            (_role        == QtCore.Qt.DisplayRole)):
            return self.__root_item.data(_section)

        return None

    # get the model index
    def index(self, _row, _column, _parent):
        """get the model index

        \param[in] _row    row of the view
        \param[in] _column column of the view
        \param[in] _parent parent tree item
        \return corresponding model index
        """
        if not self.hasIndex(_row, _column, _parent):
            return QtCore.QModelIndex()

        if not _parent.isValid():
            parentItem = self.__root_item
        else:
            parentItem = _parent.internalPointer()

        childItem = parentItem.child(_row)
        if childItem:
            return self.createIndex(_row, _column, childItem)
        else:
            return QtCore.QModelIndex()

    # get parent of model index
    def parent(self, _qmidx):
        """get parent of model index
        \param[in] _qmidx model index
        \return parent of _qmidx. or invalid model index if _qmidx is a
        root or invalid
        """
        if not _qmidx.isValid():
            return QtCore.QModelIndex()

        childItem = _qmidx.internalPointer()
        parentItem = childItem.parent()

        if parentItem == self.__root_item:
            return QtCore.QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)

    # get number of rows
    def rowCount(self, _parent):
        """get number of rows
        \param[in] _parent parent tree item
        \return number of rows
        """
        if _parent.column() > 0:
            return 0

        if not _parent.isValid():
            parentItem = self.__root_item
        else:
            parentItem = _parent.internalPointer()

        return parentItem.childCount()

    #------------------------------------------------------------
    # private methods
    #------------------------------------------------------------

