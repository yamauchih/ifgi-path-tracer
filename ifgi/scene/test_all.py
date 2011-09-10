#!/usr/bin/env python
#
# Copyright (C) 2010-2011 Yamauchi, Hitoshi
#
#
"""test all in ifgi base"""

import unittest

import test_Camera
import test_ConvReader2Primitive
import test_Film
import test_IfgiSceneReader
import test_ObjReader
import test_Primitive
import test_SceneGraph


#
# main test
#
if __name__ == '__main__':
    suits = []
    suits.append(unittest.TestLoader().loadTestsFromTestCase(test_Camera.TestCamera))
    suits.append(unittest.TestLoader().loadTestsFromTestCase(test_ConvReader2Primitive.TestConvReader2Primitive))
    suits.append(unittest.TestLoader().loadTestsFromTestCase(test_Film.TestFilm))
    suits.append(unittest.TestLoader().loadTestsFromTestCase(test_IfgiSceneReader.TestIfgiSceneReader))
    suits.append(unittest.TestLoader().loadTestsFromTestCase(test_ObjReader.TestObjReader))
    suits.append(unittest.TestLoader().loadTestsFromTestCase(test_Primitive.TestPrimitive))
    suits.append(unittest.TestLoader().loadTestsFromTestCase(test_SceneGraph.TestSceneGraph))

    alltest = unittest.TestSuite(suits)
    unittest.TextTestRunner(verbosity=2).run(alltest)
