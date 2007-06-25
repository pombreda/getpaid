"""Integration tests for donations.
"""

import unittest
from Testing.ZopeTestCase import ZopeDocTestSuite

from base import PloneGetPaidTestCase
from utils import optionflags

def test_creation():
    """Test that donations can be created and initiated.
    
    >>> self.setRoles(('Manager',))
    >>> id = self.portal.invokeFactory('Donation', 'donation')
    >>> donation = self.portal.donation
    
    Set roles.
    
    >>> donation.setRoles(('Reviewer',))
    >>> tuple(donation.getRoles())
    ('Reviewer',)
        
    """

def test_suite():
    return unittest.TestSuite((
            ZopeDocTestSuite(test_class=PloneGetPaidTestCase,
                             optionflags=optionflags),
        ))
