#!/usr/bin/env python

"""test IFGI Camera"""

import unittest
import Camera

class TestCamera(unittest.TestCase):
    """test: camera"""

    def test_camera0(self):
        """test camera"""
        glcam = Camera.GLCamera()
        # glcam.print_obj()
        mat = glcam.get_coordinate_system()
        # print mat


#
# main test
#
suit0   = unittest.TestLoader().loadTestsFromTestCase(TestCamera)
alltest = unittest.TestSuite([suit0])
unittest.TextTestRunner(verbosity=2).run(alltest)
