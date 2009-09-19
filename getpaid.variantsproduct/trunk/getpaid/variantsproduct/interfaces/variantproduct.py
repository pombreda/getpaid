from zope import schema
from zope.interface import Interface

from zope.app.container.constraints import contains
from zope.app.container.constraints import containers

import zope.schema

from getpaid.variantsproduct import variantsproductMessageFactory as _

from multiimageproduct import IMultiImageProduct

class IVariantProduct(IMultiImageProduct):
    """ Marker interface used to identify VariantProduct content """

    def getVariations():
        """ Decode human-input of variations text to machine consumable variations objects.

        @return: List of IVariation objects
        """



class IVariation(Interface):
    """ Define information we need to know about one varation.
    """

    sku = zope.schema.TextLine(title=u"Id", description=u"Unique id for this variant used in internal data structures", required=True)

    title = zope.schema.TextLine(title=u"Title", description=u"Human readable name of this product", required=True)

    price = schema.Float(title = u"Price", description=u"Price of this variation", required=True)

