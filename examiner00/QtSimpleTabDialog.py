#!/usr/bin/env python
#
# Copyright (C) 2010-2011 Yamauchi, Hitoshi
#

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
    Simple (= one) tab widget dialog, but many tabs in the tab widget
    Most of the user interaction will be done via this dialog.
    """

    def __init__(self, parent=None):
        """constructor"""

        super(QtSimpleTabDialog, self).__init__(parent)

        self.setModal(False);
        self.setMinimumWidth(0);

        # main widget: tab
        self.__tab_widget     = QtGui.QTabWidget(self);

        # frame map: groupname -> Qframe (has a QtGroupFrame)
        self.__frame_map      = {}

        # group frame map: groupname -> QtGroupframe (has QIOWIdgets)
        self.__groupframe_map = {}

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


    def add_group(self, _group_name):
        """Add a group. This means creating a new tab and called it a group.
        The added group members will be contained in a new tab.
        The group is accessed by frame with the group name.

        Internal Widget/Layout hierarchy is:
        + newTab
          +-- QFrame
              +-- QHBoxLayout
                  +-- QtGroupFrame

        \param[in] _group_name a group name to be added.
        \return the added groupframe
        """
        if self.__frame_map.has_key(_group_name) == True:
            raise StandardError(_group_name + ' has been added.')

        frame     = QtGui.QFrame()
        boxlayout = QtGui.QHBoxLayout(frame)
        boxlayout.addSpacing(10)
        frame.setLayout(boxlayout)

        groupframe = QtGroupFrame.QtGroupFrame(frame, _group_name);
        boxlayout.addWidget(groupframe);

        self.__tab_widget.addTab(frame, _group_name)

        self.__frame_map[_group_name]      = frame
        self.__groupframe_map[_group_name] = groupframe

        return groupframe


    def remove_group(self, _group_name):
        """Remove a group. This means removing the tab associated
        with _group_name.
        \param[in] _group_name a group name to be removed.
        """
        if self.__frame_map.has_key(_group_name) == False:
            raise StandardError('no such group [' + _group_name + '].')

        self.__tab_widget.removeTab(
            self.__tab_widget.indexOf(self.__frame_map[_group_name]))
        del self.__frame_map[_group_name]
        del self.__groupframe_map[_group_name]


    def get_groupframe(self, _group_name):
        """Get a groupframe.
        \param[in] _group_name key of group frame.
        \return a QtGroupFrame associated with _group_name. None when
        no _group_name found.
        """
        return self.__groupframe_map.get(_group_name, None)


# test when called directly
if __name__ == '__main__':
    """test when called directly"""

    app = QtGui.QApplication(sys.argv)

    tab_dialog = QtSimpleTabDialog()

    gf0 = tab_dialog.add_group('testtab0')
    opt0 = {'LABEL': 'Hello'}
    gf0.add(QtWidgetIO.QtLineEditWIO(), 'myLineEdit', 'HelloWorld0', opt0)

    gf1 = tab_dialog.add_group('testtab1')
    opt1 = {'LABEL': 'This is for tab1.'}
    gf1.add(QtWidgetIO.QtLineEditWIO(), 'myLineEdit', 'HelloWorld1', opt1)

    tab_dialog.open()
    s = raw_input('Push return to finish: ')
    sys.exit()
