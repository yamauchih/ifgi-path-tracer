#!/usr/bin/env python
#
# Copyright (C) 2010-2011 Yamauchi, Hitoshi
#

"""QtWidgetIOIF
\file
\brief interface of uniform input output QtWidget

These are interface and underneath widget implementation is in
QtExtWidget.py
"""

from PyQt4 import Qt, QtCore, QtGui
import QtExtWidget

#----------------------------------------------------------------------

class QtWidgetIOIF(QtCore.QObject):
    """QtWidgetIOIF

    \ingroup qtwidgetio

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

    def get_key(self):
        """get this widget's key (id).
        \return the key ID of this widget.
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


#----------------------------------------------------------------------

class QtWidgetIOObserverIF(object):
    """QtWidgetIOObserverIF widget observer interface.

    \ingroup qtwidgetio

    Interface for a class that observes a QtWidgetIOIF instance.
    The method update() changes the QtWidgetIOIF instance state.
    """

    def __init__(self):
        """constructor
        """
        pass

    def update(self, _arg):
        """interface method.
        \param[in] _arg a general argument
        """
        raise StandardError('This method must be reimplemented.')


#----------------------------------------------------------------------

# NIN class QtColorButton(QtWidgetIOIF)
# NIN class QtFileButton(QtWidgetIOIF)


class QtLineEditWIO(QtWidgetIOIF):
    """Editing a line of text that has QtWidgetIOIF interface.
    \ingroup qtwidget
    Supported options:
    - \c LABEL the widget's label
    - \c NIN VALIDATOR={QRegExp-pattern}<br>
         construct a base::QtWidgets::QRegExpValidator
    - \c NIN STRICT={0,1}<br>
         enable/disable strict syntax checking if validator is provided
    - \c NIN MINLEN minimum length of input, validator must be provided
    - \c NIN MAXLEN maximum length of input, no validator must be provided
    - \c NIN PARANOIA={0,1}<br>
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
        self.__keyid = ''


    # create a io widget
    def create(self, _id, _value, _parent, _widget_name):
        """create this IO widget.
        \param[in] _id     widget id
        \param[in] _value  widget default value
        \param[in] _parent parent Qt widget
        \param[in] _widget_name widget name
        """
        self.__extwidget = QtExtWidget.QtExtTextLine(_id, _parent,
                                                     QtCore.Qt.Horizontal)
        self.__keyid = _id
        return self.__extwidget


    # apply option
    def apply_option(self, _dict_opt):
        """apply options to customize after the creation.

        \param[in] _dict_opt options
        """
        if 'LABEL' in _dict_opt:
            self.__extwidget.set_label(_dict_opt['LABEL'])

    def get_key(self):
        """get this widget's key (id).
        \return the key ID of this widget.
        """
        return self.__keyid

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


# NIN class QtScalarSlider(QtWidgetIOIF)

#----------------------------------------------------------------------

class QtToggleButton(QtWidgetIOIF):
    """Toggle button (one check box) with QtWidgetIOIF interface.
    \ingroup qtwidget
    Supported options:
    - LABEL the widget's label
    """

    def __init__(self):
        """constructor"""
        self.__extwidget = None


    def create(self, _id, _value, _parent, _widget_name):
        """create this IO widget.
        \param[in] _id     widget id
        \param[in] _value  widget default value
        \param[in] _parent parent Qt widget
        \param[in] _widget_name widget name
        """
        self.__extwidget = QtExtWidget.QtExtToggleButton(_id, _parent)
        self.__keyid = _id

        return self.__extwidget

    # apply option
    def apply_option(self, _dict_opt):
        """apply options to customize after the creation.

        \param[in] _dict_opt options
        """
        if 'LABEL' in _dict_opt:
            self.__extwidget.set_label(_dict_opt['LABEL'])


    def get_key(self):
        """get this widget's key (id).
        \return the key ID of this widget.
        """
        return self.__keyid

    # set value
    def set_value(self, _value):
        """set value to this widget.
        \param[in] _value value (boolean) of this widget IO.
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



#----------------------------------------------------------------------

# NIN class QtPushButton(QtWidgetIOIF)
# NIN class QtRadioButton(QtWidgetIOIF)

#----------------------------------------------------------------------

# class QtCheckBox(QtWidgetIOIF):
#     """Check box with QtWidgetIOIF interface.
#     \ingroup qtwidget
#     """

#----------------------------------------------------------------------

class QtComboBoxWIO(QtWidgetIOIF):
    """Combobox with QtWidgetIOIF interface.
    \ingroup qtwidget

    Supported options:
    - LABEL the widget's label
    - ITEMS a list of string
    - RW    a bool indicating if new items may be entered by the user
    - SIZELIMIT the number of rows of the ListBox which will pop-up
    when the comboBox is selected.
    """

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
        self.__extwidget = QtExtWidget.QtExtComboBox(_id, _parent,
                                                     QtCore.Qt.Horizontal)
        self.__keyid = _id
        return self.__extwidget


    # apply option
    def apply_option(self, _dict_opt):
        """apply options to customize after the creation.

        \param[in] _dict_opt options
        """
        if 'LABEL' in _dict_opt:
            self.__extwidget.set_label(_dict_opt['LABEL'])

        if 'ITEMS' in _dict_opt:
            self.__extwidget.set_items(_dict_opt['ITEMS'])

        if 'RW' in _dict_opt:
            self.__extwidget.set_rw(_dict_opt['RW'])

        if 'SIZELIMIT' in _dict_opt:
            self.__extwidget.set_sizelimit(_dict_opt['SIZELIMIT'])


    def get_key(self):
        """get this widget's key (id).
        \return the key ID of this widget.
        """
        return self.__keyid

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



# NIN class QtListBox(QtWidgetIOIF)
# NIN class QtLabel(QtWidgetIOIF)
# NIN class QtTextField(QtWidgetIOIF)
# NIN class QtSeparator(QtWidgetIOIF)
# NIN class QtWheelControl(QtWidgetIOIF)

