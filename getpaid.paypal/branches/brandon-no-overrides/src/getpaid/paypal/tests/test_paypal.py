import re
import unittest
from Products.Five import fiveconfigure
from Products.Five import zcml
from Products.Five.testbrowser import Browser
from Products.PloneGetPaid import interfaces
from Products.PloneGetPaid.tests.base import PloneGetPaidFunctionalTestCase
from Products.PloneTestCase.layer import onsetup
from Testing import ZopeTestCase as ztc



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
        # we test the test setup here: is the paypal zcml loaded?
        # if not, this should trigger a 404 error
        browser.open(self.portal.absolute_url() + '/@@paypal-thank-you')
        # ...and then, some code copied from 
        # Products/PloneGetPaid/tests/test_functional_browser_checkout.txt

        browser.open(self.portal.absolute_url() +
                     '/@@manage-getpaid-identification')
        browser.getControl('Contact Email').value = 'info@plonegetpaid.com'
        browser.getControl( name="form.store_name").value = 'Test this fake company'
        browser.getControl('Contact Country').value = ['US']
        browser.getControl('Apply').click()
        browser.getLink('GetPaid').click()
        browser.getLink('Content Types').click()
        browser.getLink('GetPaid').click()
        browser.getLink('Payment Options').click()
        browser.getControl(name = 'form.payment_processor').displayValue = ['Testing Processor']
        browser.getControl(name = 'form.allow_anonymous_checkout.used').value = 'on'
        browser.getControl(name = 'form.allow_anonymous_checkout').value = True
        browser.getControl('Apply').click()
        browser.getLink('GetPaid').click()
        browser.getLink('Payment Processor Settings').click()
        browser.getControl(name="form.onsite.allow_authorization").displayValue = ['allow_authorization']
        browser.getControl(name="form.onsite.allow_capture").displayValue = ['allow_capture']
        browser.getControl(name="form.onsite.allow_refunds").displayValue = ['allow_refund']    
        browser.getControl('Apply').click()
        browser.getLink('GetPaid').click()
        browser.getLink('Legal Disclaimers').click()
        browser.getControl(name='form.disclaimer').value = 'Test disclaimer'
        browser.getControl(name='form.privacy_policy').value = 'Test privacy policy'
        browser.getControl('Apply').click()
        from Products.PloneGetPaid.interfaces import IGetPaidManagementOptions
        options = IGetPaidManagementOptions(self.portal)
        options.buyable_types = ['Link', 'Event']
        options.donate_types = ['Document']
        options.shippable_types = ['Document']
        # enable Paypal payment processor!
        # We can't do this from testbrowser: it requires JavaScript
        settings = interfaces.IGetPaidManagementOptions(self.portal)
        settings.offsite_payment_processors = ['paypal']
        # But we can check if it's in place
        browser.open(self.portal.absolute_url() +
                     '/@@manage-getpaid-payment-options')
        # Check that the processor is in the "to" widget, i.e. available
        enabled_processors = browser.getControl(
            name="form.offsite_payment_processors.to").options
        self.failUnless('PayPal Checkout') in enabled_processors


        browser.open('http://nohost/plone')
        browser.getLink('Link').click()
        browser.getControl('Title').value = 'Test Link'
        browser.getControl('URL').value = 'http://plonegetpaid.com/'
        browser.getControl('Save').click()

        browser.getLink('Make Buyable').click()
        browser.getControl('Price').value = '12.50'
        browser.getControl('Activate').click()
        browser.getControl('Add to Cart').click()
        browser.getControl('Continue Shopping').click()
        self.failUnless('Contains <span>1</span> Items' in browser.contents)

        self.failUnless('paypal' in browser.contents)
        # A real XML parser would be better IMO, but we use re not to add a dependency
        paypal_form = self.get_paypal_form(browser.contents)
        re.findall("<form[^>]*paypal[^>]*>.*?</form>", browser.contents,
                   re.MULTILINE|re.DOTALL)[0]
        order_id = self.get_order_id(paypal_form)
        # Now we place another order as another user and check 
        # that the order_id is  different
        another_browser = Browser()
        another_browser.addHeader('Authorization',
                'Basic %s:%s' % ('testcustomer', 'secret'))
        another_browser.open(self.portal['test-link'].absolute_url())
        another_browser.getControl('Add to Cart').click()
        another_browser.getControl('Continue Shopping').click()
        other_paypal_form = self.get_paypal_form(another_browser.contents)
        other_order_id = self.get_order_id(other_paypal_form)
        self.failIfEqual(order_id, other_order_id)
    def get_paypal_form(self, htmlpage):
        return re.findall("<form[^>]*paypal[^>]*>.*?</form>", htmlpage,
                          re.MULTILINE|re.DOTALL)[0]
    def get_order_id(self, htmlform):
        return re.findall('<input [^>]*name="invoice"[^>]*value="([^"]*)"',
                          htmlform)[0]


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(PayPalFunctionalTest),
    ))
