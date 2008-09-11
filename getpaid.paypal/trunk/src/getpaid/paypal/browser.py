from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from zope.component import getUtility, getAdapter

from Products.PloneGetPaid.interfaces import IGetPaidManagementOptions
from getpaid.core.interfaces import IPaymentProcessor, IShoppingCartUtility

class BuyNowButtonView(BrowserView):
    """Create a html page containing the Buy Now button
    """
    
    __call__ = ViewPageTemplateFile('buynowbutton.pt')
    
    def buy_now(self):
        cart = getUtility(IShoppingCartUtility).get(self.context, create=True)
        manage_options = IGetPaidManagementOptions(self.context)
        processor_name = manage_options.payment_processor
        processor = getAdapter(self.context, IPaymentProcessor, processor_name)
        return processor.cart_post_button(cart)