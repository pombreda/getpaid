import unittest

from zope import component
from zope.component import getMultiAdapter, provideUtility
from zope.app.component.hooks import getSite
from zope.annotation.interfaces import IAnnotations

from getpaid.core import cart, item
from getpaid.core.interfaces import IOrderManager, AddRecurringItemException, RecurringCartItemAdditionException

from getpaid.paypal.ipn.submit_handler import IPNListener
from getpaid.paypal.tests.base import GetPaidPaypalPloneTestCase
from getpaid.paypal.tests import mocks

class MultiItemCartIPNTests(GetPaidPaypalPloneTestCase):
    def afterSetUp(self):
        def mock_verify(object):
            return True
        
        def mock_fill_in_order_data(object, notification, order):
            pass
                    
        self.portal = getSite()
        self.viewname = 'getpaid-paypal-ipnreactor'
        # super(MultiItemCartIPNTests, self).setUp()
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
        self.manager = component.getUtility(IOrderManager)
        # swap in some mocks to reduce our paperwork
        self.real_verify = IPNListener.verify
        IPNListener.verify = mock_verify
        
        # self.real_fill_in_order_data = IPNListener.fill_in_order_data
        # IPNListener.fill_in_order_data = mock_fill_in_order_data
        
        self.mock_order_manager = mocks.MockOrderManager()
        provideUtility(self.mock_order_manager)
    
    def beforeTearDown(self):
        IPNListener.verify = self.real_verify        
        
    def tearDown(self):
        super(MultiItemCartIPNTests, self).tearDown()
        self.recurring = None
        self.nonrecurring = None
        self.manager = None
        
    def test_view_available(self):
        data = {}
        view = self._buildForm(self.portal, self.viewname, data)
        self.failUnless(view is not None)
    
    def test_ipn_handler(self):
        data = mocks.CART_IPN_MOCK()
        view = self._buildForm(self.portal, self.viewname, data)
        view.process()
        order = self.mock_order_manager.get('729492128')
        # ipn = IAnnotations(order)[config.FTI_IPN_KEY]
        # self.failIf(ipn is None)
        # self.failUnless('payment_fee' in ipn)
    
    def _buildForm(self, context, viewname, formdata):
        test_request = self.app.REQUEST
        test_request.form = formdata
        test_request.RESPONSE = test_request.response
        view = component.getMultiAdapter((context, test_request), 
                                            name=viewname)
        
        return view

        

def test_suite():
    return unittest.TestSuite((
        # Unit tests
        unittest.makeSuite(MultiItemCartIPNTests),
        ))
