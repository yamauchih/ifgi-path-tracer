#!/usr/bin/env python
#
# Copyright (C) 2010-2011 Yamauchi, Hitoshi
#
#
"""test ifgi logger"""

import unittest
# From file ILog (first one), import ILog (second one) class
from ILog import ILog

class TestIFGILogger(unittest.TestCase):
    """test: Logger"""

    def test_logger(self):
        """test logger."""

        print('ouput level = ' + str(ILog.get_output_level()))
        self.__test_output_all('default')

        for i in range(1,4) :
            ILog.set_output_level(i)
            print('set ouput level = ' + str(i))
            self.__test_output_all('lv = ' + str(i))


    def __test_output_all(self, _postfix):
        """test subroutine to test all the output level"""
        ILog.error('error message:   ' + _postfix)
        ILog.warn ('warning message: ' + _postfix)
        ILog.info ('info message:    ' + _postfix)
        ILog.debug('debug message:   ' + _postfix)


#
# main test
#
suit0   = unittest.TestLoader().loadTestsFromTestCase(TestIFGILogger)
alltest = unittest.TestSuite([suit0])
unittest.TextTestRunner(verbosity=2).run(alltest)
