"""
"""
from zope import component
from zope import interface

from interfaces import IPaypalStandardOptions
from interfaces import IPaypalStandardProcessor

_sites = {
    "Sandbox": "www.sandbox.paypal.com",
    "Production": "www.paypal.com",
    }

    paypalurl = self.plonegetpaidGetPayPalUrl()
    merchantid = self.plonegetpaidGetPayPalUserName()

class PaypalStandardProcessor( object ):
   
    interface.implements( IPaypalStandardProcessor )

    options_interface = IPaypalStandardOptions

    def __init__( self, context ):
        self.context = context

    def cart_post_button( self, cart ):
        options = IPaypalStandardOptions( self.context )
        cartitems = []
        idx = 1
        for item in cart.values():
            v = _button_cart % {"idx": idx,
                                "itemname": item.name,
                                "amount": item.cost,
                                "quantity": item.quantity,}
            cartitems.append(v)
        formvals = {
            "site": paypalurl,
            "merchant_id": merchantid,
            "cart": ''.join(cartitems),
            "order_number": order.order_id,
            }
        return _button_form % formvals

    def authorize( self, order, payment ):
        pass

_button_form = """\
<form action="https://%(site)s/cgi-bin/webscr" method="post">
<input type="hidden" name="cmd" value="_cart"/>
<input type="hidden" name="business" value="%(merchant_id)s"/>
<input type="hidden" name="currency_code" value="USD"/>
<input type="hidden" name="invoice" value="%(order_number)s"/>
%(cart)s
<input type="image" src="http://%(site)s/en_US/i/btn/x-click-but01.gif"
       name="submit"
       alt="Make payments with PayPal - it's fast, free and secure!"/>
</form>"""

_button_cart = """
<input type="hidden" name="item_name_%(idx)s" value="%(itemname)s"/>
<input type="hidden" name="amount_%(idx)s" value="%(amount)s"/>
<input type="hidden" name="quantity_%(idx)s" value="%(quantity)s"/>
"""


        
        url = self.plonegetpaidGetPayPalUrl()
        
        self.plone_log(
            'PayPalIpnResponder::   Opening URL: ' + repr(url) + ' ... ')
        # TODO: is this dangerous for other products?
        socket.setdefaulttimeout(120)
        try:
            connection = urllib2.urlopen(url, paramData)
        except URLError:
            raise IOError, 'IPN post-back failed'
        self.plone_log('PayPalIpnResponder::   Reading response ... ')
        response = connection.read()
        self.plone_log('PayPalIpnResponder::   Response: ' + repr(response))
        connection.close()
        
        # convert params into an easy to use dictionary:
        newParams = {}
        for (key, value) in params:
            newParams[key] = value
        params = newParams
        
        if response == 'VERIFIED':
            self._handleVerifiedPayPayRequest(response, params)
        elif response == 'INVALID':
            self._handleInvalidPayPayRequest(response, params)
        else:
            self._handleUnknownPayPayRequest(response, params)
            
        self.previousPayPalTransactionId = params['txn_id']
    
    
    def _handleVerifiedPayPayRequest(self, response, params):
        
        txnId = params['txn_id']
        self.plone_log('PayPalIpnResonder:: request VERIFIED; txn_id=' + txnId)
