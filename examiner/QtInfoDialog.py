#!/usr/bin/env python
#
# Copyright (C) 2010-2011 Yamauchi, Hitoshi
#

"""QtInfoDialog

\author Yamauchi, Hitoshi
\file
\brief general infomation dialog"""

import sys
from PySide import QtCore, QtGui

# QtInfoDialog
class QtInfoDialog(QtGui.QDialog):
    """QtInfoDialog
    general information dialog"""

    def __init__(self, parent=None):
        """constructor"""

        super(QtInfoDialog, self).__init__(parent)

        self.setModal(False);

        self.setMinimumWidth(0);

        # main text
        self.__info_text = QtGui.QTextEdit(self);

        # buttons
        self.__update_btn = QtGui.QPushButton('Update');
        self.__update_btn.setDefault(False);
        self.__close_btn  = QtGui.QPushButton('Close');
        self.__close_btn.setDefault(True);
        self.__button_box = QtGui.QDialogButtonBox(QtCore.Qt.Horizontal);
        self.__button_box.addButton(self.__update_btn,
                                    QtGui.QDialogButtonBox.ActionRole)
        self.__button_box.addButton(self.__close_btn,
                                    QtGui.QDialogButtonBox.AcceptRole)
        # connect signals
        self.__close_btn. pressed.connect(self.slot_closed)
        self.__update_btn.pressed.connect(self.slot_updated)


        # layout
        self.__layout = QtGui.QVBoxLayout();
        self.__layout.setObjectName('Information dialog')
        self.__layout.setContentsMargins(0, 0, 0, 0);
        self.__layout.addWidget(self.__info_text)
        self.__layout.addWidget(self.__button_box)


        self.setLayout(self.__layout);
        self.resize(420,512);

    # set html text to this info
    def set_html(self, _html_txt):
        """set html text to this information dialog.
        \param[in] _html_txt html text to show.
        """
        self.__info_text.setHtml(_html_txt)


    # slot_closed
    def slot_closed(self):
        """slot closed.
        called when close button is pushed."""
        self.accept()

    # slot_updated
    def slot_updated(self):
        """slot updated.
        called when updated button is pushed."""
        print 'DEBUG: slot_updated'

    # a signal emitted when dialog is closed
    def closed(self):
        """a signal emitted when dialog is closed"""

        print 'called QtInfoDialog::closed() '

    # emits close(), override Dialog's closeEvent
    def closeEvent(self, _close_event):
        """signal emits close(), override Dialog's closeEvent
        and call super class's closeEvent().

        \param[in] _close_event close event"""

        self.closed()
        super(QtInfoDialog, self).closeEvent(_close_event)


# test when called directly
if __name__ == '__main__':
    """test when called directly"""

    app = QtGui.QApplication(sys.argv)

    info_dialog = QtInfoDialog()
    info_dialog.set_html(
        '''
<HTML lang="en">
<HEAD>
<TITLE>Example Info dialog</TITLE>
</HEAD>
<BODY>

<h2>simple path tracer</h2>

<hr>

<ul>
 <li>Here is an unordered list.
 <ul>
   <li>IFGI
   <li>path
   <li>tracer
 </ul>
</ul>

<hr>
<address>
Copyright (C) 2010-2011 Yamauchi, Hitoshi<BR>
</address>
</BODY>
</HTML>
''')

    # info_dialog.setModal(False)
    info_dialog.open()
    s = raw_input('Push return to finish: ')
    sys.exit()
