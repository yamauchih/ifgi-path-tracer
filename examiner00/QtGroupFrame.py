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

    # add a QWidgetIO
    def add(self, _qwidgetio, _id, _value, _dict_opt):
        # d_initValues[_id] = _value

        # Widget hierarchy
        #  QGroupFrame(= self) +-- QGroupBox(= self.__group_box)
        widget = _qwidgetio.create(_id, _value,
                                   self.__group_box,
                                   _id + ':' + _value)
        assert(widget != None)
        assert(_qwidgetio.get_widget() == widget)

        # have to copy parameter list, because we're extracting grid parameters
        # base::ParameterList opt = _opt;

        # // extract grid position from parameter list
        # int nRows =  d_pGrid->rowCount();
        # int row = -1;
        # int col = 0;
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

        # // if only column is specified, stay in the current (last) row
        # if (row == -1)
        #   if (col != 0)
        #     row = nRows -1;
        #   else
        #     row = nRows;

        # int colTo = -1;
        # int rowTo = -1;
        # if (opt.isDefined("XTO"))
        # {
        #   colTo = opt["XTO"];
        #   opt.remove("XTO");
        # }
        # else colTo = col;

        # if (opt.isDefined("YTO"))
        # {
        #   rowTo = opt["YTO"];
        #   opt.remove("YTO");
        # }
        # else rowTo = row;

        # _interface->applyOptions(opt);
        # _interface->value( _value );

        # _interface->setObserver(this);

        # // special hack for QPushButtons because it would be centered otherwise
        # int rowspan = rowTo - row + 1;
        # int colspan = colTo - col + 1;
        # assert(rowspan > 0);
        # assert(colspan > 0);

        # if (w->metaObject()->className() == "QPushButton"){
        #   d_pGrid->addWidget(w, row, col, rowspan, colspan, Qt::AlignLeft);
        # }
        # else {
        #   d_pGrid->addWidget(w, row, col, rowspan, colspan);
        # }

        widget.setParent(self.__group_box)

        # // adjust the minimum size when a Widget is added.
        chrect = self.__group_box.childrenRect()

        self.__group_box.adjustSize()
        self.__group_box.updateGeometry()

        assert(_qwidgetio.get_widget() != None)
        # d_widgets[_id]=_interface;




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
