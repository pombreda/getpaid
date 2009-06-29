"""

    Site setup screens contributed by this payment processor.

"""

# Views we are going to subclass are imported from here
from Products.PloneGetPaid.browser import admin as base

class PaymentProcessor(base.PaymentProcessor):
    """ Simple wrapper to render payment processor settings screen using a certain payment processor """

    def getPaymentProcessorName(self):
        # Match getpaid.core.interfaces.IPaymentProcessor name
        return "Paypal Website Payments Standard"