#!/usr/bin/env python
#
# Copyright 2011 (C) Yamauchi, Hitoshi
#
# HitRecord
#

"""IFGI HitRecord
\file
\brief a hit record
"""

import sys

# HitRecord
class HitRecord(object):
    """hit record. members are public.
    """

    # default constructor
    def __init__(self):
        """default constructor.
        """
        self.dist = sys.float_info.max
        self.intersect_pos = None
        self.hit_primitive = None

    # class name
    def get_classname(self):
        """get class name
        \return class name
        """
        return 'HitRecord'


    # string representation
    def __str__(self):
        return 'HitRecord: dist: '+ str(self.dist) +\
            ', pos: ' + str(self.intersect_pos)



#
# main test
#
# if __name__ == '__main__':
#     pass
