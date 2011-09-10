#!/usr/bin/env python
#
# Copyright (C) 2010-2011 Yamauchi, Hitoshi
#
#
"""test enum"""

import unittest
# From file ILog (first one), import ILog (second one) class
import enum

class TestEnum(unittest.TestCase):
    """test: Logger"""

    def test_enum(self):
        """test enum and usage."""
        Animals = enum.Enum(['DOG', 'CAT', 'Horse', 'Elephant'])
        # for ani in Animals:
        #     print ani
        s = str(Animals.DOG)
        s = Animals[0]
        i = Animals.index('CAT')
        # s = str(Animals.Bat)    # error
        # print s

#
# main test
#
if __name__ == '__main__':
    suit0   = unittest.TestLoader().loadTestsFromTestCase(TestEnum)
    alltest = unittest.TestSuite([suit0])
    unittest.TextTestRunner(verbosity=2).run(alltest)
