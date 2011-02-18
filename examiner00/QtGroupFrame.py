#!/usr/bin/env python

"""QtGroupFrame

\author Yamauchi, Hitoshi
\file
\brief group frame (QtIOWidget group)"""

import sys
from PyQt4 import QtCore, QtGui

# QtGroupFrame
class QtGroupFrame(QtGui.QScrollArea):
    """QtGroupFrame
    QtIOWidget group frame.
    \see QtIOWidget
    """

    def __init__(self, _parent, _groupname):
        """constructor.

        \param[in] _parent    parent widget.
        \param[in] _groupname group name.
        """
        super(QtGroupFrame, self).__init__(_parent)

        self.setObjectName('GroupFrame.' + _groupname)
        # too flexible, no scroll bar
        self.setWidgetResizable(True)

        self.__group_box = QtGui.QGroupBox(_groupname, self);
        # self.__group_box.setMinimumSize(MIN_WIDTH, MIN_HEIGHT)

        self.__grid_layout = QtGui.QGridLayout()
        self.__grid_layout.setSizeConstraint(QtGui.QLayout.SetMinimumSize);

        self.__group_box.setLayout(self.__grid_layout);

        # layout for this widget
        self.__main_vbox = QtGui.QVBoxLayout()
        self.__main_vbox.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.__main_vbox.addWidget(self.__group_box)

        self.setWidget(self.__group_box)

        super(QtGroupFrame, self).widget().setBackgroundRole(
            QtGui.QPalette.Window)



# test when called directly
# if __name__ == '__main__':
#     """test when called directly"""

#     app = QtGui.QApplication(sys.argv)

#     tab_dialog = QtGroupFrame()
#     tab_dialog.test_addtab('testtab1')
#     tab_dialog.test_addtab('testtab2')

#     tab_dialog.open()
#     s = raw_input('Push return to finish: ')
#     sys.exit()
