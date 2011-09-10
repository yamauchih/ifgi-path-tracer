#!/usr/bin/env python
#
# Copyright (C) 2010-2011 Yamauchi, Hitoshi
#
#
"""test all in ifgi/example"""

import unittest

import test_ifgi_init_shutdown
import test_ifgi_render_0
import test_ifgi_render_1

#
# main test
#
if __name__ == '__main__':
    suits = []
    suits.append(unittest.TestLoader().loadTestsFromTestCase(test_ifgi_init_shutdown.TestIfgiInitShutdown))
    suits.append(unittest.TestLoader().loadTestsFromTestCase(test_ifgi_render_0.TestIfgiRender0))
    suits.append(unittest.TestLoader().loadTestsFromTestCase(test_ifgi_render_1.TestIfgiRender1))

    alltest = unittest.TestSuite(suits)
    unittest.TextTestRunner(verbosity=2).run(alltest)
