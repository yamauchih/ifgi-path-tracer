#!/usr/bin/env python
#
# Copyright (C) 2010-2011 Yamauchi, Hitoshi
#
"""ifgi logger
\file
\brief a simple logging system"""

# Logger
class ILog(object):
    """simple logger class.
    """

    # __outoutlvel
    # 0. (none)
    # 1. error
    # 2. warning
    # 3. info
    # 4. debug
    __outputlevel = 4

    # default constructor
    def __init__(self):
        """default constructor"""
        pass

    # set output level
    # @staticmethod makes this method C++/Java static like method
    @staticmethod
    def set_output_level(_lv):
        """set output level. staticmethod
        Output level:
        - 1. error
        - 2. warning
        - 3. info
        - 4. debug
        \param[in] _lv output level
        """
        if (_lv < 0) or (_lv > 4):
            raise StandardError('output level should be [0,4].')

        ILog.__outputlevel = _lv


    # get output level
    @staticmethod
    def get_output_level():
        """get output level. staticmethod
        \return current output level
        """
        return ILog.__outputlevel

    # error
    @staticmethod
    def error(_mes):
        """output error message
        \param[in] _mes message
        """
        if(ILog.__outputlevel >= 1):
            print('error: ' + _mes)

    # warning
    @staticmethod
    def warn(_mes):
        """output warning message
        \param[in] _mes message
        """
        if(ILog.__outputlevel >= 2):
            print('warn:  ' + _mes)

    # info
    @staticmethod
    def info(_mes):
        """output info message
        \param[in] _mes info message
        """
        if(ILog.__outputlevel >= 3):
            print('info:  ' + _mes)

    # debug
    @staticmethod
    def debug(_mes):
        """output debug message
        \param[in] _mes message
        """
        if(ILog.__outputlevel >= 4):
            print('debug: ' + _mes)


#
# main test ... test_ObjReader
#
# if __name__ == '__main__':
#     objreader = ObjReader()
#     objreader.read('../sampledata/one_tri.obj')
#
