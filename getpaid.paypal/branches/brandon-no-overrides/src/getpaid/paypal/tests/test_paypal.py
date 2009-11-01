from Products.PloneGetPaid.tests.base import PloneGetPaidFunctionalTestCase
import unittest
from Products.PloneGetPaid import interfaces
from Products.Five.testbrowser import Browser
from Products.PloneTestCase.layer import onsetup
from Products.Five import fiveconfigure
from Products.Five import zcml
from Testing import ZopeTestCase as ztc



@onsetup
def setup_product():
    fiveconfigure.debug_mode = True
    import getpaid.paypal
    zcml.load_config('configure.zcml', getpaid.paypal)
    fiveconfigure.debug_mode = False
    ztc.installPackage('getpaid.paypal')

setup_product()


class PayPalFunctionalTest(PloneGetPaidFunctionalTestCase):
    def test_button_invoice_field(self):
        browser = Browser()
        # we test the test setup here: is the paypal zcml loaded?
        # if not, this should trigger a 404 error
        browser.open(self.portal.absolute_url() + '/@@paypal-thank-you')
        # ...and then, some code copied from 
        # Products/PloneGetPaid/tests/test_functional_browser_checkout.txt
        membership = self.portal.portal_membership
        membership.addMember('testmanager', 'secret',
                 ['Member', 'Manager'], [])

        browser.getLink('Log in').click()
        browser.getControl('Login Name').value = 'testmanager'
        browser.getControl('Password').value = 'secret'
        browser.getControl('Log in').click()

        self.portal.portal_quickinstaller.installProduct('PloneGetPaid')
        browser.getLink('Home').click()

        browser.getLink('Site Setup').click()
        browser.getLink('GetPaid').click()
        browser.getLink('Site Profile').click()
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
        browser.getLink('GetPaid').click() 
        from Products.PloneGetPaid.interfaces import IGetPaidManagementOptions
        options = IGetPaidManagementOptions(self.portal)
        options.buyable_types = ['Link', 'Event']
        options.donate_types = ['Document']
        options.shippable_types = ['Document']
        # enable Paypal payment processor!
        settings = interfaces.IGetPaidManagementOptions(self.portal)
        settings.offsite_payment_processors = ['PayPal Checkout']
        # XXX it doesn't seem to be enabled, really!

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

        #This will fail
        self.failUnless('paypal' in browser.contents)

def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(PayPalFunctionalTest),
    ))
