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
    """a ray"""

    # default constructor
    def __init__(self, _origin, _dir):
        """default constructor.
        \param[in] _origin ray origin
        \param[in] _dir    ray direction
        """
        self.origin = _origin
        self.dir    = _dir

    # class name
    def get_classname(self):
        """get class name
        \return class name"""
        return 'Ray'

#
# main test
#
if __name__ == '__main__':
    pass
