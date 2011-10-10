#!/usr/bin/env python
#
# Copyright (C) 2010-2011 Yamauchi, Hitoshi
#

"""QtSceneGraphDialog

\author Yamauchi, Hitoshi
\file
\brief scene graph inspector dialog pyqt implementtaion"""

import sys

from PySide import QtCore, QtGui
from ifgi.scene import SceneGraph, Primitive

import QtSceneGraphWidget, GLSceneGraph

# QtSceneGraphDialog
class QtSceneGraphDialog(QtGui.QDialog):
    """QtSceneGraphDialog
    SceneGraph viewer dialog"""

    # signal definition
    signal_closed = QtCore.Signal(object)

    def __init__(self, _parent):
        """constructor"""

        super(QtSceneGraphDialog, self).__init__(_parent)

        # scenegraph treeview widget
        self.__sg_view_widget = \
            QtSceneGraphWidget.QtSceneGraphViewWidget(self, self);

        self.__layout = QtGui.QVBoxLayout();
        self.__layout.setObjectName('SceneGraph viewer, dialog layout');
        self.__layout.setMargin(0);
        self.__layout.addWidget(self.__sg_view_widget);
        self.setLayout(self.__layout);
        self.resize(450, 300)

        # only works with show(), exec_() will override
        self.setModal(False)
        self.setWindowModality(QtCore.Qt.NonModal)


    # get scenegraph treeview widget
    def get_scenegraph_view_widget(self):
        return self.__sg_view_widget

    # a signal emitted when dialog is closed
    def closed(self):
        """a signal emitted when dialog is closed"""
        self.signal_closed.emit('QtSceneGraphDialog.closed')
        # print 'called QtSceneGraphWidget::closed() '


    # Clear current view and import GL scenegraph.
    def update_scenegraph(self, _gl_scenegraph):
        """import _gl_scenegraph and update model and view.
        \param[in] _gl_scenegraph GL scenegraph.
        """
        self.__sg_view_widget.update_scenegraph(_gl_scenegraph)



    # emits close(), override Dialog's closeEvent
    def closeEvent(self, _close_event):
        """signal emits close(), override Dialog's closeEvent
        and call super class's closeEvent().

        \param[in] _close_event close event"""

        self.closed()
        super(QtSceneGraphDialog, self).closeEvent(_close_event)


# test when called directly
if __name__ == '__main__':
    """test when called directly"""

    app = QtGui.QApplication(sys.argv)

    sgdialog = QtSceneGraphDialog(None)

    # sgmodel_root = sgdialog.get_scenegraph_view_widget().get_scenegraph_model(). \
    #     get_scenegraph_model_root()

    #----------------------------------------------------------------------
    # 1. create a SceneGraph
    #
    # This SceneGraph is independent from GLSceneGraph (can be used
    # for tracer)
    sg = SceneGraph.SceneGraph()
    assert(sg.get_root_node() == None)

    # create scenegraph's root node
    #   simplest example: root scenegraph node only
    rootsgnode = SceneGraph.SceneGraphNode('sgroot')
    sg.set_root_node(rootsgnode)

    # create a scenegraph
    #
    # + rootnode + child0 (camera)
    #            + child1
    #            + child2
    #            + child3 + child4 + primitive
    #

    # set camera. Camera is a special node.
    child0 = SceneGraph.CameraNode('camera')
    rootsgnode.append_child(child0)
    sg.set_current_camera(child0.get_camera())

    child1 = SceneGraph.SceneGraphNode('child1')
    child2 = SceneGraph.SceneGraphNode('child2')
    child3 = SceneGraph.SceneGraphNode('child3')
    prim0  = Primitive.TriMesh()
    child4 = SceneGraph.PrimitiveNode('child4', prim0)


    rootsgnode.append_child(child1)
    rootsgnode.append_child(child2)
    rootsgnode.append_child(child3)

    child3.append_child(child4)

    #----------------------------------------------------------------------
    # 2. create a GLSceneGraph
    #
    # attach the SceneGraph to a GLSceneGraph
    glsg = GLSceneGraph.GLSceneGraph()
    glsg.set_scenegraph(sg)

    # import gl scenegraph to dialog -> treeview widget -> model/view
    sgdialog.update_scenegraph(glsg)

    sgdialog.show()
    s = raw_input('Push return to exit: ')
    sys.exit()
