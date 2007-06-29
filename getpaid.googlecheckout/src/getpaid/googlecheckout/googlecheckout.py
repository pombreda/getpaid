"""
"""
from zope import component
from zope import interface

from gchecky.controller import Controller
from gchecky import model as gmodel

class GController(gbase.Controller):
    pass

def gcart_item(entry):
    return gmodel.item_t(
        name = entry.name,
        description = entry.description,
        unit_price = gmodel.price_t(
            value = entry.cost,
            currency = 'USD'
            ),
        quantity = entry.quantity
        )

class GCartAdapter(object):
    """
    """
    def __init__(self, context):
        self.context = context
        self.gcart = gmodel.checkout_shopping_cart_t(
            shopping_cart = gmodel.shopping_cart_t(
                items = [gcart_item(entry) for entry in cart.values()]
                )
            )

    def toxml(self):
        return self.gcart.toxml()
        

class GoogleCheckoutProcessor( object ):
   
    implements( interfaces.IGoogleCheckoutProcessor )

    options_interface = interfaces.IGoogleCheckoutOptions

    def __init__( self, context ):
        self.context = context
        self._controller = None

    def getController( self ):
        if self._controller is None:
            options = interfaces.IGoogleCheckoutOptions( self.context )
            self._controller = GController(options.merchant_id,
                                           options.merchant_key,
                                           options.server_url == 'Sandbox')
        return self._controller

    controller = property(getController)

    def cart_post_button( self, cart ):
        prepared = self.controller.prepare_order(GCartAdapter(cart))
        return prepared

    def authorize( self, order, payment ):
        pass
