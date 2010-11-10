#!/usr/bin/env python
#
# const test
#

import const

# This works well
# const.a = 'hello'
# const.a = 'world'

# This works well
class ConstTest(object):
    def __init__(self):
        const.a = 'hello'
        self.a = const.a
        self.a = 'world'
        print self.a

ConstTest()

