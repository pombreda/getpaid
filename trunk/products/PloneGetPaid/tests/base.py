"""Base class for integration tests, based on ZopeTestCase and PloneTestCase.

Note that importing this module has various side-effects: it registers a set of
products with Zope, and it sets up a sandbox Plone site with the appropriate
products installed.
"""

from Testing import ZopeTestCase

# Let Zope know about the two products we require above-and-beyond a basic
# Plone install (PloneTestCase takes care of these).
ZopeTestCase.installProduct('ore.member')
ZopeTestCase.installProduct('CMFOnFive')
ZopeTestCase.installProduct('PloneGetPaid')


# Import PloneTestCase - this registers more products with Zope as a side effect
from Products.PloneTestCase.PloneTestCase import PloneTestCase
from Products.PloneTestCase.PloneTestCase import FunctionalTestCase
from Products.PloneTestCase.PloneTestCase import setupPloneSite

# Set up a Plone site, and apply the membrane and borg extension profiles
# to make sure they are installed.


#setupPloneSite(extension_profiles=('membrane:default', 'PloneGetPaid:default'))

class PloneGetPaidTestCase(PloneTestCase):
    """Base class for integration tests for the 'PloneGetPaid' product. This may
    provide specific set-up and tear-down operations, or provide convenience
    methods.
    """
    
class PloneGetPaidFunctionalTestCase(FunctionalTestCase):
    """Base class for functional integration tests for the 'PloneGetPaid' product. 
    This may provide specific set-up and tear-down operations, or provide 
    convenience methods.
    """