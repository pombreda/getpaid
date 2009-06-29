from zope.component import getUtility
from getpaid.core.interfaces import IPaymentProcessor
from getpaid.core.interfaces import IOrderManager

# Which classes we subclass
from Products.PloneGetPaid.browser import checkout as base

from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile

__author__ = "Mikko Ohtamaa <mikko.ohtamaa@twinapex.com> http://www.twinapex.com"
__docformat__ = "epytext"
__license__ = "BSD"
__copyright__ = "2009 Twinapex Research"
    
class CheckoutReviewAndPay(base.CheckoutReviewAndPay):
    """ Null payment method review and pay page.
    
    1) Render purchase summary
    
    2) Render a <form> which handles the actual payment process.
       The <form> target is another view (CompletePaymentAndThankYou).
       
       <form> can be async (managed outside the workflow)
       or sync (managed by base.CheckoutReviewAndPay.makePayment)
           
    """
    
    template = ZopeTwoPageTemplateFile("templates/pay.pt")
    