#!/usr/bin/env python
#
# Copyright (C) 2010-2011 Yamauchi, Hitoshi
#

"""QtExtWidget
\file
\brief Qt extented widget set for QtWidgetIO
\see QtWidgetIO

- QtExtTextLine: Qt extension TextLine
- QtExtCombobox: Qt extension Combobox
"""

from PyQt4 import Qt, QtCore, QtGui

#----------------------------------------------------------------------

class QtExtTextLine(QtGui.QWidget):
    """QtExtTextLine
    \ingroup qtextwidget_container
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
        if (self.__orientation == Qt.Qt.Horizontal):
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
        return res

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


    def textChanged(self, _text):
        # print 'textChanged signal'
        pass

    def returnPressed(self, _text):
        # print 'returnPressed signal'
        pass


# ----------------------------------------------------------------------

class QtExtColorButton(QtGui.QFrame):
    """QtExtColorButton
    \ingroup qtextwidget_container
    Qt extended color button widget for QtWidgetIO
    """

    # signal value changed
    signal_value_change = QtCore.pyqtSignal(object)


    def __init__(self, _color, _parent, _name):
        """constructor

        \param[in] _color  initial color
        \param[in] _parent parent widget
        \param[in] _name   widget name
        """
        super(QtExtColorButton, self).__init__(_parent)
        self.setObjectName(_name)

        self.__color  = _color   # QColor

        self.__hbox = QtGui.QHBoxLayout(self)
        self.__hbox.setSizeConstraint(QtGui.QLayout.SetMinimumSize);
        # hbox->setSizeConstraint(QLayout::SetFixedSize);

        self.__label = QtGui.QLabel(self)
        self.__label.setObjectName(_name + '.valueLabel')
        # for expand minimumSize(), all direction 1 pixel
        self.__label.setMargin(1)
	# give minimumSize to this
        self.__label.setMinimumSize(self.__label.sizeHint())

        self.__button = QtGui.QPushButton(self) # "Browse ...",this
        self.__button.setObjectName(_name + '.browse')
        # same as label
        self.__button.setContentsMargins(1, 1, 1, 1)
        self.__button.setMinimumSize(self.__button.sizeHint())

        hspacing = 10
        self.__hbox.addWidget(self.__label)
        # self.__button.setMinimumSize(Qt.QSize(100, FEAT_HIGHT))
        # self.__button.setMaximumSize(Qt.QSize(100, FEAT_HIGHT))
        self.__hbox.addWidget(self.__button)
        self.__hbox.addSpacing(hspacing)
        self.__hbox.addStretch(10)

        self.set_color(_color)
        self.__button.clicked.connect(self.__choose_color)

        self.setToolTip('push to select a color');


    def set_label(self, _label):
        """Sets the widget's label.

        \param[in] _label widget's label.
        """
        self.__label.setText(_label)


    def set_color(self, _col):
        """Sets the current color.

        \param[in] _col color
        """
        self.__color = _col

        qicon = self.__button.icon()

        # get correct pixmap size. Assume less than 128x128.
        extent = 128

        if(not qicon.pixmap(extent).isNull()):
            pm = QtGui.QPixmap(qicon.pixmap(extent))
            pm.fill(_col)
            qicon.addPixmap(pm)
            self.__button.setIcon(qicon)
        else:
            pm = QtGui.QPixmap(self.__button.width() - 4, self.__button.height() - 4);
            pm.fill(_col)
            qicon.addPixmap(pm)
            self.__button.setIcon(pm)
            self.__button.setIconSize(QGui.QSize(
                self.__button.width() - 4 , self.__button.height() - 4))


    def get_color(self):
        """get current color.

        \return current color
        """
        return self.__color


    def slotSetValue(self, _color):
        """a slot. same as set_color().
        """
        self.set_color(_color)


    def __choose_color():
        """choose a RGBA color by the color dialog
        """
        rgba = QColorDialog.getColor(self.__color, self, \
                                         'QtExtColorButton choose color',\
                                         QtGui.QColorDialog.ShowAlphaChannel)
        if(rgba.isValid()):
            self.set_color(rgba)
            self.signal_value_changed.emit(rgba)


# ----------------------------------------------------------------------

class QtExtToggleButton(QtGui.QWidget):
    """QtExtToggleButton
    \ingroup qtextwidget_container
    Qt extended toggle button (one check box) widget for QtWidgetIO

    The widget structure is: [x] LABEL
    """

    # constructor
    def __init__(self, _label, _parent):
        """constructor

        \param[in] _label  text label
        \param[in] _parent parent Qt widget
        """

        super(QtExtToggleButton, self).__init__(_parent)

        self.__checkbox = QtGui.QCheckBox(_parent);
        self.__checkbox.setObjectName(_label);
        self.__checkbox.setChecked(False);

        # connect signal
        self.__checkbox.stateChanged.connect(self.slotUpdate)

        # QtCore.Qt.Horizontal orientation only
        self.__layout = QtGui.QHBoxLayout(self)
        self.__layout.addWidget(self.__checkbox)
        self.__layout.activate();
        self.setLayout(self.__layout);


    def set_label(self, _label):
        """set the widget's label
        \param[in] _label label text"""
        self.__checkbox.setText(_label)
        self.__checkbox.setMinimumSize(self.__checkbox.sizeHint())

    def get_value(self):
        """returns the currently entered Text
        \return value of this widget IO, text.
        """
        res = self.__checkbox.checkState();
        if(res == QtCore.Qt.Checked):
            return True

        # Qt.Unchecked or Qt.PartiallyChecked
        return False

    # set value
    def set_value(self, _is_checked):
        """set boolean value of this ext wiegdt.
        \param[in] _is_checked true when checked"""
        if(_is_checked == True):
            self.__checkbox.setChecked(QtCore.Qt.Checked)
        else:
            self.__checkbox.setChecked(QtCore.Qt.Unchecked)

    def slotUpdate(self, _check_state):
        """slot for when state changed
        """
        print 'Toggele button: state = ', str(_check_state)

#----------------------------------------------------------------------

class QtExtComboBox(QtGui.QFrame):
    """QtExtComboBox
    \ingroup qtextwidget_container
    Qt extended combobox widget for QtWidgetIO
    """

    def __init__(self, _label, _parent, _orientation):
        """constructor

        \param[in] _label  text label
        \param[in] _parent parent Qt widget
        \param[in] _orientation widget orientation (Horizontal, Vertical)
        """

        super(QtExtComboBox, self).__init__(_parent)

        self.__label = QtGui.QLabel(self)
        self.__label.setObjectName(_label + '.valueLabel')
        # self.__text  = QtGui.QLineEdit(self)
        # self.__text.setObjectName(_label  + '.valueEdit')

        self.__combo = QtGui.QComboBox(self)
        self.__combo.setObjectName(_label + '.valueEdit');
        self.__combo.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)

        # send out two different signals
        #
        # C++: m_combo's activated(int) emit the signal this's activated(int)
        #   connect(m_combo, SIGNAL(activated(int)), this, SIGNAL(activated(int)));
        # the difference is only the object: m_combo.activated -> this.activated
        self.__combo.activated.connect(self.activated)
        self.__combo.activated.connect(self.slotActivatedWithIndex)
        self.__combo.textChanged.connect(self.slotActivatedWithIndex)


        self.__max_line = 5
        self.__item_list = []

        # set one column list box
        self.__combo.view().sizeHintForColumn(1);
        self.__combo.setMinimumSize(QtCore.QSize(self.__combo.sizeHint().width()+20,
                                                 self.__combo.sizeHint().height()))

        self.__orientation = _orientation;
        if self.__orientation == Qt.Qt.Horizontal:
            self.__layout = QtGui.QHBoxLayout(self)
        else:
            self.__layout = GuGui.QVBoxLayout(self)

        self.__label.setMinimumSize(QtCore.QSize(0,0));
        self.__label.setMaximumWidth(50);

        self.__combo.setSizePolicy(QtGui.QSizePolicy(
                QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred))

        self.__layout.addWidget(self.__label, 0);
        hspacing = 10
        self.__layout.addSpacing(hspacing);
        self.__layout.addWidget(self.__combo, 1);

        # empty label needed to align the combo box to the left
        # emptyLabel = QtGui.QLabel(self)
        # self.__layout.addWidget(emptyLabel, 100);


    def set_label(self, _label):
        """set label.
        \param[in] _label label
        """
        self.__label.setText(_label)
        self.__label.setMinimumSize(self.__label.sizeHint())
        self.__label.setMaximumSize(self.__label.sizeHint())


    def set_items(self, _item_list):
        """set items.
        \param[in] _item_list item string list
        """

        self.__item_list = _item_list
        self.__combo.clear()

        for txt in _item_list:
            self.__combo.addItem(txt)

        self.__combo.setMinimumSize(self.__combo.sizeHint())
        self.__combo.view().sizeHintForColumn(1)



    def get_value_index(self):
        """get current value index.
        \return combo box value index
        """
        return self.__combo.currentIndex()


    def get_value(self):
        """get current value.
        \return current value (text)
        """
        ret_text = self.__combo.currentText()
        return ret_text


    # def set_value_by_index(self, _index):
    #     """set current commbobox index.
    #     \param[in] _index index of the combobox to be set.
    #     """
    #     self.__combo.setCurrentIndex(_index)


    def set_value(self, _str):
        """set current combobox index by a string.
        \param[in] _index index of the combobox to be set.
        """
        if _str in self.__item_list:
            self.__combo.setCurrentIndex(self.__item_list.index(_str))
        else:
            self.__combo.setEditText(_str)


    def set_sizelimit(self, _max_line):
        """set combobox max size.
        \param[in] _max_line max lines
        """
        if _max_line < 1:
            QtCore.qWarning('QtExtComboBox::setSizeLimit: _max_line (' + \
                                str(_max_line) +' is < 1. set to 1.')
            _max_line = 1

        self.__max_line = _max_line
        self.__combo.setMaxVisibleItems(_max_line);



    def set_rw(self, _is_readwrite):
        """set readwrite mode.
        \param[in] _is_readwrite readwrite mode. when true readwrite,
        otherwise, readonly.
        """
        self.__combo.setEditable(_is_readwrite)
        # if _is_readwrite:
        #     d_emptyLabel->hide();
        # else:
        #     d_emptyLabel->show();


    def set_insertion_policy(self, _insertion_policy):
        """set insertion policy.
        \param[in] _insertion_policy combobox insertion policy
        """
        self.__combo.setInsertPolicy(_insertion_policy)


    #----------------------------------------------------------------------

    def activated(self, _arg):
        print 'signal::activated.'



    #----------------------------------------------------------------------

    def slotActivatedWithIndex(self, _text):
        """slotActivated with text argument.
        """
        print 'slotActivatedWithIndex: ' + str(_text)
        # self.activated.emit(_text)

# ----------------------------------------------------------------------
