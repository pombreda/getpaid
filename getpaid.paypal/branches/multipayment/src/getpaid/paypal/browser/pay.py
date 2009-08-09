import urllib

# Zope imports
from zope.component import getUtility, getAdapter
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile

# Plone imports
from Products.CMFCore.utils import getToolByName

# GetPaid imports
import getpaid.core.interfaces
from getpaid.core.interfaces import IPaymentProcessor
from getpaid.paymentprocessors.interfaces import IPaymentMethodInformation
from Products.PloneGetPaid.browser import checkout as base

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getUtility

from Products.PloneGetPaid.interfaces import IGetPaidManagementOptions
from getpaid.core.interfaces import IShoppingCartUtility, IOrderManager
from getpaid.core.order import Order
from getpaid.core import payment

from cPickle import loads, dumps
from AccessControl import getSecurityManager

from getpaid.paypal.paypal import PaypalStandardProcessor
from getpaid.paypal.interfaces import IPaypalStandardOptions

_sites = {
    "Sandbox": "www.sandbox.paypal.com",
    "Production": "www.paypal.com",
    }


class CheckoutReviewAndPay(base.CheckoutReviewAndPay):
    """ Null payment method review and pay page.

    1) Render purchase summary

    2) Render a <form> which handles the actual payment process.
       The <form> target is another view (CompletePaymentAndThankYou).

       <form> can be async (managed outside the workflow)
       or sync (managed by base.CheckoutReviewAndPay.makePayment)
       
    TODO: Cart is destroyed on the last wizard step - fix this

    """

    template = ZopeTwoPageTemplateFile("templates/pay.pt")

    def renderPaypalForm(self, order):
        options = IPaypalStandardOptions( self.context )
        siteroot = getToolByName(self.context, "portal_url").getPortalObject()
        manage_options = IGetPaidManagementOptions( siteroot )        
        cartitems = []
        idx = 1
        _button_form = """<form style="display:inline;" action="https://%(site)s/cgi-bin/webscr" method="post" id="paypal-button">
<input type="hidden" name="cmd" value="_cart" />
<input type="hidden" name="upload" value="1" />
<input type="hidden" name="business" value="%(merchant_id)s" />
<input type="hidden" name="currency_code" value="%(currency)s" />
<input type="hidden" name="return" value="%(return_url)s" />
<input type="hidden" name="cbt" value="Return to %(store_name)s" />
<input type="hidden" name="rm" value="2" />
<input type="hidden" name="notify_url" value="%(IPN_url)s" />
<input type="hidden" name="invoice" value="%(order_id)s" />
<input type="hidden" name="no_note" value="1" />
%(cart)s
<input type="image" src="http://%(site)s/en_US/i/btn/x-click-but01.gif"
    name="submit"
    alt="Make payments with PayPal - it's fast, free and secure!" />
</form>
"""
        _button_cart = """<input type="hidden" name="item_name_%(idx)s" value="%(item_name)s" />
<input type="hidden" name="item_number_%(idx)s" value="%(item_number)s" />
<input type="hidden" name="amount_%(idx)s" value="%(amount)s" />
<input type="hidden" name="quantity_%(idx)s" value="%(quantity)s" />
"""
       
        for item in order.shopping_cart.values():
            v = _button_cart % {"idx": idx,
                                "item_name": item.name,
                                "item_number" : item.product_code,
                                "amount": item.cost,
                                "quantity": item.quantity,}
            cartitems.append(v)
            idx += 1
        siteURL = siteroot.absolute_url()
        # having to do some magic with the URL passed to Paypal so their system replaies properly
        returnURL = "%s/@@paypal-thank-you" % siteURL
        IPNURL = "%s/%s" % (siteURL, urllib.quote_plus("@@getpaid-paypal-ipnreactor"))
        formvals = {
            "site": _sites[options.server_url],
            "merchant_id": options.merchant_id,
            "cart": ''.join(cartitems),
            "return_url": returnURL,
            "currency": options.currency,
            "IPN_url" : IPNURL,
            "order_id" : order.order_id,
            "store_name": manage_options.store_name,
            }
        return _button_form % formvals

    def prepareOrder(self, processor_id):

        # processor id = Paypal Website Payments Standard

        site_root = getToolByName(self.context, "portal_url").getPortalObject()
 
        manage_options = IGetPaidManagementOptions( self.context )

        # we'll get the order_manager, create the new order, and store it.
        # createOrder() is defined in base.CheckoutReviewAndPay.createOrder()
        order = self.createOrder()

        order.finance_workflow.fireTransition('create')

        # register the payment processor name to make the workflow handlers happy
        order.processor_id = processor_id

        # TODO: This should happen after the payment has been accepted?
        order_manager = getUtility( IOrderManager )
        order_manager.store(order)

        # have to wait for the order to be created and the cart added for this to work
        order.finance_workflow.fireTransition('authorize')

        # save html for button - we'll destroy the cart later on
       
        #
        # TODO: Fix this... cart_post_button is not suitable name here
        #
       
        processor = getAdapter(site_root, getpaid.core.interfaces.IPaymentProcessor, processor_id)
       
        return order
       


    def getForm(self):
        """ Return the form code which takes to PayPal to complete the payment """

        payment_processor_name = self.wizard.getActivePaymentProcessor()

        site_root = getToolByName(self.context, "portal_url").getPortalObject()
        processor = getAdapter(site_root, getpaid.core.interfaces.IPaymentProcessor, payment_processor_name)
       
        # TODO: This destroyes cart and authorizes order even
        # though the user has not paid yet... FIX
        order = self.prepareOrder(payment_processor_name)
       
        html = self.renderPaypalForm(order)
       
        return html
       
        return processor.cart_post_button(order)


