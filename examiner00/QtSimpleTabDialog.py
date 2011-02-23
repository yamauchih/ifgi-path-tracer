#!/usr/bin/env python

"""QtSimpleTabDialog

\author Yamauchi, Hitoshi
\file
\brief simple tab dialog"""

import sys
from PyQt4 import QtCore, QtGui

import QtGroupFrame
import QtWidgetIO

# QtSimpleTabDialog
class QtSimpleTabDialog(QtGui.QDialog):
    """QtSimpleTabDialog
    Simple (one) tab widget dialog
    Most of the user interaction will be done via this dialog.
    """

    def __init__(self, parent=None):
        """constructor"""

        super(QtSimpleTabDialog, self).__init__(parent)

        self.setModal(False);
        self.setMinimumWidth(0);

        # main widget: tab
        self.__tab_widget = QtGui.QTabWidget(self);

        # buttons: Apply, Update, OK, Close
        self.__apply_btn  = QtGui.QPushButton('Apply');
        self.__update_btn = QtGui.QPushButton('Update');
        self.__ok_btn     = QtGui.QPushButton('Ok');
        self.__close_btn  = QtGui.QPushButton('Close');

        self.__apply_btn. setDefault(False);
        self.__update_btn.setDefault(False);
        self.__ok_btn.    setDefault(False);
        self.__close_btn. setDefault(True);

        self.__button_box = QtGui.QDialogButtonBox(QtCore.Qt.Horizontal);

        self.__button_box.addButton(self.__apply_btn,
                                    QtGui.QDialogButtonBox.ActionRole)
        self.__button_box.addButton(self.__update_btn,
                                    QtGui.QDialogButtonBox.ActionRole)
        self.__button_box.addButton(self.__ok_btn,
                                    QtGui.QDialogButtonBox.AcceptRole)
        self.__button_box.addButton(self.__close_btn,
                                    QtGui.QDialogButtonBox.RejectRole)

        # connect signals
        self.__apply_btn. pressed.connect(self.slot_apply)
        self.__update_btn.pressed.connect(self.slot_updated)
        self.__ok_btn.    pressed.connect(self.slot_ok)
        self.__close_btn. pressed.connect(self.slot_closed)

        # layout
        self.__layout = QtGui.QVBoxLayout();
        self.__layout.setObjectName('QtSimpleTabDialog')
        self.__layout.setMargin(0);
        self.__layout.addWidget(self.__tab_widget)
        self.__layout.addWidget(self.__button_box)


        self.setLayout(self.__layout);
        self.resize(420,512);


    # slot_apply
    def slot_apply(self):
        """slot apply.
        called when apply button is pushed."""
        print 'DEBUG: slot_apply'

    # slot_updated
    def slot_updated(self):
        """slot updated.
        called when updated button is pushed."""
        print 'DEBUG: slot_updated'

    # slot_ok
    def slot_ok(self):
        """slot ok.
        called when ok button is pushed."""
        self.accept()

    # slot_closed
    def slot_closed(self):
        """slot closed.
        called when close button is pushed."""
        self.reject()


    # a signal emitted when dialog is closed
    def closed(self):
        """a signal emitted when dialog is closed"""

        print 'called QtSimpleTabDialog::closed() '

    # emits close(), override Dialog's closeEvent
    def closeEvent(self, _close_event):
        """signal emits close(), override Dialog's closeEvent
        and call super class's closeEvent().

        \param[in] _close_event close event"""

        self.closed()
        super(QtSimpleTabDialog, self).closeEvent(_close_event)


    def test_addtab(self, _tabname):
        """test add a tab"""
        frame     = QtGui.QFrame()
        boxlayout = QtGui.QHBoxLayout(frame)
        boxlayout.addSpacing(10)
        frame.setLayout(boxlayout)

        groupframe = QtGroupFrame.QtGroupFrame(frame, _tabname);
        boxlayout.addWidget(groupframe);

        opt = {}
        groupframe.add(QtWidgetIO.QtLineEditWIO(), 'myLineEdit', 'HelloWorld', opt)
        self.__tab_widget.addTab(frame, _tabname)


# test when called directly
if __name__ == '__main__':
    """test when called directly"""

    app = QtGui.QApplication(sys.argv)

    tab_dialog = QtSimpleTabDialog()
    tab_dialog.test_addtab('testtab1')
    tab_dialog.test_addtab('testtab2')

    tab_dialog.open()
    s = raw_input('Push return to finish: ')
    sys.exit()
