#!/usr/bin/env python
## QtSceneGraphWidget
# \file
# \brief SceneGraph inspector widget
# \module QtSceneGraphWidget


"""IFGI QtSceneGraphWidget v 0.0.0"""

from PyQt4 import Qt, QtCore, QtGui
import GLSceneGraph

## QtSceneGraphView
#
# tree structured SceneGraph inspector view widget
#
class QtSceneGraphViewWidget(QtGui.QTreeView):

    ## constructor
    #
    # \param _parent parent Qt widget
    def __init__(self, parent=None):
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

  
    ## get scenegraph (Qt) model
    # \return the model
    def get_scenegraph_model(self):
        return self.model

    ## slot clicked
    # \param[in] _qmidx clicked item model index
    def slot_clicked(self, _qmidx):
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

    ## slot double clicked
    # \param[in] _qmidx double clicked item model index
    def slot_doubleClicked(self, _qmidx):
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


    ## slot activated
    # \param[in] _qmidx activated item model index
    def slot_activated(self, _qmidx):
        print 'slot activated'
        if (_qmidx.isValid()):
            self.cur_tree_item = _qmidx.internalPointer();
            print 'slot activated: ' + str(type(self.cur_tree_item))
        else:
            self.cur_tree_item = None


    ## slot collapsed
    # \param[in] _qmidx collapsed item model index
    def slot_collapsed(self, _qmidx):
        print 'slot collapsed'

    ## slot expanded
    # \param[in] _qmidx expanded item model index
    def slot_expanded(self, _qmidx):
        print 'slot expanded'



## ScneGraph node, but for QTreeview's label only
#
# returns ['Node', 'Type', 'Status', 'Mode'] for the QTreeView label
class QtTreeviewLabelGLSceneGraphNode(GLSceneGraph.GLSceneGraphNode):
    ## get nodename
    # \return node label 'Node'
    def get_nodename(self):
        return 'Node'

    ## get classname (shown in the SceneGraph viewer as node Type)
    # \return class name label 'Type'
    def get_classname(self):
        return 'Type'

    ## get node active state string
    # \return get node active state string label 'Status'
    def get_active_state(self):
        return 'Status'

    ## get draw mode string
    # \return draw mode string label 'Mode'
    def get_global_drawmode_str(self):
        return 'Mode'


##
# SceneGraphNode tree item.
#
# Adapter: this is a SceneGraphNode, but this pretends a TreeItem.
#
#
class SceneGraphNodeTreeItem(object):

    ## constructor
    #
    # \param[in] _sgnode a GLSceneGraphNode
    # \param[in] _parent parent node (None for only root node)
    def __init__(self, _sgnode, _parent = None):
        self.parentItem     = _parent
        self.sceneGraphNode = _sgnode
        self.childItems     = []

    ## append child
    #
    # \param[in] _item child tree item
    def appendChild(self, _item):
        self.childItems.append(_item)

    ## get child
    #
    # \param[in] _row row position of child
    def child(self, _row):
        return self.childItems[_row]

    ## get number of children
    # \return number of children
    def childCount(self):
        return len(self.childItems)

    ## colomnCount
    # 
    # \return always 4. ['Node', 'Type', 'Status', 'Mode']
    def columnCount(self):
        return 4

    ## get column data string.
    #
    # \param[in] _column scenegraph node view column (0...3)
    def data(self, _column):
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

    ## get parent
    # \return parent tree item
    def parent(self):
        return self.parentItem

    ## get row (depth)
    # \return get row (depth) size
    def row(self):
        if self.parentItem:
            return self.parentItem.childItems.index(self)
        return 0

    ## get scenegraph node
    # \return scenegraph node 
    def get_node(self):
        return self.sceneGraphNode


## SceneGraph Model
#
# QAbstractItemModel: suitable for any model
#
class SceneGraphModel(QtCore.QAbstractItemModel):

    ## constructor
    # \param[in] _parent 
    def __init__(self, _parent = None):
        super(SceneGraphModel, self).__init__(_parent)
        self.rootItem =\
            SceneGraphNodeTreeItem(QtTreeviewLabelGLSceneGraphNode())

    ## get scene graph model root
    #
    # \return get scene graph model root
    def get_scenegraph_model_root(self):
        return self.rootItem

    ## get numver of columns
    #
    # \param[in] _parent parent tree item
    def columnCount(self, _parent):
        if _parent.isValid():
            return _parent.internalPointer().columnCount()
        else:
            return self.rootItem.columnCount()

    ## get data
    #
    # \param[in] _qmidx model index
    # \param[in] _role  model role (currently DisplayRole only)
    # \return tree item data (string, node data of [Node, Type,
    # Status, Mode])
    def data(self, _qmidx, _role):
        if not _qmidx.isValid():
            return None

        if _role != QtCore.Qt.DisplayRole:
            return None

        item = _qmidx.internalPointer()

        return item.data(_qmidx.column())

    ## flag
    #
    # \param[in] _qmidx model index
    # \return tree item flag
    def flags(self, _qmidx):
        if not _qmidx.isValid():
            return QtCore.Qt.NoItemFlags

        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable


    ## get header data
    #
    # \param[in] _section
    # \param[in] _orientation
    # \param[in] _role
    # \return header label data (string of ['Node', 'Type', 'Status',
    # 'Mode']), None if invalid _section, _orientation
    def headerData(self, _section, _orientation, _role):
        if ((_orientation == QtCore.Qt.Horizontal) and 
            (_role        == QtCore.Qt.DisplayRole)):
            return self.rootItem.data(_section)

        return None

    ## get the model index
    #
    # \param[in] _row    row of the view
    # \param[in] _column column of the view
    # \param[in] _parent parent tree item
    # \return corresponding model index
    def index(self, _row, _column, _parent):
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

    ## get parent of model index
    # \param[in] _qmidx model index
    # \return parent of _qmidx. or invalid model index if _qmidx is a
    # root or invalid
    def parent(self, _qmidx):
        if not _qmidx.isValid():
            return QtCore.QModelIndex()

        childItem = _qmidx.internalPointer()
        parentItem = childItem.parent()

        if parentItem == self.rootItem:
            return QtCore.QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)

    ## get number of rows
    # \param[in] _parent parent tree item
    # \return number of rows
    def rowCount(self, _parent):
        if _parent.column() > 0:
            return 0

        if not _parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = _parent.internalPointer()

        return parentItem.childCount()
