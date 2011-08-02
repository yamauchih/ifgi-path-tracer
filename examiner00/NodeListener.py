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
    def __init__(self, _name, _subject, _qt_node_dialog):
        """constructor.
        \param[in] _name listener's name
        \param[in] _subject observing/listening subject
        \param[in] _qt_node_dialog node dialog (QtSimpleTabDialog)
        """
        super(NodeListener, self).__init__(_name, _subject)
        self.__node_dialog = _qt_node_dialog
        assert(self.__node_dialog != None)


    def update(self, _event):
        """get update from the subject
        This should be overridden.

        event is a list ['event name', other args, ]
        - ConfigChanged: caused by calling set_config_dict()
        - StateChanged:  caused by e.g., draw mode changed
        \param[in] _event what kind of event happened."""
        print 'DEBUG: ', self.get_name(), 'received event', _event
        self.__node_dialog.signal_update.emit(_event)

