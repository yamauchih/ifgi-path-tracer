#!/usr/bin/env python
#
# QtExaminer widget version 0.0.0
#
# \author Yamauchi, Hitoshi
#

"""IFGI QtSceneGraphDialog Version 0.0.0"""

import sys
import QtSceneGraphWidget

from PyQt4 import QtCore, QtGui

# QtSceneGraphDialog
#
# SceneGraph viewer dialog
#
class QtSceneGraphDialog(QtGui.QDialog):

    # constructor
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




    # emitted when dialog is closed
    def closed(self):
        print 'called QtSceneGraphWidget::closed() '

    # Clear current view and import scene graph _root.
    # Calls sceneGraphViewer()'s update() method.
    def update(self, _sceneGraphRoot):
        print 'QtSceneGraphWidget::update called'

    # emits close(), override Dialog's closeEvent
    # and call super class closeEvent()
    #
    # \param[in] _close_event close event
    def closeEvent(self, _close_event):
        self.closed()
        super(QtSceneGraphDialog, self).closeEvent(_close_event)








if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    sgdialog = QtSceneGraphDialog()
    sys.exit(sgdialog.exec_())
