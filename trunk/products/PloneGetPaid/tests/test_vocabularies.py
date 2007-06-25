"""Integration tests for donations.
"""

import unittest
from Testing.ZopeTestCase import ZopeDocTestSuite

from base import PloneGetPaidTestCase
from utils import optionflags

def test_suite():
    return unittest.TestSuite((
            ZopeDocTestSuite(test_class=PloneGetPaidTestCase,
                             optionflags=optionflags),
        ))
