"""Test of make payable functionality

These tests verify that content classes can be marked as payable
and that they receive the payable functlionality when they are 
marked as such
"""

import unittest
from Testing.ZopeTestCase import ZopeDocTestSuite

from base import PloneGetPaidTestCase
from utils import optionflags

class TestMakePayable(PloneGetPaidTestCase):
    
    def test_mark_object_payable(self):
        pass
    
def test_suite():
    return unittest.TestSuite((
            ZopeDocTestSuite(test_class=PloneGetPaidTestCase,
                             optionflags=optionflags),
        ))
