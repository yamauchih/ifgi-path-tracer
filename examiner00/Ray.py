#!/usr/bin/env python
#
# Ray
#

"""IFGI Ray"""

import math
import numpy

#
# Ray class
#
class Ray(object):
    # default constructor
    #
    # \param[in] _origin ray origin
    # \param[in] _dir    ray direction
    def __init__(self, _origin, _dir):
        self.origin = _origin
        self.dir    = _dir

    # class name
    def get_classname(self):
        return "Ray"



#
# main test
#
if __name__ == '__main__':
    pass
