from Products.PloneGetPaid.browser.checkout import CheckoutReviewAndPay
from getpaid.core.interfaces import IPaymentProcessor
from Products.PloneGetPaid.interfaces import IGetPaidManagementOptions
from zope.component import getAdapter
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile

class PaypalCheckoutPayment(CheckoutReviewAndPay):
    """
    We need to override some of the methods for the checkout
    as the checkout process is different for PayPal
    """
    template = ZopeTwoPageTemplateFile("templates/checkout-review-pay.pt")
        
    def buy_now(self):
        cart = getUtility(IShoppingCartUtility).get(self.context, create=True)
        manage_options = IGetPaidManagementOptions(self.context)
        processor_name = manage_options.payment_processor
        processor = getAdapter(self.context, IPaymentProcessor, processor_name)
        #order = self.createOrder()
        #order.processor_id = processor_name
        #order.finance_workflow.fireTransition( "create" )
        
        return processor.cart_post_button(cart)

