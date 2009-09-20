from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from getpaid.variantsproduct import variantsproductMessageFactory as _

from getpaid.variantsproduct.interfaces import IProductImageProvider

class IProductListingView(Interface):
    """
    View methods exposed to the template.
    """


class ProductListingView(BrowserView):
    """
    Summary view of the products in the current folder.
    """
    implements(IProductListingView)

    def __init__(self, context, request):
        self.context = context
        self.request = request


    def has_image(self, catalog_brain):
        """ Check whether the iterated item is product like and supports multiple images

        @return: True or False
        """

        # TODO: I don't think metadata supports interface checks...
        if catalog_brain["portal_type"] in ["MultiImageProduct", "VariantProduct"]:
            return True

        return False

    def get_image_tag(self, item):

        object = item.getObject()

        if IProductImageProvider.providedBy(object):
            image = object.getMainImage()
            return image.tag()

        return None


