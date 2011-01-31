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

    tree structured SceneGraph inspector view widget
    """

    # constructor
    def __init__(self, parent=None):
        """constructor

        \param[in] _parent parent Qt widget"""

        super(QtSceneGraphViewWidget, self).__init__(parent)

        # self.setObjectName(_name);
        # for showing the root as a collapsed sign ([+] or [-])
        self.setRootIsDecorated(True);
        self.resize(400, 300);

        self.model = SceneGraphModel()

        # init model here

        self.setModel(self.model)

        # init the current/selected scenegrap node
        self.cur_tree_item = 0
        assert(self.selectionModel() != None)
        qmidx = self.selectionModel().currentIndex()
        # current node is selected
        self.slot_activated(qmidx)

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

        return self.model

    # slot clicked
    def slot_clicked(self, _qmidx):
        """slot clicked.
        \param[in] _qmidx clicked item model index"""

        # set the selected current tree item
        self.slot_activated(_qmidx);

        # selected and right click

        # NIN
        # if ((self.cur_tree_item != None) and
        #     (d_mouseButtons == Qt::RightButton)):
        #     assert(self.cur_tree_item.get_node() != None)
        #     self.rightButtonPressed(self.cur_tree_item.node());

        # self.adjustColumnSizeByContents()
        print 'slot clicked'

    # slot double clicked
    def slot_doubleClicked(self, _qmidx):
        """slot double clicked
        \param[in] _qmidx double clicked item model index"""

        print 'slot double clicked'
        self.slot_activated(_qmidx)

        if (self.cur_tree_item == None):
            # no selected node
            return

        glsgnode = self.cur_tree_item.get_node()
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
            self.cur_tree_item = _qmidx.internalPointer();
            print 'slot activated: ' + str(type(self.cur_tree_item))
        else:
            self.cur_tree_item = None


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
