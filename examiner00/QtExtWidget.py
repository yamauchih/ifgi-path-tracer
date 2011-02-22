#!/usr/bin/env python

"""QtExtWidget
\file
\brief Qt extented widget set for QtWidgetIO
\module QtWidgetIO
"""

from PyQt4 import Qt, QtCore, QtGui

# QtExtTextLine
class QtExtTextLine(QtGui.QWidget):
    """QtExtTextLine

    Qt extended text line widget for QtWidgetIO
    """

    # constructor
    def __init__(self, _label, _parent, _orientation):
        """constructor

        \param[in] _parent parent Qt widget"""

        super(QtExtTextLine, self).__init__(_parent)

        self.__label = QtGui.QLabel(self)
        self.__label.setObjectName(_label + '.valueLabel')
        self.__text  = QtGui.QLineEdit(self)
        self.__text.setObjectName(_label + '.valueEdit')

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
    def setLabel(self, _label):
        self.__label.setText(_label)
        self.__label.setMinimumSize(self.__label.sizeHint())

    # Sets the validator of the lineEdit widget
    # def setValidator(QValidator* _val):
    #     d_text->setValidator(_val);

    # Returns the validator.
    # const QValidator* validator() const  { return d_text->validator(); }

    # Sets the maximum length of accepted strings.
    # void setMaxLength(int _len) { d_text->setMaxLength(_len); }

    # Returns the currently entered Text
    def get_value(self):
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

    # def textChanged(self, _text):
    #     print 'textChanged signal'

    # def returnPressed(self, _text):
    #     print 'returnPressed signal'

