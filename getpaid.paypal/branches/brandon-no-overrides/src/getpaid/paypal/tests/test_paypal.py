import re
import unittest
from getpaid.core import interfaces as igetpaid
from Products.Five import fiveconfigure
from Products.Five import zcml
from Products.Five.testbrowser import Browser
from Products.PloneGetPaid import interfaces
from Products.PloneGetPaid.interfaces import IGetPaidManagementOptions
from Products.PloneGetPaid.tests.base import PloneGetPaidFunctionalTestCase
from Products.PloneTestCase.layer import onsetup
from zope.interface import alsoProvides



@onsetup
def setup_product():
    fiveconfigure.debug_mode = True
    import getpaid.paypal
    zcml.load_config('configure.zcml', getpaid.paypal)
    # roadrunner doesn't work without this
    import Products.PloneGetPaid
    zcml.load_config('configure.zcml', Products.PloneGetPaid)
    fiveconfigure.debug_mode = False

setup_product()


class PayPalFunctionalTest(PloneGetPaidFunctionalTestCase):
    def test_button_invoice_field(self):
        browser = Browser()
        browser.handleErrors = False
        membership = self.portal.portal_membership
        membership.addMember('testmanager', 'secret',
                 ['Member', 'Manager'], [])
        membership.addMember('testcustomer', 'secret',
                 ['Member', 'Manager'], [])
        browser.addHeader('Authorization',
                'Basic %s:%s' % ('testmanager', 'secret'))

        self.portal.portal_quickinstaller.installProduct('PloneGetPaid')
        # Some code adapted from 
        # Products/PloneGetPaid/tests/test_functional_browser_checkout.txt
        # But here we configure PloneGetPaid programmatically
        # to make he test faster
        configuration = interfaces.IGetPaidManagementOptions(self.portal)

        configuration.contact_email = 'info@plonegetpaid.com'
        configuration.store_name = 'Test this fake company'
        configuration.contact_country = 'US'
        configuration.payment_processor = 'Testing Processor'
        configuration.allow_anonymous_checkout = True
        options = IGetPaidManagementOptions(self.portal)
        options.buyable_types = ['Link', 'Event']
        options.donate_types = ['Document']
        options.shippable_types = ['Document']
        # enable Paypal payment processor!
        # We can't do this from testbrowser: it requires JavaScript
        settings = interfaces.IGetPaidManagementOptions(self.portal)
        settings.offsite_payment_processors = ['paypal']
        self.loginAsPortalOwner()
        self.portal.invokeFactory( 'Link', 'test-link')
        link_object = self.portal['test-link']
        link_object.setRemoteUrl('http://plonegetpaid.com/')
        alsoProvides(link_object, interfaces.IBuyableMarker)
        igetpaid.IBuyableContent(link_object).price = 12.50
        link_object.reindexObject()

        browser.open(link_object.absolute_url())
        browser.getControl('Add to Cart').click()
        browser.getControl('Continue Shopping').click()
        self.failUnless('Contains <span>1</span> Items' in browser.contents)

        self.failUnless('paypal' in browser.contents)
        paypal_form = self.get_paypal_form(browser.contents)
        order_id = self.get_field_value(paypal_form, 'invoice')
        # Now we place another order as another user and check 
        # that the order_id is  different
        another_browser = Browser()
        another_browser.addHeader('Authorization',
                'Basic %s:%s' % ('testcustomer', 'secret'))
        another_browser.open(link_object.absolute_url())
        another_browser.getControl('Add to Cart').click()
        another_browser.getControl('Continue Shopping').click()
        other_paypal_form = self.get_paypal_form(another_browser.contents)
        other_order_id = self.get_field_value(other_paypal_form, 'invoice')
        self.failIfEqual(order_id, other_order_id)
        # the price of th first element is in the amount_1 field
        price = float(self.get_field_value(other_paypal_form, 'amount_1'))
        self.failUnlessAlmostEqual(price, 12.5)

    def get_paypal_form(self, htmlpage):
        "returns the first PayPal form in the proided htmlpage using the re module"
        # A real XML parser would be better IMO, but we use re not to add a dependency
        return re.findall("<form[^>]*paypal[^>]*>.*?</form>", htmlpage,
                          re.MULTILINE|re.DOTALL)[0]
    def get_field_value(self, htmlform, fieldname):
        "Returns the value of the 'fieldname' input tag using regular expressions"
        return re.findall('<input [^>]*name="' + fieldname + '"[^>]*value="([^"]*)"',
                          htmlform)[0]


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(PayPalFunctionalTest),
    ))
