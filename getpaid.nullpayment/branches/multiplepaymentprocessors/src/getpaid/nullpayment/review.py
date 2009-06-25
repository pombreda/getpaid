from getpaid.wizard.interfaces import IWizardStepOverlay

# Which classes we subclass
from Products.GetPaid.browser import checkout as base


    
class CheckoutReviewAndPay(base.CheckoutReviewAndPay):
    """ Null payment method review and pay page """
    
    
    