import os
from urllib import urlencode

from zope.interface import implements, Interface
from zope import component

from AccessControl import getSecurityManager
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from Products.PloneGetPaid.interfaces import PayableMarkers, IGetPaidCartViewletManager, INamedOrderUtility
from Products.PloneGetPaid.interfaces import IGetPaidManagementOptions, IConditionalViewlet, IVariableAmountDonatableMarker
from Products.PloneGetPaid import sessions
from Products.PloneGetPaid import config

import getpaid.core.interfaces

from Products.statusmessages.interfaces import IStatusMessage

from Products.PloneGetPaid.browser.cart import ShoppingCart

from getpaid.atshop import atshopMessageFactory as _

from getpaid.atshop.interfaces import IVariationItemFactory, IBuyableMarker

class BaseShoppingAddView(ShoppingCart):
    """ Abstract base class for processing the add cart item requests


    GetPaid view to process form request to add item variation to the cart.

    Add variation items to the cart.

    HTTP request parameters:

        * quantity

        * product_code (optional)

        * add_item flag

    """

    def notifyUser(self, item):

        # Notify user that the shopping cart has been updated
        messages = IStatusMessage(self.request)
        messages.addStatusMessage(u"%d %s items in the shopping cart " % (item.quantity, item.name), type="info")

    def isContextAddable( self ):
        return IBuyableMarker.providedBy(self.context)

    def __call__( self ):
        if self.request.has_key('add_item'):
            self.addToCart()

        # Keep shopping...
        self.request.response.redirect(self.context.absolute_url())


class AddVariantView(BaseShoppingAddView):
    """ Add items with variations to cart """

    def addToCart( self ):
        """ Add item to the cart based on HTTP POST request
        """
        # GEt line item creator
        item_factory = component.getMultiAdapter( (self.cart, self.context), IVariationItemFactory)

        # Decode HTTP POST input
        qty = int(self.request.get('quantity', 1))
        product_code = self.request.get("product_code")

        # Update the cart
        item = item_factory.create(product_code, quantity=qty)

        if not item:
            # Item already exist in the cart and was not created
            item = self.cart[product_code]

        self.notifyUser(item)



class AddProductView(BaseShoppingAddView):
    """ Add items without variations to cart.
    """


    def addToCart( self ):
        """ Add item to the cart based on HTTP POST request
        """
        # GEt line item creator
        item_factory = component.getMultiAdapter( (self.cart, self.context), getpaid.core.interfaces.ILineItemFactory )

        # Decode HTTP POST input
        qty = int(self.request.get('quantity', 1))

        # Update the cart
        item = item_factory.create(quantity=qty)

        if not item:
            # Item already exist in the cart and was not created
            item = self.cart[self.context.UID()]

        self.notifyUser(item)

