"""
"""
import urllib

from zope import interface
from zope.app.component.hooks import getSite

from interfaces import IPaypalStandardOptions, IPaypalStandardProcessor
from getpaid.core.interfaces import IRecurringLineItem

from Products.PloneGetPaid.interfaces import IGetPaidManagementOptions
from getpaid.core import interfaces as GetPaidInterfaces

_sites = {
    "Sandbox": "www.sandbox.paypal.com",
    "Production": "www.paypal.com",
    }
    
class PaypalOrderWrapper(object):
    """ adapter of standard getpaid order object to add paypal functions
    """
    
    def __init__(self, context):
        self.context = context
        
    def is_recurring(self):
        """ recurring payment orders have only 1 item and it is a recurring item
        """
        order_items = self.context.shopping_cart.values()
        if len(order_items) == 1 and IRecurringLineItem.providedBy(order_items[0]):
            return True
            
        return False

class PaypalBaseButton(object):
    
    def __init__(self, order):
        self.order = order
        siteroot = getSite()
        self.options = IPaypalStandardOptions(siteroot)
        self.manage_options = IGetPaidManagementOptions(siteroot)
        site_url = siteroot.absolute_url()
        self.return_url = "%s/@@getpaid-thank-you" % site_url
        self.ipn_url = "%s/%s" % (site_url, urllib.quote_plus("@@getpaid-paypal-ipnreactor"))
    
class PaypalRecurringButton(PaypalBaseButton):
    
    unit_token_map = {'months':'M',}
    
    def __call__(self):
        """ return a properly assembled button for recurring payments
        """
        
        _button_form = """<form style="display:inline;" action="https://%(site)s/cgi-bin/webscr" method="post" id="paypal-button">
<input value="_xclick-subscriptions" name="cmd" type="hidden" />
<input name="a3" type="hidden" value="%(cost)s"/>
<input name="p3" type="hidden" value="%(interval)s"/>
<input name="t3" type="hidden" value="%(unit)s"/>
<input name="srt" type="hidden" value="%(total_occurrences)s"/>
<input name="item_name" type="hidden" value="%(item_name)s" />
<input name="src" type="hidden" value="1" />
<input name="sra" type="hidden" value="1" />
<input type="hidden" name="upload" value="1" />
<input type="hidden" name="business" value="%(merchant_id)s" />
<input type="hidden" name="currency_code" value="%(currency)s" />
<input type="hidden" name="return" value="%(return_url)s" />
<input type="hidden" name="cbt" value="Return to %(store_name)s" />
<input type="hidden" name="rm" value="2" />
<input type="hidden" name="notify_url" value="%(IPN_url)s" />
<input type="hidden" name="invoice" value="%(order_id)s" />
<input type="hidden" name="no_note" value="1" />
<input type="image" src="http://%(site)s/en_US/i/btn/x-click-but01.gif"
    name="submit"
    alt="Make payments with PayPal - it's fast, free and secure!" />
</form>
"""

        item = self.order.shopping_cart.values()[0]
        formvals = {
            "site": _sites[self.options.server_url],
            "merchant_id": self.options.merchant_id,
            "return_url": self.return_url,
            "currency": self.options.currency,
            "IPN_url" : self.ipn_url,
            "order_id" : self.order.order_id,
            "store_name": self.manage_options.store_name,
            "item_name": item.name,
            "item_number" : item.product_code,
            "cost": item.cost,
            "quantity": item.quantity,
            "unit": self.unit_token_map[item.unit],
            "interval": item.interval,
            "total_occurrences": item.total_occurrences,
            }
            
        return _button_form % formvals
    
class PaypalStandardButton(PaypalBaseButton):
    
    def __call__(self):
        """ return a properly assembled button for one-time payments
        """
        cartitems = []
        # idx = 1
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
        for index, item in enumerate(self.order.shopping_cart.values()):
            # last-minute sanity check for mixed recurring and non-recurring items
            if IRecurringLineItem.providedBy(item):
                msg = "Shopping cart may not contain both one-time and recurring payment items"
                raise Exception(msg)
            
            idx = index + 1
            v = _button_cart % {"idx": idx,
                                "item_name": item.name,
                                "item_number" : item.product_code,
                                "amount": item.cost,
                                "quantity": item.quantity,}
            cartitems.append(v)
        
        formvals = {
            "site": _sites[self.options.server_url],
            "merchant_id": self.options.merchant_id,
            "cart": ''.join(cartitems),
            "return_url": self.return_url,
            "currency": self.options.currency,
            "IPN_url" : self.ipn_url,
            "order_id" : self.order.order_id,
            "store_name": self.manage_options.store_name,
            }
            
        return _button_form % formvals

class PaypalStandardProcessor( object ):
   
    interface.implements( IPaypalStandardProcessor, GetPaidInterfaces.IRecurringPaymentProcessor )

    options_interface = IPaypalStandardOptions

    def __init__( self, context ):
        self.context = context
        
    def cart_post_button( self, order ):
        
        porder = PaypalOrderWrapper(order)
        if porder.is_recurring():
            return PaypalRecurringButton(order)()
        else:
            return PaypalStandardButton(order)()
    
    def capture(self, order, price):
        # always returns async - just here to make the processor happy
        return GetPaidInterfaces.keys.results_async

    def authorize( self, order, payment ):
        pass