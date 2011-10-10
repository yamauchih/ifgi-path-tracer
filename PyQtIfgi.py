#!/usr/bin/env python
"""Qt ifgi path tracer

\file
\brief ifgi path tracer with Qt examiner GUI
\author Yamauchi, Hitoshi
"""

import optparse
import sys
from PyQt4  import QtCore, QtGui, QtOpenGL
from examiner00 import QtExaminerWindow

# main
if __name__ == '__main__':
    # parse command line
    arg_parser = optparse.OptionParser(option_list =
                                       QtExaminerWindow.get_default_option_list(),
                                       version="%prog 0.1.0")
    (cmd_options, args) = arg_parser.parse_args()

    app = QtGui.QApplication(sys.argv)
    win = QtExaminerWindow.QtExaminerWindow()
    win.create_window()
    win.init_app(cmd_options)
    win.show()
    sys.exit(app.exec_())

