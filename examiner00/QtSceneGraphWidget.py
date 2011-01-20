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
    def __init__(self, data, parent = None):
        self.parentItem     = parent
        self.sceneGraphNode = data
        self.childItems     = []

    def appendChild(self, item):
        self.childItems.append(item)

    def child(self, row):
        return self.childItems[row]

    def childCount(self):
        return len(self.childItems)

    def columnCount(self):
        return len(self.sceneGraphNode)

    def data(self, column):
        try:
            return self.sceneGraphNode[column]
        except IndexError:
            return None

    def parent(self):
        return self.parentItem

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
        self.rootItem = SceneGraphNodeTreeItem(('Node', 'Type', 'Status', 'Mode'))

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
