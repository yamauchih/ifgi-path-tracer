#!/usr/bin/env python
#
# QtSceneGraphWidget
#   SceneGraph inspector
#
# \author Yamauchi, Hitoshi
#

"""IFGI QtSceneGraphWidget v 0.0.0"""

from PyQt4 import Qt, QtCore, QtGui

# QtSceneGraphView
#
# tree structured SceneGraph inspector view
#
class QtSceneGraphViewWidget(QtGui.QTreeView):

    # constructor
    def __init__(self, parent=None):
        super(QtSceneGraphViewWidget, self).__init__(parent)

        # self.setObjectName(_name);
        # for showing the root as a collapsed sign ([+] or [-])
        self.setRootIsDecorated(True);
        self.resize(400, 300);

        self.model = SceneGraphModel()

        # init model here

        self.setModel(self.model)

    # get scenegraph model
    def get_scenegraph_model(self):
        return self.model


#
# SceneGraphNode tree item.
#
# Adapter: this is a SceneGraphNode, but this pretends a TreeItem.
#
#
class SceneGraphNodeTreeItem(object):

    # constructor
    #
    # \param[in] _sgnode a GLSceneGraphNode
    # \param[in] _parent parent node (None for only root node)
    def __init__(self, _sgnode, _parent = None):
        self.parentItem     = _parent
        self.sceneGraphNode = _sgnode
        self.childItems     = []

    # append child
    def appendChild(self, _item):
        self.childItems.append(_item)

    # get child
    def child(self, _row):
        return self.childItems[_row]

    # get number of children
    def childCount(self):
        return len(self.childItems)

    # colomnCount
    # 
    # always 4. ['Node', 'Type', 'Status', 'Mode']
    def columnCount(self):
        return 4

    # get GLSceneGraphNode
    #
    # \param[in] _column scenegraph node view column (0...3)
    def data(self, _column):
        if   (_column == 0):
            return self.sceneGraphNode.get_nodename()
        elif (_column == 1):
            return self.sceneGraphNode.get_classname()
        elif (_column == 2):
            if self.sceneGraphNode.is_node_active():
                return 'Active'
            else:
                return 'Deactivated'
        elif (_column == 3):
            if self.sceneGraphNode.is_global_drawmode():
                return 'Global'
            else:
                return 'Local: NIN no local drawmode name'
        else:
            raise IndexError('SceneGraphNodeTreeItem: data')
            return 'Error: IndexError'

    # get parent
    def parent(self):
        return self.parentItem

    # get row (depth)
    def row(self):
        if self.parentItem:
            return self.parentItem.childItems.index(self)
        return 0

#
# SceneGraph Model.
#
# QAbstractItemModel: suitable for any model
#
class SceneGraphModel(QtCore.QAbstractItemModel):

    # constructor
    def __init__(self, parent = None):
        super(SceneGraphModel, self).__init__(parent)
        self.rootItem = SceneGraphNodeTreeItem(
            # root is used for the column label
            # HEREHERE 2011-1-24(Mon)
            ('Node', 'Type', 'Status', 'Mode')
            )

    # get scene graph model root
    #
    # \return get scene graph model root
    def get_scenegraph_model_root(self):
        return self.rootItem

    def columnCount(self, parent):
        if parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return self.rootItem.columnCount()

    def data(self, index, role):
        if not index.isValid():
            return None

        if role != QtCore.Qt.DisplayRole:
            return None

        item = index.internalPointer()

        return item.data(index.column())

    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.NoItemFlags

        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.rootItem.data(section)

        return None

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()

        childItem = index.internalPointer()
        parentItem = childItem.parent()

        if parentItem == self.rootItem:
            return QtCore.QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        return parentItem.childCount()
