#!/usr/bin/env python

"""QtWidgetIOIF
\file
\brief interface of uniform input output QtWidget

These are interface and underneath widget implementation is in
QtExtWidget.py
"""

from PyQt4 import Qt, QtCore, QtGui
import QtExtWidget

# QtWidgetIOIF
class QtWidgetIOIF(QtCore.QObject):
    """QtWidgetIOIF

    QtWidgetIO interface.
    This provides a uniform interface of widget input/output.
    Set something with a dictionary.
    Get anything by a value.

    """

    # constructor
    def __init__(self, parent):
        """constructor

        \param[in] _parent parent Qt widget"""

        super(QtWidgetIOIF, self).__init__(parent)


    # create a io widget
    def create(self, _id, _value, _parent, _widget_name):
        """create this IO widget.
        \param[in] _id     widget id
        \param[in] _value  widget default value
        \param[in] _parent parent Qt widget
        \param[in] _widget_name widget name
        """
        raise StandardError ('Internal Error! must implemented in derived class.')

    # apply option
    def apply_option(self, _dict_opt):
        """apply options to customize after the creation.

        \param[in] _dict_opt options
        """
        raise StandardError ('Internal Error! must implemented in derived class.')

    # set value
    def set_value(self, _value):
        """set value to this widget.
        \param[in] _value value of this widget IO.
        """
        raise StandardError ('Internal Error! must implemented in derived class.')

    # get value
    def get_value(self):
        """get this widget's value.
        \return the value of IO widget.
        """
        raise StandardError ('Internal Error! must implemented in derived class.')

    # Qt widget implementation
    def get_widget(self):
        """get this widget's implementation.
        \return the Qt widget.
        """
        raise StandardError ('Internal Error! must implemented in derived class.')



# QtLineEditWIO
class QtLineEditWIO(QtWidgetIOIF):
    """Editing a line of text that has QtWidgetIOIF interface.

    Supported options:
    - \c LABEL the widget's label
    - \c VALIDATOR={QRegExp-pattern}<br>
         construct a base::QtWidgets::QRegExpValidator
    - \c STRICT={0,1}<br>
         enable/disable strict syntax checking if validator is provided
    - \c MINLEN minimum length of input, validator must be provided
    - \c MAXLEN maximum length of input, no validator must be provided
    - \c PARANOIA={0,1}<br>
         Notify observer any time the QLineEdit changed (signal
	 QLineEdit::textChanged()). \a Note: Notification is done only
	 if the text is \a QValidator::Acceptable in case that a validator
	 is provided!
    \a Note: Use mkOpt() to construct options list.<br>
    """

    # constructor
    def __init__(self):
        """constructor"""
        self.__extwidget = None


    # create a io widget
    def create(self, _id, _value, _parent, _widget_name):
        """create this IO widget.
        \param[in] _id     widget id
        \param[in] _value  widget default value
        \param[in] _parent parent Qt widget
        \param[in] _widget_name widget name
        """
        self.__extwidget = QtExtWidget.QtExtTextLine('MyLabel', _parent,
                                                     QtCore.Qt.Horizontal)
        return self.__extwidget


    # apply option
    def apply_option(self, _dict_opt):
        """apply options to customize after the creation.

        \param[in] _dict_opt options
        """
        if 'LABEL' in _dict_opt:
            self.__extwidget.set_label(_dict_opt['LABEL'])

    # set value
    def set_value(self, _value):
        """set value to this widget.
        \param[in] _value value of this widget IO.
        """
        self.__extwidget.set_value(_value)

    # get value
    def get_value(self):
        """get this widget's value.
        \return the value of IO widget.
        """
        return self.__extwidget.get_value()


    # Qt widget implementation
    def get_widget(self):
        """get this widget's implementation.
        \return the Qt widget.
        """
        return self.__extwidget

    # slot for returnPressed() signal
    # def slotUpdate(self, _text)
