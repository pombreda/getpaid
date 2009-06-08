"""

    Setup unit test suite for getpaid.paymentprocessors package. 

"""

from Testing import ZopeTestCase as ztc
from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase.layer import onsetup

from Products.PloneGetPaid.tests.base import PloneGetPaidTestCase

@onsetup
def setup_package():
    fiveconfigure.debug_mode = True
    import getpaid.paymentprocessors
    print "Loading ZCML"
    zcml.load_config('configure.zcml', getpaid.paymentprocessors)
    fiveconfigure.debug_mode = False        
    
    ztc.installPackage('getpaid.paymentprocessors')
    
setup_package()
    
class PaymentProcessorTestCase(PloneGetPaidTestCase):
    """ Base class for getpaid.paymentprocessors unit tests """
    
    def afterSetUp( self ):
        PloneGetPaidTestCase.afterSetUp(self)
        
