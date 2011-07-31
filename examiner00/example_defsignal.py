from PyQt4.QtCore import *
from PyQt4.QtGui  import *

class MyWidget(QWidget):

    # user defined signal
    pyqt_signal = pyqtSignal(object)

    def __init__(self, parent=None):
        super(MyWidget, self).__init__(parent)

        self.ok_button = QPushButton("ok", self)

        layout = QHBoxLayout()
        layout.addWidget(self.ok_button)
        self.setLayout(layout)

        self.ok_button.clicked.connect(self.slot1)
        self.pyqt_signal.connect(self.slot2)

    def slot1(self):
        print 'slot1'
        self.pyqt_signal.emit([1, 2, 3])

    def slot2(self, arg):
        print "slot2 arg = %s" % arg

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    win = MyWidget()
    win.show()
    sys.exit( app.exec_() )
