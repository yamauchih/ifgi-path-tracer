#!/usr/bin/env python
#
# Copyright (C) 2010-2011 Yamauchi, Hitoshi
#
#
"""test ifgi orthonomal basis"""

import numpy
import unittest
# From file ILog (first one), import ILog (second one) class
from OrthonomalBasis import OrthonomalBasis

class TestIFGIONB(unittest.TestCase):
    """test: OrthonomalBasis"""

    def test_onb(self):
        """test ONB."""

        onb0 = OrthonomalBasis()
        print onb0
        onb0.init_from_u(numpy.array([1, 0, 0]))
        print onb0

#
# main test
#
if __name__ == '__main__':
    suit0   = unittest.TestLoader().loadTestsFromTestCase(TestIFGIONB)
    alltest = unittest.TestSuite([suit0])
    unittest.TextTestRunner(verbosity=2).run(alltest)
