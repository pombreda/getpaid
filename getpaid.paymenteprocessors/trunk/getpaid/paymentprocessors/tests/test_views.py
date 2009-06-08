import unittest

from base import PaymentProcessorTestCase

from Products.Five import zcml
from zope.configuration.exceptions import ConfigurationError

from getpaid.paymentprocessors.registry import ProcessorEntry

configure_zcml = '''
<configure
    xmlns="http://namespaces.zope.org/zope"
    xmlns:five="http://namespaces.zope.org/five"
    xmlns:paymentprocessors="http://namespaces.plonegetpaid.com/paymentprocessors"
    i18n_domain="foo">
    
    <paymentprocessors:registerProcessor
       name="dummy"
       processor="getpaid.paymentprocessors.tests.dummies.DummyProcessor"
       selection_view="getpaid.paymentprocessors.tests.dummies.DummyButton"
       thank_you_view="getpaid.paymentprocessors.tests.dummies.DummyThankYou"
       />
    
</configure>'''

class TestViews(PaymentProcessorTestCase):
    """ Test ZCML directives """
    
    def enable(self):
        """ Install test views to the site """
        zcml.load_string(configure_zcml)
        
        # See that our processor got registered
        self.assertEqual(len(ProcessorEntry.registry.items()), 1)
        
        
    def render_selection_view(self):
        view = self.portal.restrictedTraver("@@getpaid-checkout-wizard")

    def test_selection_screen_no_processor(self):
        """ Render payment processor selection view screen """
        
        self.enable()
        
        self.render_selection_view()
        
    def test_selection_screen_one_processor(self):
        pass
    
    def test_selection_screen_n_processors(self):
        pass
    
            
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestViews))
    return suite
