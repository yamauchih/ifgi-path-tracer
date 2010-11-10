#!/usr/bin/env python
#
# test for Examiner widget related functions
#

"""test IFGI ExaminerWidget"""

import unittest
import numpy
import ExaminerWidget

class TestExaminerWidget(unittest.TestCase):

    # test mapToSphere function
    def test_mapToSphere(self):

        win_pos_list = [numpy.array([  0,   0]),
                        numpy.array([100,   0]),
                        numpy.array([ 80,  90]), # center
                        numpy.array([150, 150]),
                        numpy.array([159, 179]) # corner
                        # out of range numpy.array([200, 200])
                        ]
        win_width  = 160
        win_height = 180
        pos3d_on_sphere = numpy.array([0, 0, 0])

        for wpos in win_pos_list:
            ret = ExaminerWidget.mapToSphere(wpos, win_width, win_height)
            print 'map to sphere ' + str(wpos) + ' -> ' + str(ret)

#
# main test
#
suit0   = unittest.TestLoader().loadTestsFromTestCase(TestExaminerWidget)
alltest = unittest.TestSuite([suit0])
unittest.TextTestRunner(verbosity=2).run(alltest)
