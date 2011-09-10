#!/usr/bin/env python
#
# Copyright (C) 2010-2011 Yamauchi, Hitoshi
#
#
"""test all in ifgi base"""

import unittest

import test_ILog
import test_Listener
import test_OrthonomalBasis
import test_Sampler
import test_const
import test_enum
import test_ifgimath
import test_numpy_util


#
# main test
#
if __name__ == '__main__':
    suits = []
    suits.append(unittest.TestLoader().loadTestsFromTestCase(test_ILog.TestIFGILogger))
    suits.append(unittest.TestLoader().loadTestsFromTestCase(test_Listener.TestListener))
    suits.append(unittest.TestLoader().loadTestsFromTestCase(test_OrthonomalBasis.TestIFGIONB))
    suits.append(unittest.TestLoader().loadTestsFromTestCase(test_Sampler.TestStratifiedRegularSampler))
    suits.append(unittest.TestLoader().loadTestsFromTestCase(test_const.TestConst))
    suits.append(unittest.TestLoader().loadTestsFromTestCase(test_enum.TestEnum))
    suits.append(unittest.TestLoader().loadTestsFromTestCase(test_ifgimath.TestIFGImathModule))
    suits.append(unittest.TestLoader().loadTestsFromTestCase(test_numpy_util.TestNumpyUtil))

    alltest = unittest.TestSuite(suits)
    unittest.TextTestRunner(verbosity=2).run(alltest)
