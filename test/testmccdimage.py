#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
# Unit tests

# builds on stuff from ImageD11.test.testpeaksearch
"""

import unittest
import os
import logging
import sys

for idx, opts in enumerate(sys.argv[:]):
    if opts in ["-d", "--debug"]:
        logging.basicConfig(level=logging.DEBUG)
        sys.argv.pop(idx)
try:
    logging.debug("tests loaded from file: %s" % __file__)
except:
    __file__ = os.getcwd()

from utilstest import UtilsTest

from fabio.marccdimage import marccdimage
from fabio.tifimage import tifimage
import numpy as np

# statistics come from fit2d I think
# filename dim1 dim2 min max mean stddev
TESTIMAGES = """corkcont2_H_0089.mccd  2048 2048  0  354  7.2611 14.639
corkcont2_H_0089.mccd.bz2 2048 2048  0  354  7.2611 14.639
corkcont2_H_0089.mccd.gz 2048 2048  0  354  7.2611 14.639
somedata_0001.mccd 1024 1024  0  20721  128.37 136.23
somedata_0001.mccd.bz2 1024 1024  0  20721  128.37 136.23
somedata_0001.mccd.gz 1024 1024  0  20721  128.37 136.23"""

class testnormaltifok(unittest.TestCase):
    """
    check we can read normal tifs as well as mccd
    """
    imdata = None
    image = 'testimages/tifimagewrite_test0000.tif'
    def setUp(self):
        """
        create an image 
        """
        self.imdata = np.zeros((24, 24), np.uint16)
        self.imdata[ 12:14, 15:17 ] = 42
        obj = tifimage(self.imdata, { })
        obj.write(self.image)
    def tearDown(self):
        "leave the test image in place for debugging, it is small"
        return
    def test_read_openimage(self):
        from fabio.openimage import openimage
        obj = openimage(self.image)
        if obj.data.astype(int).tostring() != self.imdata.astype(int).tostring():
            print type(self.imdata), self.imdata.dtype
            print type(obj.data), obj.data.dtype
            print obj.data - self.imdata
        self.assertEqual(obj.data.astype(int).tostring(),
                          self.imdata.astype(int).tostring())




class testflatmccds(unittest.TestCase):
    def setUp(self):
        UtilsTest.getimage("corkcont2_H_0089.mccd.bz2")
        UtilsTest.getimage("somedata_0001.mccd.bz2")

    def test_read(self):
        """ check we can read MarCCD images"""
        for line in TESTIMAGES.split("\n"):
            vals = line.split()
            name = vals[0]
            dim1, dim2 = [int(x) for x in vals[1:3]]
            mini, maxi, mean, stddev = [float(x) for x in vals[3:]]
            obj = marccdimage()
            obj.read(os.path.join("testimages", name))
            self.assertAlmostEqual(mini, obj.getmin(), 2, "getmin")
            self.assertAlmostEqual(maxi, obj.getmax(), 2, "getmax")
            self.assertAlmostEqual(mean, obj.getmean(), 2, "getmean")
            self.assertAlmostEqual(stddev, obj.getstddev(), 2, "getstddev")
            self.assertEqual(dim1, obj.dim1, "dim1")
            self.assertEqual(dim2, obj.dim2, "dim2")





def test_suite_all_mccd():
    testSuite = unittest.TestSuite()
    testSuite.addTest(testnormaltifok("test_read_openimage"))
    testSuite.addTest(testflatmccds("test_read"))
    return testSuite

if __name__ == '__main__':
    mysuite = test_suite_all_mccd()
    runner = unittest.TextTestRunner()
    runner.run(mysuite)


