#!/usr/bin/env python
#
# Copyright (C) 2010-2011 Yamauchi, Hitoshi
#

"""QtExtWidget
\file
\brief Qt extented widget set for QtWidgetIO
\see QtWidgetIO
"""

from PyQt4 import Qt, QtCore, QtGui

# QtExtTextLine
class QtExtTextLine(QtGui.QWidget):
    """QtExtTextLine

    Qt extended text line widget for QtWidgetIO

    The widget structure is: LABEL [text input line]
    """

    # constructor
    def __init__(self, _label, _parent, _orientation):
        """constructor

        \param[in] _label  text label
        \param[in] _parent parent Qt widget
        \param[in] _orientation widget orientation (Horizontal, Vertical)
        """

        super(QtExtTextLine, self).__init__(_parent)

        self.__label = QtGui.QLabel(self)
        self.__label.setObjectName(_label + '.valueLabel')
        self.__text  = QtGui.QLineEdit(self)
        self.__text.setObjectName(_label  + '.valueEdit')

        # connect signals
        self.__text.textChanged.  connect(self.slotChanged)
        self.__text.returnPressed.connect(self.slotReturnPressed)
        # DELETEME self.__text.lostFocus.    connect(self.slotReturnPressed)

        hspacing = 10
        self.__orientation = _orientation
        if (self.__orientation == QtCore.Qt.Horizontal):
            self.__layout = QtGui.QHBoxLayout(self)
            self.__layout.addWidget(self.__label)

        else:
            hspacing = 4
            self.__layout = GtGui.QVBoxLayout(self);
            self.__layout.addWidget(self.__label, 0);

        self.__layout.addSpacing(hspacing);
        self.__layout.addWidget(self.__text);
        self.__layout.activate();

        self.setLayout(self.__layout);


    # Sets the widget's label.
    def set_label(self, _label):
        """set the widget's label
        \param[in] _label label text"""
        self.__label.setText(_label)
        self.__label.setMinimumSize(self.__label.sizeHint())

    # Sets the validator of the lineEdit widget
    def set_validator(self, _validator):
        """Sets the validator of the lineEdit widget.
        \param[in] _validator text validator."""
        self.__text.setValidator(_validator)

    # Returns the validator.
    def get_validator():
        """get current validator.
        \return validator currentry associated with the text."""
        return self.__text.validator()

    # Sets the maximum length of accepted strings.
    def set_max_length(self, _length):
        """Sets the maximum length of accepted strings.
        \param[in] _length max length to be set.
        """
        self.__text.setMaxLength(_length)

    # returns the currently entered Text
    def get_value(self):
        """returns the currently entered Text
        \return value of this widget IO, text.
        """
        res = self.__text.text();
        if res.isEmpty():
            return ''
        return ret;

    # set value
    def set_value(self, _text):
        """set value of this ext wiegdt.
        \param[in] _text text to set"""
        self.__text.clear()
        self.__text.setText(_text)

    # slot changed
    def slotChanged(self, _text):
        """
        """
        res = self.__text.text()
        if (not res.isEmpty()):
            self.textChanged(res)

    # slot return pressed
    def slotReturnPressed(self):
        print 'NIN: slotReturnPressed'
    #     res = self.__text.text();
    #     if (not res.isEmpty()):
    #         emit self.returnPressed(res)


    #--- signals

    def textChanged(self, _text):
        print 'textChanged signal'

    def returnPressed(self, _text):
        print 'returnPressed signal'

