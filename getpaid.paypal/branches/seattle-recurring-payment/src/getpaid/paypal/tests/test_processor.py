import unittest

from zope import component
from zope.component import getMultiAdapter, provideUtility
from zope.app.component.hooks import getSite
from zope.annotation.interfaces import IAnnotations

from getpaid.core import cart, item
from getpaid.core.interfaces import IOrderManager, AddRecurringItemException, RecurringCartItemAdditionException

from getpaid.paypal.ipn.submit_handler import IPNListener
from getpaid.paypal.paypal import PaypalRecurringButton
from getpaid.paypal.tests.base import GetPaidPaypalPloneTestCase
from getpaid.paypal.tests import mocks

class ProcessorTests(GetPaidPaypalPloneTestCase):
    def afterSetUp(self):
        self.portal = getSite()
        self.cart = cart.ShoppingCart()
        self.nonrecurring = item.LineItem()
        self.nonrecurring.name = "Non-recurring"
        self.nonrecurring.quantity = 1
        self.nonrecurring.cost = 25
        self.nonrecurring.item_id = "nonrecurring"
        self.recurring = item.RecurringLineItem()
        self.recurring.name = "Recurring"
        self.recurring.quantity = 1
        self.recurring.cost = 25
        self.recurring.item_id = "recurring"
    
    def beforeTearDown(self):
        pass
    
    def test_recurring_processor(self):
        processor = PaypalRecurringButton(self.)
    # def tearDown(self):
    #     super(ProcessorTests, self).tearDown()
    #     self.recurring = None
    #     self.nonrecurring = None
    #     self.manager = None
    #     
    # def test_view_available(self):
    #     data = {}
    #     view = self._buildForm(self.portal, self.viewname, data)
    #     self.failUnless(view is not None)
    # 
    # def test_ipn_handler(self):
    #     data = mocks.CART_IPN_MOCK()
    #     view = self._buildForm(self.portal, self.viewname, data)
    #     import pdb; pdb.set_trace( )
    #     view.process()
    #     order = self.mock_order_manager.get('729492128')
    #     # ipn = IAnnotations(order)[config.FTI_IPN_KEY]
    #     # self.failIf(ipn is None)
    #     # self.failUnless('payment_fee' in ipn)
    # 
    # def _buildForm(self, context, viewname, formdata):
    #     test_request = self.app.REQUEST
    #     test_request.form = formdata
    #     test_request.RESPONSE = test_request.response
    #     view = component.getMultiAdapter((context, test_request), 
    #                                         name=viewname)
    #     
    #     return view

        

def test_suite():
    return unittest.TestSuite((
        # Unit tests
        unittest.makeSuite(ProcessorTests),
        ))
