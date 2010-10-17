#!/usr/bin/env python
#
# Examiner Window Application
#
# Menu etc.
#
# \author Yamauchi, Hitoshi
#

"""IFGI Examiner Window"""

import sys
import math
import OpenGL
import numpy

from PyQt4  import QtCore, QtGui, QtOpenGL
from OpenGL import GL
from OpenGL import GLU

import ExaminerWidget

class ExaminerWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(ExaminerWindow, self).__init__()

        widget = QtGui.QWidget()
        self.setCentralWidget(widget)

        # currently onle one widget is in the window
        self.examiner_widget = ExaminerWidget.ExaminerWidget()

        vbox = QtGui.QVBoxLayout()
        vbox.setMargin(5)
        vbox.addWidget(self.examiner_widget)
        widget.setLayout(vbox)

        self.createActions()
        self.createMenus()

        message = "ExaminerWindow ready"
        self.statusBar().showMessage(message)

        self.setWindowTitle("ExaminerWindow 0.0.0")
        self.setMinimumSize(100,100)
        self.resize(512,512)

        #     def contextMenuEvent(self, event):
        #         menu = QtGui.QMenu(self)
        #         menu.addAction(self.cutAct)
        #         menu.addAction(self.copyAct)
        #         menu.addAction(self.pasteAct)
        #         menu.exec_(event.globalPos())

    def menu_file_new(self):
        self.statusBar().showMessage('NIN: File--New invoked')

    def menu_file_open(self):
        self.statusBar().showMessage('NIN: File--Open invoked')

    def menu_process_ifgi_ptrace(self):
        self.statusBar().showMessage('NIN: Process--IFGI ptrace invoked')

    def menu_help_about(self):
        self.statusBar().showMessage('NIN: Help--About invoked')
        QtGui.QMessageBox.about(self, "About Menu",
                                'ExaminerWindow: simple OpenGL viewer for IFGI path ' +
                                'tracer<br>' +
                                'Author: Yamauchi, Hitoshi.')

    def createActions(self):
        self.newAct = QtGui.QAction("&New", self,
                                    shortcut=QtGui.QKeySequence.New,
                                    statusTip="Create a new scene",
                                    triggered=self.menu_file_new)

        self.openAct = QtGui.QAction("&Open...", self,
                                     shortcut=QtGui.QKeySequence.Open,
                                     statusTip="Open a file",
                                     triggered=self.menu_file_open)

        self.exitAct = QtGui.QAction("E&xit", self, shortcut="Ctrl+Q",
                                     statusTip="Exit the application",
                                     triggered=self.close)

        self.ifgi_ptraceAct = QtGui.QAction("&IFGI ptrace", self,
                                            # shortcut=QtGui.QKeySequence.Undo,
                                            statusTip="invoke the IFGI path tracer",
                                            triggered=self.menu_process_ifgi_ptrace)

        self.aboutAct = QtGui.QAction("&About", self,
                                      statusTip="Show the ExaminerWindow's About box",
                                      triggered=self.menu_help_about)


    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.newAct)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        self.processMenu = self.menuBar().addMenu("&Process")
        self.processMenu.addAction(self.ifgi_ptraceAct)

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)



#
# main
#
if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)
    window = ExaminerWindow()
    window.show()
    sys.exit(app.exec_())

