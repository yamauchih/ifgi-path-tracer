#!/usr/bin/env python
#
# Copyright (C) 2010-2011 Yamauchi, Hitoshi
#

"""test ifgi utility"""

import unittest
import ifgi_util

class TestIfgiUtil(unittest.TestCase):
    """test: IFGI util module"""

    def test_dict_util(self):
        """test ifgi_util's dictionary related utilities."""

        dict0  = {'foo':1, 'bar':1, 'baz':1, }
        klist0 = ['foo', 'bar', 'baz']

        assert(ifgi_util.has_dict_all_key(dict0, klist0))
        assert(ifgi_util.get_dict_missing_key(dict0, klist0) == [])

        klist1 = ['hoge', 'moge', 'baz']
        assert(not(ifgi_util.has_dict_all_key(dict0, klist1)))
        assert(ifgi_util.get_dict_missing_key(dict0, klist1) == ['hoge', 'moge', ])


#
# main test
#
if __name__ == '__main__':
    suit0   = unittest.TestLoader().loadTestsFromTestCase(TestIfgiUtil)
    alltest = unittest.TestSuite([suit0])
    unittest.TextTestRunner(verbosity=2).run(alltest)
