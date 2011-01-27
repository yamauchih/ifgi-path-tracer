#!/usr/bin/env python
## QtSceneGraphDialog
#
# \author Yamauchi, Hitoshi
# \file
# \brief scene graph inspector dialog pyqt implementtaion

"""IFGI QtSceneGraphDialog Version 0.0.0"""

import sys
import QtSceneGraphWidget
import SceneGraph
import GLSceneGraph
import Primitive

from PyQt4 import QtCore, QtGui

## QtSceneGraphDialog
#
# SceneGraph viewer dialog
class QtSceneGraphDialog(QtGui.QDialog):

    ## constructor
    def __init__(self, parent=None):
        super(QtSceneGraphDialog, self).__init__(parent)
        # self.setModal(_modal);

        self.sceneGraphView = QtSceneGraphWidget.QtSceneGraphViewWidget(self);

        self.layout = QtGui.QVBoxLayout();
        self.layout.setObjectName('SceneGraph viewer, dialog layout');
        self.layout.setMargin(0);
        self.layout.addWidget(self.sceneGraphView);
        self.setLayout(self.layout);
        self.resize(450, 300)


    ## emitted when dialog is closed
    def closed(self):
        print 'called QtSceneGraphWidget::closed() '

    ## Clear current view and import scene graph _root.
    # Calls sceneGraphViewer()'s update() method.
    def update(self, _sceneGraphRoot):
        print 'QtSceneGraphWidget::update called'

    ## emits close(), override Dialog's closeEvent
    # and call super class closeEvent()
    #
    # \param[in] _close_event close event
    def closeEvent(self, _close_event):
        self.closed()
        super(QtSceneGraphDialog, self).closeEvent(_close_event)


## test when called directly
if __name__ == '__main__':
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
    rootsgnode = SceneGraph.SceneGraphNode()
    sg.set_root_node(rootsgnode)

    # create a scenegraph
    #
    # + rootnode + child0
    #            + child1
    #            + child2
    #            + child3 + child4 + primitive
    #
    child0 = SceneGraph.SceneGraphNode()
    child1 = SceneGraph.SceneGraphNode()
    child2 = SceneGraph.SceneGraphNode()
    child3 = SceneGraph.SceneGraphNode()
    child4 = SceneGraph.SceneGraphNode()
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

    # NIN: GLSceneGraph -> SceneGraphNodeTreeItem graph
    ti = QtSceneGraphWidget.SceneGraphNodeTreeItem(glsg.gl_root_node, 
                                                   sgmodel_root)
    sgmodel_root.appendChild(ti)
    




    sys.exit(sgdialog.exec_())
