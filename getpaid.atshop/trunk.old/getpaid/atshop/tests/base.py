"""Test setup for integration and functional tests.

When we import PloneTestCase and then call setupPloneSite(), all of
Plone's products are loaded, and a Plone site will be created. This
happens at module level, which makes it faster to run each test, but
slows down test runner startup.
"""

from zope import component

from Products.Five import zcml
from Products.Five import fiveconfigure

from Testing import ZopeTestCase as ztc

from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

import getpaid.core.interfaces

# When ZopeTestCase configures Zope, it will *not* auto-load products
# in Products/. Instead, we have to use a statement such as:
#   ztc.installProduct('SimpleAttachment')
# This does *not* apply to products in eggs and Python packages (i.e.
# not in the Products.*) namespace. For that, see below.
# All of Plone's products are already set up by PloneTestCase.

@onsetup
def setup_product():
    """Set up the package and its dependencies.

    The @onsetup decorator causes the execution of this body to be
    deferred until the setup of the Plone site testing layer. We could
    have created our own layer, but this is the easiest way for Plone
    integration tests.
    """

    # Load the ZCML configuration for the example.tests package.
    # This can of course use <include /> to include other packages.

    fiveconfigure.debug_mode = True
    import getpaid.atshop
    zcml.load_config('configure.zcml', getpaid.atshop)
    fiveconfigure.debug_mode = False

    # We need to tell the testing framework that these products
    # should be available. This can't happen until after we have loaded
    # the ZCML. Thus, we do it here. Note the use of installPackage()
    # instead of installProduct().
    # This is *only* necessary for packages outside the Products.*
    # namespace which are also declared as Zope 2 products, using
    # <five:registerPackage /> in ZCML.

    # We may also need to load dependencies, e.g.:
    #   ztc.installPackage('borg.localrole')

    ztc.installProduct('PloneGetPaid')
    ztc.installPackage('getpaid.atshop')

# The order here is important: We first call the (deferred) function
# which installs the products we need for this product. Then, we let
# PloneTestCase set up this product on installation.

setup_product()
ptc.setupPloneSite(products=["Products.PloneGetPaid", 'getpaid.atshop'])


from Products.PloneGetPaid.tests.base import PloneGetPaidTestCase, PloneGetPaidFunctionalTestCase

class TestCase(PloneGetPaidTestCase):
    """We use this base class for all the tests in this package. If
    necessary, we can put common utility or setup code in here. This
    applies to unit test cases.
    """

    def afterSetUp(self):
        PloneGetPaidTestCase.afterSetUp(self)

    def create_cart(self):
        cart = component.getUtility(getpaid.core.interfaces.IShoppingCartUtility).get(self.portal, create=True)
        return cart

class FunctionalTestCase(PloneGetPaidFunctionalTestCase):
    """We use this class for functional integration tests that use
    doctest syntax. Again, we can put basic common utility or setup
    code in here.
    """

    def afterSetUp(self):

        PloneGetPaidFunctionalTestCase.afterSetUp(self)

        roles = ('Member', 'Contributor')
        self.portal.portal_membership.addMember('contributor',
                                                'secret',
                                                roles, [])

        from Products.Five.testbrowser import Browser

        self.browser = Browser()
        self.browser.open(self.portal.absolute_url())

        self.browser.handleErrors = False
        self.portal.error_log._ignored_exceptions = ()

        def raising(self, info):
            import traceback
            traceback.print_tb(info[2])
            print info[1]

        from Products.SiteErrorLog.SiteErrorLog import SiteErrorLog
        SiteErrorLog.raising = raising

        from Products.PloneTestCase.setup import portal_owner, default_password

         # Go admin
        self.browser.open(self.portal.absolute_url() + "/login_form")
        self.browser.getControl(name='__ac_name').value = portal_owner
        self.browser.getControl(name='__ac_password').value = default_password
        self.browser.getControl(name='submit').click()



# Sample text used to fill in variant information for the test products
VARIANTS_TEXT="""t-shirt-s; T-Shirt (S); 20.00
t-shirt-m; T-Shirt (M); 30.00
t-shirt-xl; T-Shirt (XL); 40.00
"""
