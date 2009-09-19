"""

    Interface definitions for products with variations.

"""

from zope import schema
from zope.interface import Interface

from zope.app.container.constraints import contains
from zope.app.container.constraints import containers

import zope.schema

from getpaid.variantsproduct import variantsproductMessageFactory as _

from multiimageproduct import IMultiImageProduct

__author__ = "Mikko Ohtamaa <mikko.ohtamaa@twinapex.com> http://www.twinapex.com"
__docformat__ = "epytext"
__license__ = "GPL"
__copyright__ = "2009 Twinapex Research"

class IVariantBuyMarker(Interface):
    """ Marker interface controlling whether variant specific buying portlet is shown next to the content """

class IVariantProduct(IMultiImageProduct):
    """ Marker interface used to identify VariantProduct content """

    def getProductVariations():
        """ Get variations of this product.

        @return: List of IVariation objects
        """

    def getProductVariationBySKU(sku):
        """


        """
class IVariationItemFactory(Interface):
    """ Create shopping cart items from IVariantProduct instance.
    """

    def createCartItem(context, variationId):
        """
        @return: IShippableLineItem instance
        """

class IVariation(Interface):
    """ Define information we need to know about one varation.
    """

    sku = zope.schema.TextLine(title=u"Id", description=u"Unique id for this variant used in internal data structures", required=True)

    title = zope.schema.TextLine(title=u"Title", description=u"Human readable name of this product", required=True)

    price = schema.Float(title = u"Price", description=u"Price of this variation", required=True)

