#!/usr/bin/env python

"""QtSceneGraphDialog

\author Yamauchi, Hitoshi
\file
\brief scene graph inspector dialog pyqt implementtaion"""

import sys
import QtSceneGraphWidget
import SceneGraph
import GLSceneGraph
import Primitive

from PyQt4 import QtCore, QtGui


# QtSceneGraphDialog
class QtSceneGraphDialog(QtGui.QDialog):
    """QtSceneGraphDialog
    SceneGraph viewer dialog"""

    def __init__(self, parent=None):
        """constructor"""

        super(QtSceneGraphDialog, self).__init__(parent)
        # self.setModal(_modal);

        self.sceneGraphView = QtSceneGraphWidget.QtSceneGraphViewWidget(self);

        self.layout = QtGui.QVBoxLayout();
        self.layout.setObjectName('SceneGraph viewer, dialog layout');
        self.layout.setMargin(0);
        self.layout.addWidget(self.sceneGraphView);
        self.setLayout(self.layout);
        self.resize(450, 300)

    # a signal emitted when dialog is closed
    def closed(self):
        """a signal emitted when dialog is closed"""

        print 'called QtSceneGraphWidget::closed() '

    # Clear current view and import scene graph _root.
    def update(self, _sceneGraphRoot):
        """Clear current view and import scene graph _root.
        Calls sceneGraphViewer()'s update() method."""

        print 'QtSceneGraphWidget::update called'

    # emits close(), override Dialog's closeEvent
    def closeEvent(self, _close_event):
        """signal emits close(), override Dialog's closeEvent
        and call super class's closeEvent().

        \param[in] _close_event close event"""

        self.closed()
        super(QtSceneGraphDialog, self).closeEvent(_close_event)




# copy scenegraph tree subroutine
def copy_glsg_to_treeitem_sub(_cur_glsgnode, _cur_tinode, _level):
        """copy OpenGL scenegraph tree to tree item graph subroutine
        \param[in]: _cur_glsgnode current visiting OpenGL scenegraph node
        \param[in]: _cur_tinode   current visiting tree item node
        \param[in]: _level        current depth level"""

        ti_parent = _cur_tinode
        for ch_glsgnode in _cur_glsgnode.children:
            if ch_glsgnode.is_primitive_node() == True:
                print 'DEBUG: creating tree item by a primitive'
                # primitive node
                ti = QtSceneGraphWidget.SceneGraphNodeTreeItem(
                    ch_glsgnode.get_primitive(),
                    ti_parent)
                ti_parent.appendChild(ti)
            else:
                print 'DEBUG: creating tree item by a scenegraph node'
                # create and refer the glsg node
                ti = QtSceneGraphWidget.SceneGraphNodeTreeItem(ch_glsgnode,
                                                               ti_parent)
                ti_parent.appendChild(ti)
                copy_glsg_to_treeitem_sub(ch_glsgnode, ti, _level + 1)



# test when called directly
if __name__ == '__main__':
    """test when called directly"""
    app = QtGui.QApplication(sys.argv)
    sgdialog = QtSceneGraphDialog()

    # dummy FIXME: replace these with SceneGraphNode
    sgmodel_root = sgdialog.sceneGraphView.get_scenegraph_model(). \
        get_scenegraph_model_root()

    #----------------------------------------------------------------------
    # 1. create a SceneGraph
    #
    # This SceneGraph is independent from GLSceneGraph (can be used
    # for tracer)
    sg = SceneGraph.SceneGraph()
    assert(sg.root_node == None)

    # create scenegraph's root node
    #   simplest example: root scenegraph node only
    rootsgnode = SceneGraph.SceneGraphNode('sgroot')
    sg.set_root_node(rootsgnode)

    # create a scenegraph
    #
    # + rootnode + child0
    #            + child1
    #            + child2
    #            + child3 + child4 + primitive
    #
    child0 = SceneGraph.SceneGraphNode('child0')
    child1 = SceneGraph.SceneGraphNode('child1')
    child2 = SceneGraph.SceneGraphNode('child2')
    child3 = SceneGraph.SceneGraphNode('child3')
    child4 = SceneGraph.SceneGraphNode('child4')
    prim0  = Primitive.TriMesh()

    rootsgnode.append_child(child0)
    rootsgnode.append_child(child1)
    rootsgnode.append_child(child2)
    rootsgnode.append_child(child3)
    child3.append_child(child4)
    child4.set_primitive(prim0)

    #----------------------------------------------------------------------
    # 2. create a GLSceneGraph
    #
    # attach the SceneGraph to a GLSceneGraph
    glsg = GLSceneGraph.GLSceneGraph()
    glsg.set_scenegraph(sg)

    # create tree item root
    ti = QtSceneGraphWidget.SceneGraphNodeTreeItem(glsg.gl_root_node,
                                                   sgmodel_root)
    sgmodel_root.appendChild(ti)
    # create tree item graph from the GLSceneGraph
    copy_glsg_to_treeitem_sub(glsg.gl_root_node, ti, 0)

    sys.exit(sgdialog.exec_())
