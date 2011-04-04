from Products.Five import zcml
from getpaid.core.tests.base import GetPaidTestCase
import Products.Five
import getpaid.paypal
zcml.load_config('configure.zcml', Products.Five)
zcml.load_config('configure.zcml', getpaid.paypal)
zcml.load_config('overrides.zcml', getpaid.paypal)


from Products.Five import fiveconfigure

from Testing import ZopeTestCase as ztc

from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

# from getpaid.core.tests.base import GetPaidTestCase
# from Products.PloneGetPaid.tests.base import PloneGetPaidFunctionalTestCase
# from Products.PloneGetPaid.interfaces import IGetPaidManagementOptions
# from Products.Five.testbrowser import Browser

# Traditional "Products namespace" products need to be loaded at the module
# level to ensure that they are available early enough.
# see Professional Plone Development (optilude) p. 107
ztc.installProduct('PloneGetPaid')

# def baseAfterSetUp( self ):
#     """Code that is needed is the afterSetUp of both test cases.
#     """
# 
#     # This looks like a safe place to install Five.
#     ztc.installProduct('Five')
# 
#     # Set up sessioning objects
#     ztc.utils.setupCoreSessions(self.app)
    
@onsetup
def setup_getpaid_paypal():
    """Set up the additional products required for the PayPal payment 
       processor.
    
       The @onsetup decorator causes the execution of this body to be deferred
       until the setup of the Plone site testing layer.
    """
    
    # Load the ZCML configuration for the policy package.
    fiveconfigure.debug_mode = True
    import getpaid.paypal
    zcml.load_config('configure.zcml', getpaid.paypal)
    zcml.load_config('overrides.zcml', getpaid.paypal)
    fiveconfigure.debug_mode = False
    
    # We need to tell the testing framework that these products
    # should be available. This can't happen until after we have loaded
    # the ZCML.
    ztc.installPackage('getpaid.paypal')
    
# The order here is important: We first call the (deferred) function which
# installs the products we need for this package. Then, we let 
# PloneTestCase set up this product on installation.

setup_getpaid_paypal()
# Installing the policy product will install this and other products we
# might be theming
ptc.setupPloneSite(products=['PloneGetPaid'])

class GetPaidPaypalPloneTestCase(ptc.PloneTestCase):
    """We use this base class for all the tests in this package. If necessary,
    we can put common utility or setup code in here.
    """



class GetPaidPayPalTestCase(GetPaidTestCase):

    def setUp( self ):
        # coreSetUp( )
        super(GetPaidPayPalTestCase, self).setUp()
    
    def tearDown( self ):
        super(GetPaidPayPalTestCase, self).tearDown()
    

