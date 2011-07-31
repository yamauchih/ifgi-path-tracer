#!/usr/bin/env python
#
# Copyright (C) 2010-2011 Yamauchi, Hitoshi
#
# Observer or Listener patteren. Ref. Wikipedia

"""ifgi observer/listener, subject patteren
\file
\brief observer/listener, subject patteren"""


class Listener(object):
    """Observer pattern's Observer/Listener"""

    def __init__(self, _name, _subject):
        """constructor.
        \param[in] _name listener's name
        \param[in] _subject observing/listening subject
        """
        self.__name = _name
        _subject.register(self)

    def get_name(self):
        """get the listener's name
        \return listener's name."""
        return self.__name

    def update(self, _event):
        """get update from the subject
        This should be overridden.
        \param[in] _event what kind of event happened."""
        raise StandardError('Should be reimplemented.')


class Subject(object):
    """Observer patteren's subject.
    """
    def __init__(self):
        """constructor"""
        self.__listeners = []

    def register(self, _listener):
        """register the listener.
        \param[in] _listener a lister/observer to be added."""
        self.__listeners.append(_listener)

    def unregister(self, _listener):
        """unregister the listener.
        \param[in] _listener a lister/observer to be removed."""
        self.__listeners.remove(_listener)

    def notify_listeners(self, _event):
        """Notify myself's change to all the listeners.
        \param[in] _event an event
        """
        for listener in self.__listeners:
            listener.update(_event)

