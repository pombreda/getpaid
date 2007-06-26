"""Integration tests for donations.
"""

import unittest
from Testing.ZopeTestCase import ZopeDocTestSuite

from base import PloneGetPaidTestCase
from utils import optionflags


def test_creation():
    """Test that donations can be created and initiated.
    
    >>> self.setRoles(('Manager',))
    >>> id = self.portal.invokeFactory('Document', 'page-to-donate')
    >>> donation = self.portal.restrictedTraverse('page-to-donate')
    
    Let's make it Donation-able
    
    >>> from Products.Five.utilities.marker import mark
    >>> from Products.PloneGetPaid.interfaces import IDonatableMarker
    >>> mark( donation, IDonatableMarker)
    """

def test_suite():
    return unittest.TestSuite((
            ZopeDocTestSuite(test_class=PloneGetPaidTestCase,
                             optionflags=optionflags),
        ))
