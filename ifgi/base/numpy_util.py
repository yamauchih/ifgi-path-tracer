#!/usr/bin/env python
#
# Copyright (C) 2010-2011 Yamauchi, Hitoshi
#
# numpy related utility
"""
\file
\brief numpy related utility"""

import math, numpy

def array2str(_array):
    """numpy array -> string conversion
    \param[in] _array numpy array value
    \return string representation of numpy array
    """
    ret_str = ''
    for x in xrange(_array.size):
        ret_str += (str(_array[x]) + ' ')

    return ret_str


def str2array(_array_str):
    """string -> numpy array conversion
    \param[in] _array_str string representation of numpy array by array2str
    \return numpy array value
    """
    return numpy.fromstring(_array_str, sep=' ')


