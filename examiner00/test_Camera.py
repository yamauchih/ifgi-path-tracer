#!/usr/bin/env python
#
# test for Camera
#

"""test IFGI Camera"""

import unittest
import Camera

class TestCamera(unittest.TestCase):

    def test_camera0(self):
        glcam = Camera.GLCamera()
        glcam.print_obj()
        mat = glcam.getCoordinateSystem()
        print mat


#
# main test
#
suit0   = unittest.TestLoader().loadTestsFromTestCase(TestCamera)
alltest = unittest.TestSuite([suit0])
unittest.TextTestRunner(verbosity=2).run(alltest)
