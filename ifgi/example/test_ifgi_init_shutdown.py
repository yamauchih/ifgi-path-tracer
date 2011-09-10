#!/usr/bin/env python
#
# Copyright (C) 2010-2011 Yamauchi, Hitoshi
#
# Example: initialize and shutdown
#
# For set up the environment to run, see test_all.sh
#
"""
\file
\brief initialize and shutdown ifgi renderer
"""

import unittest
from ifgi.ptracer.IfgiSys import IfgiSys


class TestIfgiInitShutdown(unittest.TestCase):
    """test: ifgi sysyem start and shutdown"""

    def test_start_shutdown(self):
        """start and shutdown ifgi system"""

        ifgi_inst = IfgiSys()

        assert(ifgi_inst.state() == "stop")
        assert(ifgi_inst.start() == True)

        assert(ifgi_inst.state() == "up")
        assert(ifgi_inst.stop()  == True)

        assert(ifgi_inst.state() == "stop")
        assert(ifgi_inst.start() == True)

        assert(ifgi_inst.state() == "up")
        assert(ifgi_inst.shutdown() == True)

        assert(ifgi_inst.state() == "down")


#
# main test
#
if __name__ == '__main__':
    suit0   = unittest.TestLoader().loadTestsFromTestCase(TestIfgiInitShutdown)
    alltest = unittest.TestSuite([suit0])
    unittest.TextTestRunner(verbosity=2).run(alltest)



