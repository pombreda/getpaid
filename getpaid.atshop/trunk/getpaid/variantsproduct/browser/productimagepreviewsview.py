from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from getpaid.variantsproduct import variantsproductMessageFactory as _

from getpaid.variantsproduct.interfaces import IProductImageProvider

class IProductImagePreviewsView(Interface):
    """
    ProductImagePreviews view interface
    """

    def images():
        """ @return: List of product images as tuples:

                * Name

                * Image SRC URL

                * Link target URL

        """


class ProductImagePreviewsView(BrowserView):
    """ Render all images associated with a buyable product.

    """
    implements(IProductImagePreviewsView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def images(self):
        """
        """
        return self._images

    def __call__(self):
        self.image_provider = IProductImageProvider(self.context)
        self._images = self.image_provider.getImages()

        return self.index()