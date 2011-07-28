#!/usr/bin/env python
#
# Copyright (C) 2010-2011 Yamauchi, Hitoshi
#

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
    # MIN_WIDTH  = 300
    # MIN_HEIGHT = 300

    def __init__(self, _parent, _groupname):
        """constructor.

        \param[in] _parent    parent widget.
        \param[in] _groupname group name.
        """
        super(QtGroupFrame, self).__init__(_parent)

        self.setObjectName('GroupFrame.' + _groupname)
        # too flexible, no scroll bar
        self.setWidgetResizable(True)
        self.setSizePolicy(QtGui.QSizePolicy.Preferred,
                           QtGui.QSizePolicy.Preferred)


        self.__group_box = QtGui.QGroupBox(_groupname, self);
        # self.__group_box.setMinimumSize(300, 300)

        self.__grid_layout = QtGui.QGridLayout()
        self.__grid_layout.setSizeConstraint(QtGui.QLayout.SetMinimumSize);

        self.__group_box.setLayout(self.__grid_layout);

        # layout for this widget
        self.__main_vbox = QtGui.QVBoxLayout()
        self.__main_vbox.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.__main_vbox.addWidget(self.__group_box)
        self.setLayout(self.__main_vbox)

        self.setWidget(self.__group_box)

        super(QtGroupFrame, self).widget().setBackgroundRole(
            QtGui.QPalette.Window)

        # widget map
        self.__widgets = {}


    # add a QWidgetIO
    def add(self, _qwidgetio, _id, _value, _dict_opt):
        # d_initValues[_id] = _value

        # Widget hierarchy
        #  QtGroupFrame(= self) +-- QGroupBox(= self.__group_box)
        widget = _qwidgetio.create(_id, _value,
                                   self.__group_box,
                                   _id + ':' + _value)
        assert(widget != None)
        assert(_qwidgetio.get_widget() == widget)

        # have to copy parameter list, because we're extracting grid parameters
        # base::ParameterList opt = _opt;

        # extract grid position from parameter list
        nRows =  self.__grid_layout.rowCount()
        row = -1
        col = 0
        # if (opt.isDefined("X"))
        # {
        #   col = opt["X"];
        #   opt.remove("X");
        # }
        # if (opt.isDefined("Y"))
        # {
        #   row = opt["Y"];
        #   opt.remove("Y");
        # }

        # if only column is specified, stay in the current (last) row
        if (row == -1):
            if (col != 0):
                row = nRows -1
            else:
                row = nRows

        colTo = -1;
        rowTo = -1;
        # if (opt.isDefined("XTO"))
        # {
        #   colTo = opt["XTO"];
        #   opt.remove("XTO");
        # }
        # else
        colTo = col

        # if (opt.isDefined("YTO"))
        # {
        #   rowTo = opt["YTO"];
        #   opt.remove("YTO");
        # }
        # else
        rowTo = row

        _qwidgetio.apply_option(_dict_opt);
        _qwidgetio.set_value(_value);
        # _qwidgetio.->setObserver(self);

        # special hack for QPushButtons because it would be centered otherwise
        rowspan = rowTo - row + 1;
        colspan = colTo - col + 1;
        assert(rowspan > 0);
        assert(colspan > 0);

        # if (w->metaObject()->className() == "QPushButton"):
        #   self.__grid_layout.addWidget(w, row, col, rowspan, colspan,
        #                                Qt.AlignLeft)
        # else:
        self.__grid_layout.addWidget(widget, row, col, rowspan, colspan);

        widget.setParent(self.__group_box)

        # adjust the minimum size when a Widget is added.
        chrect = self.__group_box.childrenRect()

        self.__group_box.adjustSize()
        self.__group_box.updateGeometry()

        assert(_qwidgetio.get_widget() != None)

        # record the map
        self.__widgets[_id] = _qwidgetio;


    def get_widget_dict_key(self):
        """get QtWidgetIO widget dictionary's key().
        \return key list
        """
        return self.__widgets.keys()

    def get_widget(self, _widget_id):
        """get QtWidgetIO widget by widget_id.
        \return QIOWIdget
        """
        return self.__widgets[_id]

    def set_value(self, _widget_id, _value):
        """set widget_id widget value.
        \param[in] _widget_id widget id.
        \param[in] _value      value of widget_id widget.
        """
        if (not (_widget_id in self.__widgets)):
            raise StandardError('no such _widget_id [' + _widget_id + '] widget.')

        self.__widgets[_id].set_value(_value)

    def get_value(self, _widget_id):
        """get widget_id widget value.
        \param[in] _widget_id widget id.
        \return widget_id widget value.
        """
        if (not (_widget_id in self.__widgets)):
            raise StandardError('no such _widget_id [' + _widget_id + '] widget.')

        return self.__widgets[_id].get_value()


    def set_dict(self, _dict):
        """set all values in the _dict when the key is registered as
        a QtWidgetIO.

        \param[in] _dict widget's key and value dict.
        """
        for key in _dict:
            if key in self.__widgets:
                self.__widgets[key].set_value(_dict[key])



    def get_dict(self):
        """get all registered QtIOWidget {key, value} as a dict.
        \return all registered widget key values.
        """
        ret_dict = {}
        for w in self.__widgets:
            key = self.__widgets[w].get_key()
            val = self.__widgets[w].get_value()
            ret_dict[key] = val
            # print 'QtGroupFrame.get_dict: ', key, val

        return ret_dict




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
