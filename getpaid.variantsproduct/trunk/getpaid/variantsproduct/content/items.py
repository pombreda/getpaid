"""

    Make variant items for the shopping cart

"""

__author__ = "Mikko Ohtamaa <mikko.ohtamaa@twinapex.com> http://www.twinapex.com"
__docformat__ = "epytext"
__license__ = "GPL"
__copyright__ = "2009 Twinapex Research"

import zope.interface
from zope import component
from zope.app.intid.interfaces import IIntIds

from getpaid.core import interfaces, item
from getpaid.variantsproduct.interfaces import IVariationItemFactory

class VariationItemFactory(object):
    """ Create shopping cart listings for variation items.

    NOTE: Normal LineItems are placed to cart by their Archetypes UID.
    We use value item stock keeping unit (SKU).
    I don't know whether this cause problems.

    See Products.PloneGetPaid.content module for inspiration.
    """

    zope.interface.implements(IVariationItemFactory)

    def __init__( self, cart, context):
        self.cart = cart
        self.context = context

    def create(self, sku, quantity = 1):
        """
        @return getpaid.core.item.PayableLineItem
        """

        nitem = item.PayableLineItem()
        nitem.item_id = self.context.UID() # archetypes uid

        # we use intids to reference content that we can dereference cleanly
        # without access to context.
        nitem.uid = component.getUtility( IIntIds ).register(self.context)


        def getUnicodeString( s ):
            """Try to convert a string to unicode from utf-8, as this is what Archetypes uses"""
            if type( s ) is type( u'' ):
                # this is already a unicode string, no need to convert it
                return s
            elif type( s ) is type( '' ):
                # this is a string, let's try to convert it to unicode
                try:
                    return s.decode( 'utf-8' )
                except UnicodeDecodeError, e:
                    # not utf-8... return as is and hope for the best
                    return s


        variation = self.context.getProductVariationBySKU(sku)

        # copy over information regarding the item
        nitem.name = getUnicodeString( variation.title )
        nitem.description = getUnicodeString( self.context.Description() )
        nitem.cost = variation.price

        nitem.product_code = variation.sku
        nitem.quantity = quantity

        # We place items to cart by their SKU,
        # *not* Archetypes ID
        self.cart[variation.sku] = nitem

        return nitem
