"""Unit test for adding a payable type to a shopping cart.
"""

import unittest
from Testing.ZopeTestCase import ZopeDocTestSuite
from utils import optionflags

from base import PloneGetPaidTestCase

def test_add_to_cart():
    """Test that payments can be processed.
    
    """



def test_suite():
    return unittest.TestSuite((
            ZopeDocTestSuite(test_class=PloneGetPaidTestCase,
                             optionflags=optionflags),
        ))
