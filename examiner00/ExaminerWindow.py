#!/usr/bin/env python
#
# Examiner Window Application
#
# Menu etc.
#
# \author Yamauchi, Hitoshi
#

"""IFGI Examiner Window"""

import math
import numpy
import optparse
import os
import sys

import OpenGL

from PyQt4  import QtCore, QtGui, QtOpenGL
from OpenGL import GL
from OpenGL import GLU

import ExaminerWidget
import SceneGraph
import GLSceneGraph

class ExaminerWindow(QtGui.QMainWindow):
    # constructor
    def __init__(self, parent=None):
        super(ExaminerWindow, self).__init__()
        self.examiner_widget = None

    # create widgets and window
    def create_window(self):
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


    # init application after window is created.
    #
    # call after the window are created. Usually, this set up the
    # application, like commanline specify some commands. (for
    # example, load scene)
    # \param[in] _cmd_opt command line option created by optparse
    def init_app(self, _cmd_opt):
        if self.examiner_widget == None:
            raise StandardError, ('No examiner widget. have you call create_window?')

        # load a file
        if _cmd_opt.infilename != '':
            self.com_load_file(_cmd_opt.infilename)

        # other command will be here.

    #----------------------------------------------------------------------
    # Menu bar
    #----------------------------------------------------------------------

    # File--New
    def menu_file_new(self):
        self.statusBar().showMessage('NIN: File--New invoked')

    # File--Open
    def menu_file_open(self):
        options = QtGui.QFileDialog.Options()
        # if not self.native.isChecked():
        options |= QtGui.QFileDialog.DontUseNativeDialog
        fileName = QtGui.QFileDialog.getOpenFileName(self,
                                                     "Open a scene file",
                                                     '', # use last selected item
                                                     '', #
                                                     "All Files (*);;obj Files (*.obj)",
                                                     options)
        if fileName:
            print 'fileName = ' + fileName
        else:
            print 'canceled'
            self.statusBar().showMessage('File--Open: cancelled')
            return

        self.com_load_file(fileName)

        self.statusBar().showMessage('File--Open [' + fileName + ']')

    # Process--IFGI ptrace
    def menu_process_ifgi_ptrace(self):
        self.statusBar().showMessage('NIN: Process--IFGI ptrace invoked')

    # Help--about
    def menu_help_about(self):
        self.statusBar().showMessage('NIN: Help--About invoked')
        QtGui.QMessageBox.about(self, "About Menu",
                                'ExaminerWindow: simple OpenGL viewer for IFGI path ' +
                                'tracer<br>' +
                                'Author: Yamauchi, Hitoshi.')
    # create menubar actions
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

    # create menubar
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


    #----------------------------------------------------------------------
    # command action implementation
    #----------------------------------------------------------------------

    # load file command
    def com_load_file(self, _infilename):
        if (_infilename == None) or (_infilename == ''):
            raise StandardError, ('com_load_file: emoty filename')

        # got the filename, create a generic scene graph
        sg = SceneGraph.create_one_trimeh_scenegraph(_infilename)
        sg.print_obj()          # for debug

        # attach the GL scene graph to SceneGraph
        glsg = GLSceneGraph.GLSceneGraph()
        glsg.set_scenegraph(sg)

        # debug mode on
        self.examiner_widget.set_debug_mode(True)

        # attach the GL scene graph to Examiner to see
        self.examiner_widget.attach_gl_scenegraph(glsg)





# get default option list
# \return default option list
def get_default_option_list():
    default_option_list = [
        optparse.make_option("-v", "--verbose", action="store_true", dest="verbose",
                             default=False,
                             help="verbose mode."
                             "[default %default]"
                             ),
        optparse.make_option("-i", "--infile", action="store", dest="infilename",
                             default='',
                             help="input scene file name."
                             "[default [%default]]"
                             )
        ]
    return default_option_list


#
# main
#
if __name__ == '__main__':
    # parse command line
    arg_parser = optparse.OptionParser(option_list = get_default_option_list(),
                                       version="%prog 0.1.0")
    (cmd_options, args) = arg_parser.parse_args()

    app = QtGui.QApplication(sys.argv)
    win = ExaminerWindow()
    win.create_window()
    win.init_app(cmd_options)
    win.show()
    sys.exit(app.exec_())

