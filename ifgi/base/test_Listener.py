#!/usr/bin/env python
#
# Copyright (C) 2010-2011 Yamauchi, Hitoshi
#
#
"""test Listener"""

import numpy
import unittest
# From file ILog (first one), import ILog (second one) class
import Listener

class MyListener(Listener.Listener):

    def __init__(self, _name, _subject):
        """constructor.
        \param[in] _name listener's name
        \param[in] _subject observing/listening subject
        """
        super(MyListener, self).__init__(_name, _subject)

    def update(self, _event):
        """get update from the subject
        This should be overridden.
        \param[in] _event what kind of event happened."""
        print self.get_name(), "received event", _event


class TestListener(unittest.TestCase):
    """test: observer patteren"""

    def test_listener(self):
        """test listener."""

        subject = Listener.Subject('IamaSubject')

        listener_0 = MyListener('<listener A>', subject)
        listener_1 = MyListener('<listener B>', subject)
        # subject has two listeners/observers
        subject.notify_listeners('<event 1>')
        # output:
        #     <listener A> received event <event 1>
        #     <listener B> received event <event 1>

#
# main test
#
suit0   = unittest.TestLoader().loadTestsFromTestCase(TestListener)
alltest = unittest.TestSuite([suit0])
unittest.TextTestRunner(verbosity=2).run(alltest)
