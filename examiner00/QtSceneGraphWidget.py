#!/usr/bin/env python

"""QtSceneGraphWidget
\file
\brief SceneGraph inspector widget
\module QtSceneGraphWidget"""

from PyQt4 import Qt, QtCore, QtGui
import GLSceneGraph

# QtSceneGraphView
class QtSceneGraphViewWidget(QtGui.QTreeView):
    """QtSceneGraphView

    Tree structured SceneGraph inspector view widget.
    Current enabled keys:
      - Ctrl+E       show node config dialog
      - Ctrl+I       show node information dialog
      - Ctrl+M       execute a command (copy, paste)
      - Return       return key pressed (popup context menu)
    """
    #NIN Keys
    # - Ctrl+Insert  copy  scene node config
    # - Shift+Insert paste scene node config


    #------------------------------------------------------------
    # signal: class static
    #------------------------------------------------------------
    __signal_key_pressed = QtCore.pyqtSignal()


    # constructor
    def __init__(self, parent=None):
        """constructor

        \param[in] _parent parent Qt widget"""

        super(QtSceneGraphViewWidget, self).__init__(parent)

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

        #------------------------------
        # connect slots
        #------------------------------
        # click event
        self.clicked.      connect(self.slot_clicked)
        self.doubleClicked.connect(self.slot_doubleClicked)
        self.activated.    connect(self.slot_activated)
        self.collapsed.    connect(self.slot_collapsed)
        self.expanded.     connect(self.slot_expanded)


    # get scenegraph (Qt) model
    def get_scenegraph_model(self):
        """get scenegraph (Qt) model
        \return the model"""

        return self.__model

    # show config dialog
    def show_config_dialog(self, _glsgnode):
        """show config dialog for _glsgnode.
        \param[in] _glsgnode gl scenegraph node to configure"""
        print 'DEBUG: show config dialog'

    # show node info
    def show_nodeinfo_dialog(self, _glsgnode):
        """show information dialog for _glsgnode.
        \param[in] _glsgnode gl scenegraph node"""
        print 'DEBUG: show info dialog'

    # show dialog for \c _item resp. the corresponding \c _node
    def right_button_pressed(self, _glsgnode):
        """right button pressed on _glsgnode.
        \param[in] _glsgnode GL scenegraph node."""

    # return pressed action will do the same to the rightButtonPressed
    def return_key_pressed(self):
        if ((self.__cur_tree_item != None) and
            (self.__cur_tree_item.get_node() != None)):
            self.right_button_pressed(self.__cur_tree_item.get_node())

    # initialize parameter option
    # def initParameter(self):

    # auto adjust column size
    def adjust_columnsize_by_contents(self):
        if(self.__columnsize_autoadjust):
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

        assert(self.__cur_tree_item != None)
        assert(self.__cur_tree_item.get_node() != None)

        if (self.__key_modifier_state & QtCore.Qt.ControlModifier != 0):
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
        elif(self.__key_modifier_state & QtCore.Qt.ShiftModifier != 0):
            # Shift+
            if (_qkeyev.key() == QtCore.Qt.Key_Insert):
                print 'DEBUG: Shift+Key_Insert'
                # NIN: self.paste_scenegraph_config()
                pass
            else:
                # do nothing for other keys
                pass
        elif(self.__key_modifier_state == QtCore.Qt.NoModifier):
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

        # NIN __signal_key_pressed.emit(self.scenegraph_root,
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
            self.rightButtonPressed(self.__cur_tree_item.node());

        self.adjust_columnsize_by_contents()
        print 'slot clicked'

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

        print 'slot activated'
        if (_qmidx.isValid()):
            self.__cur_tree_item = _qmidx.internalPointer();
            print 'slot activated: ' + str(type(self.__cur_tree_item))
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
    def get_global_drawmode_str(self):
        """get draw mode string
        \return draw mode string label 'Mode'"""

        return 'Mode'


# SceneGraphNode tree item.
class SceneGraphNodeTreeItem(object):
    """SceneGraphNode tree item.

    Adapter: this is a SceneGraphNode, but this pretends a TreeItem.
    """

    # constructor
    def __init__(self, _sgnode, _parent = None):
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
            return self.sceneGraphNode.get_global_drawmode_str()
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
        self.rootItem =\
            SceneGraphNodeTreeItem(QtTreeviewLabelGLSceneGraphNode())

    # get scene graph model root
    def get_scenegraph_model_root(self):
        """get scene graph model root
        \return get scene graph model root"""

        return self.rootItem

    # get numver of columns
    def columnCount(self, _parent):
        """get numver of columns

        \param[in] _parent parent tree item"""

        if _parent.isValid():
            return _parent.internalPointer().columnCount()
        else:
            return self.rootItem.columnCount()

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
            return self.rootItem.data(_section)

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
            parentItem = self.rootItem
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

        if parentItem == self.rootItem:
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
            parentItem = self.rootItem
        else:
            parentItem = _parent.internalPointer()

        return parentItem.childCount()
