from Products.PloneGetPaid.browser.checkout import CheckoutReviewAndPay
from getpaid.core.interfaces import IPaymentProcessor
from Products.PloneGetPaid.interfaces import IGetPaidManagementOptions
from zope.component import getAdapter
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile

class OgoneCheckoutPayment(CheckoutReviewAndPay):
    """
    We need to override some of the method for the checkout
    as the checkout process is different for ogone
    """
    template = ZopeTwoPageTemplateFile("templates/checkout-review-pay.pt")

    def setUpWidgets( self, ignore_request=False ):
        retval = super(OgoneCheckoutPayment, self).setUpWidgets(ignore_request)
        return retval

    @form.action(u"Make Payment", name="make-payment")
    def makePayment(self, action, data):
        """ create an order, and submit to the processor
        """
        manage_options = IGetPaidManagementOptions( self.context )
        processor_name = manage_options.payment_processor

        if not processor_name:
            raise RuntimeError( "No Payment Processor Specified" )

        processor = getAdapter( self.context,
                                IPaymentProcessor,
                                processor_name )

        order = self.createOrder()
        order.processor_id = processor_name
        order.finance_workflow.fireTransition( "create" )

        # extract data to our adapters
        result = processor.authorize( order, None )

