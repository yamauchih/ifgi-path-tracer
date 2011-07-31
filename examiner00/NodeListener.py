#!/usr/bin/env python
#
# Copyright (C) 2010-2011 Yamauchi, Hitoshi
#

"""NodeListener
\file
\brief Node status observer pattern (Listener/Subject)"""

from ifgi.base  import Listener
import QtExaminerWidget

class NodeListener(Listener.Listener):
    """Node listener
    """
    def __init__(self, _name, _subject, _examiner_widget):
        """constructor.
        \param[in] _name listener's name
        \param[in] _subject observing/listening subject
        """
        super(MyListener, self).__init__(_name, _subject)
        self.__examiner_widget =  _examiner_widget


    def update(self, _event):
        """get update from the subject
        This should be overridden.
        \param[in] _event what kind of event happened."""
        print self.get_name(), "received event", _event
        _examiner_widget.updateGL()

