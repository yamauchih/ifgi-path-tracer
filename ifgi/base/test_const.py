#!/usr/bin/env python
#
# Copyright (C) 2010-2011 Yamauchi, Hitoshi
#
"""const test.
\file
\brief test for python const.
"""
import const

# This works well
# const.a = 'hello'
# const.a = 'world'

# This works well
class ConstTest(object):
    """const test"""
    def __init__(self):
        """constructor."""
        const.a = 'hello'
        self.a = const.a
        self.a = 'world'
        # print self.a

ConstTest()

