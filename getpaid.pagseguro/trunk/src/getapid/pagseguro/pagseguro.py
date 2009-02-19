# This is a very initial project to implement Pagseguro to get paid. It is been created over the getpaid.paypal wich seemed to be the closest approach
# Projeto inicial para implmentar um processador de pagamento do Pagseguro ao Getpaid. Esta sendo baseado na solução do getpaid.paypal

import urllib

from Products.CMFCore.utils import getToolByName
from zope import component
from zope import interface

# I think pagseguro just works with reais, so we can just print it instead of
# givving options
# from interfaces import IPaypalStandardOptions, IPaypalStandardProcessor

from Products.PloneGetPaid.interfaces import IGetPaidManagementOptions
from getpaid.core import interfaces as GetPaidInterfaces

_sites = {
    #servidor de teste do pagseguro ver: http://visie.com.br/pagseguro/ambientetestes.php
    "Sandbox": "localhost",     
    "Production": "pagseguro.uol.com.br",
    }

class PagSeguroProcessor( object ):
   
#    interface.implements( IPaypalStandardProcessor )

#    options_interface = IPaypalStandardOptions

    def __init__( self, context ):
        self.context = context


    def cart_post_button( self, order ):
       # options = IPaypalStandardOptions( self.context )
        siteroot = getToolByName(self.context, "portal_url").getPortalObject()
        manage_options = IGetPaidManagementOptions( siteroot )        
        cartitems = []
        idx = 1
#formulario de acordo com o exemplo em http://visie.com.br/pagseguro/carrinho-proprio.php
        _button_form = """<form target="pagseguro" method="post"
action="https://pagseguro.uol.com.br/security/webpagamentos/webpagto.aspx">
<input type="hidden" name="email_cobranca"
value="suporte@lojamodelo.com.br">
<input type="image" src="https://pagseguro.uol.com.br/Imagens/btnFinalizaBR.jpg"
    name="submit"
    alt="Make payments with PayPal - it's fast, free and secure!" />
</form>

"""
        _button_cart = """<input type="hidden" name="item_id_%(idx)s" value="%(item_name)s" >
<input type="hidden" name="item_descr_%(idx)s" value="%(item_description)s" >
<input type="hidden" name="item_quant_%(idx)s" value="%(quantity)s" >
<input type="hidden" name="item_valor_%(idx)s" value="%(amount)s" >
<input type="hidden" name="item_peso_%(idx)s" value"%(peso)s" >

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
        returnURL = "%s/@@getpaid-thank-you" % siteURL
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
   
    def capture(self, order, price):
        # always returns async - just here to make the processor happy
        return GetPaidInterfaces.keys.results_async

    def authorize( self, order, payment ):
        pass


