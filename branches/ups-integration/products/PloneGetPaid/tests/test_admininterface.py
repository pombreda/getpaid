"""Unit tests for setting admin interface options.
"""

from unittest import TestSuite, makeSuite
from base import PloneGetPaidTestCase
from Products.PloneGetPaid import interfaces, vocabularies
from Products.CMFCore.utils import getToolByName

class testAdminInterface(PloneGetPaidTestCase):

    manage_options = interfaces.IGetPaidManagementOptions( portal )
    
    def afterSetUp(self):
        self.setRoles(('Manager',))

    def testSetupPaymentProcessor( self ):
        """Test setting a payment processor."""
        #get the list of payment processors and get the first processor in the list
        our_payment_processor = "Google Checkout"
        manage_options.payment_processor = [our_payment_processor]
        self.failUnless(our_payment_processor in manage_options.payment_processor)


    def testSetupCurrency( self ):
        """Test setting a currency."""
        #set the currency in the GetPaid admin options to US
        our_currency = "US"
        manage_options.currency = [our_currency]
        #test to see if it was set properly
        self.failUnless(our_currency in manage_options.currency)


    def testSetupDisclaimer( self ):
        """Test setting a disclaimer."""
        our_disclaimer = "This is a disclaimer"
        manage_options.disclaimer = [our_disclaimer]
        #test to see if it was set properly
        self.failUnless(our_disclaimer in manage_options.disclaimer)

    def testSetupShipping( self ):
        """Test setting a shipping method."""
        our_shipping_method = "UPS"
        manage_options.shipping = [our_shipping_method]
        #test to see if it was set properly
        self.failUnless(our_shipping_method in manage_options.shipping_method)

    def testSetupTax( self ):
        """Test setting tax rate."""
        our_tax_method = "Flat Rate"
        manage_options.tax_method = [our_tax_method]
        #test to see if it was set properly
        self.failUnless(our_tax_method in manage_options.tax_method)

    def testSetupDiscounts( self ):
        """Test setting up discounts."""
        our_discounts = "10%"
        manage_options.discounts = [our_discounts]
        #test to see if it was set properly
        self.failUnless(our_discounts in manage_options.discounts)

    def testSetupCreditcards( self ):
        """Test setting acceptable credit cards."""
        our_credit_card = "VISA"
        manage_options.credit_cards = [our_credit_card]
        #test to see if it was set properly
        self.failUnless(our_credit_card in manage_options.credit_cards)

def test_suite():
    suite = TestSuite()
    suite.addTest(makeSuite(testAdminInterface))
    return suite
