from zope import schema
from zope.interface import Interface

from zope.app.container.constraints import contains
from zope.app.container.constraints import containers

from getpaid.atshop import atshopMessageFactory as _

class IMultiImageProduct(Interface):
    """Buyable product with multiple images"""


class IProductImageProvider(Interface):

    def getImages():
        """ Get Images associated with the product.

        @return: iterable of Image objects
        """

    def getMainImage():
       """ Get the preferred image used in the folder listings.

        @return: Image object or None
        """

