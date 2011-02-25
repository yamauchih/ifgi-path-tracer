#!/usr/bin/env python
"""Examiner Window Application

\file
\brief geometry examiner window
\author Yamauchi, Hitoshi
"""

import math
import numpy
import optparse
import os
import sys

import OpenGL

from PyQt4  import QtCore, QtGui, QtOpenGL
from OpenGL import GL
from OpenGL import GLU

import QtExaminerWidget
import SceneGraph
import GLSceneGraph
import QtSceneGraphDialog

# examiner window
class QtExaminerWindow(QtGui.QMainWindow):
    """Qt geometry examiner window."""

    # constructor
    def __init__(self, parent=None):
        """constructor"""
        super(QtExaminerWindow, self).__init__()
        self.__examiner_widget = None

    # create widgets and window
    def create_window(self):
        """create widgets and window."""
        widget = QtGui.QWidget()
        self.setCentralWidget(widget)

        # currently onle one widget is in the window
        self.__examiner_widget = QtExaminerWidget.QtExaminerWidget()

        vbox = QtGui.QVBoxLayout()
        vbox.setMargin(5)
        vbox.addWidget(self.__examiner_widget)
        widget.setLayout(vbox)

        self.createActions()
        self.createMenus()

        message = "QtExaminerWindow ready"
        self.statusBar().showMessage(message)

        self.setWindowTitle("QtExaminerWindow 0.0.0")
        self.setMinimumSize(100,100)
        self.resize(512,512)

        #     def contextMenuEvent(self, event):
        #         menu = QtGui.QMenu(self)
        #         menu.addAction(self.cutAct)
        #         menu.addAction(self.copyAct)
        #         menu.addAction(self.pasteAct)
        #         menu.exec_(event.globalPos())


    # init application after window is created.
    def init_app(self, _cmd_opt):
        """init application after window is created.

        call after the window are created. Usually, this set up the
        application, like commanline specify some commands. (for
        example, load scene)
        \param[in] _cmd_opt command line option created by optparse
        """


        if self.__examiner_widget == None:
            raise StandardError, ('No examiner widget. have you call create_window?')

        # load a file
        if _cmd_opt.infilename != '':
            self.com_file_load(_cmd_opt.infilename)

        # other command will be here.

    #----------------------------------------------------------------------
    # Menu bar
    #----------------------------------------------------------------------

    # File--New
    def menu_file_new(self):
        """File--New menu."""
        self.com_file_new()
        self.statusBar().showMessage('File--New invoked')

    # File--Open
    def menu_file_open(self):
        """File--Open menu."""
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

        self.com_file_load(fileName)

        self.statusBar().showMessage('File--Open [' + fileName + ']')


    # View -- move mode
    def menu_view_move(self):
        """View -- move mode."""
        print 'NIN: menu_view_move'

    # View -- move mode
    def menu_view_move(self):
        """View -- move mode."""
        print 'NIN: menu_view_move'

    # View -- move mode
    def menu_view_move(self):
        """View -- move mode."""
        print 'NIN: menu_view_move'

    # View -- move mode
    def menu_view_move(self):
        """View -- move mode."""
        print 'NIN: menu_view_move'

    # View -- move mode
    def menu_view_move(self):
        """View -- move mode."""
        print 'NIN: menu_view_move'

    # View -- pick mode
    def menu_view_pick(self):
        """View -- pick mode."""
        print 'NIN: menu_view_pick'

    # View -- lasso mode
    def menu_view_lasso(self):
        """View -- lasso mode."""
        print 'NIN: menu_view_lasso'

    # View -- identify mode
    def menu_view_identify(self):
        """View -- identify mode."""
        print 'NIN: menu_view_identify'

    # View -- restore home
    def menu_view_restorehome(self):
        """View -- restore home."""
        print 'NIN: menu_view_restorehome'

    # View -- set home
    def menu_view_sethome(self):
        """View -- set home."""
        print 'NIN: menu_view_sethome'
        # sgdialog = QtSceneGraphDialog()

    # View -- all
    def menu_view_all(self):
        """View -- all."""
        self.__examiner_widget.view_all()

    # View -- toggle perspective
    def menu_view_toggle_perspective(self):
        """View -- toggle perspective."""
        print 'NIN: menu_view_toggle_perspective'

    # View -- scenegraph
    def menu_view_scenegraph(self):
        """View -- scenegraph."""
        print 'DEBUG: menu_view_scenegraph'
        glsg = self.__examiner_widget.peek_gl_scenegraph()

        # import gl scenegraph to dialog -> treeview widget -> model/view
        self.__sgdialog = QtSceneGraphDialog.QtSceneGraphDialog()
        self.__sgdialog.update_scenegraph(glsg)

        self.__sgdialog.show()



    # Process--IFGI ptrace
    def menu_process_ifgi_ptrace(self):
        """Process--IFGI ptrace."""
        self.statusBar().showMessage('NIN: Process--IFGI ptrace invoked')

    # Help--about
    def menu_help_about(self):
        """Help--about."""
        self.statusBar().showMessage('NIN: Help--About invoked')
        QtGui.QMessageBox.about(self, "About Menu",
                                'QtExaminerWindow: simple OpenGL viewer for ' +
                                'IFGI path tracer<br>' +
                                'Author: Yamauchi, Hitoshi.')
    # create menubar actions
    def createActions(self):
        """create menubar actions."""

        # File menu
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

        # View menu -- view mode
        self.viewMoveAct = QtGui.QAction("Examine mode", self, # shortcut="Ctrl+M",
                                         checkable=True,
                                         statusTip="Examine object mode (Trackball)",
                                         triggered=self.menu_view_move)
        self.viewPickAct = QtGui.QAction("Picking mode", self, # shortcut="Ctrl+M",
                                         checkable=True,
                                         statusTip="Picking mode",
                                         triggered=self.menu_view_pick)
        self.viewLassoAct = QtGui.QAction("Lasso mode", self, # shortcut="Ctrl+M",
                                          checkable=True,
                                          statusTip="Lasso mode",
                                          triggered=self.menu_view_lasso)
        self.viewIdentifyAct = QtGui.QAction("Identify mode", self, # shortcut="Ctrl+M",
                                             checkable=True,
                                             statusTip="Identify mode",
                                             triggered=self.menu_view_identify)
        # make these a group (radio button)
        self.viewModeGroup = QtGui.QActionGroup(self)
        self.viewModeGroup.addAction(self.viewMoveAct)
        self.viewModeGroup.addAction(self.viewPickAct)
        self.viewModeGroup.addAction(self.viewLassoAct)
        self.viewModeGroup.addAction(self.viewIdentifyAct)
        self.viewMoveAct.setChecked(True) # default mode

        # View menu -- change view related
        self.viewRestoreHomeyAct = QtGui.QAction("Restore Home", self,
                                                 statusTip="Restore the home view",
                                                 triggered=self.menu_view_restorehome)
        self.viewSetHomeyAct = QtGui.QAction("Set home", self,
                                             statusTip="Set current view to home",
                                             triggered=self.menu_view_sethome)
        self.viewViewallAct = QtGui.QAction("View all", self,
                                            statusTip="View whole scene",
                                            triggered=self.menu_view_all)
        self.viewTogglePerspectiveAct = QtGui.QAction(
            "Toggle Perspective", self,
            checkable=True,
            statusTip="Toggle Perspective and Orthogonal view",
            triggered=self.menu_view_toggle_perspective)
        # default perspective FIXME check camera
        self.viewTogglePerspectiveAct.setChecked(True)

        self.viewScenegraphAct = QtGui.QAction("Show scene graph", self,
                                               statusTip="Show scenegraph control",
                                               triggered=self.menu_view_scenegraph)


        # Process menu
        self.ifgi_ptraceAct = QtGui.QAction("&IFGI ptrace", self,
                                            # shortcut=QtGui.QKeySequence.Undo,
                                            statusTip="invoke the IFGI path tracer",
                                            triggered=self.menu_process_ifgi_ptrace)

        # Help menu
        self.aboutAct = QtGui.QAction("&About", self,
                                      statusTip="Show the QtExaminerWindow's About box",
                                      triggered=self.menu_help_about)

    # create menubar
    def createMenus(self):
        """create menubar."""
        # file menu
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.newAct)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        # view menu
        self.viewMenu = self.menuBar().addMenu("&View")
        self.viewMenu.addAction(self.viewMoveAct)
        self.viewMenu.addAction(self.viewPickAct)
        self.viewMenu.addAction(self.viewLassoAct)
        self.viewMenu.addAction(self.viewIdentifyAct)
        self.viewMenu.addSeparator()
        self.viewMenu.addAction(self.viewRestoreHomeyAct)
        self.viewMenu.addAction(self.viewSetHomeyAct)
        self.viewMenu.addAction(self.viewViewallAct)
        self.viewMenu.addAction(self.viewTogglePerspectiveAct)
        self.viewMenu.addSeparator()
        self.viewMenu.addAction(self.viewScenegraphAct)

        # process menu
        self.processMenu = self.menuBar().addMenu("&Process")
        self.processMenu.addAction(self.ifgi_ptraceAct)

        # help menu
        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)


    #----------------------------------------------------------------------
    # command action implementation
    #----------------------------------------------------------------------

    # load file command
    def com_file_new(self):
        """file new command.
        create empty scenegraph and set it to examiner widget.
        """
        # create an empty scenegraph
        sg = SceneGraph.create_empty_scenegraph()

        # attach the SceneGraph to a GLSceneGraph
        glsg = GLSceneGraph.GLSceneGraph()
        glsg.set_scenegraph(sg)

        # debug mode on
        self.__examiner_widget.set_debug_mode(True)

        # attach the GLSceneGraph to Examiner to see
        self.__examiner_widget.attach_gl_scenegraph(glsg)


    # load file command
    def com_file_load(self, _infilename):
        """load file command."""
        if (_infilename == None) or (_infilename == ''):
            raise StandardError, ('com_file_load: empty filename')

        # got the filename, create a generic scene graph
        sg = SceneGraph.create_one_trimeh_scenegraph(_infilename)
        sg.update_all_bbox()
        sg.print_all_obj()      # for debug

        # attach the SceneGraph to a GLSceneGraph
        glsg = GLSceneGraph.GLSceneGraph()
        glsg.set_scenegraph(sg)

        # debug mode on
        self.__examiner_widget.set_debug_mode(True)

        # attach the GLSceneGraph to Examiner to see
        self.__examiner_widget.attach_gl_scenegraph(glsg)
        self.__examiner_widget.view_all()


# get default option list
def get_default_option_list():
    """get default option list.
    \return default option list"""

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


# main
if __name__ == '__main__':
    # parse command line
    arg_parser = optparse.OptionParser(option_list = get_default_option_list(),
                                       version="%prog 0.1.0")
    (cmd_options, args) = arg_parser.parse_args()

    app = QtGui.QApplication(sys.argv)
    win = QtExaminerWindow()
    win.create_window()
    win.init_app(cmd_options)
    win.show()
    sys.exit(app.exec_())

