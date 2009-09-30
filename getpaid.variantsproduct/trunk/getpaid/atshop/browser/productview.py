"""

   Base classes for end user visible product screens.

"""

__author__ = "Mikko Ohtamaa <mikko.ohtamaa@twinapex.com> http://www.twinapex.com"
__docformat__ = "epytext"
__license__ = "GPL"
__copyright__ = "2009 Twinapex Research"

from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from getpaid.atshop import atshopMessageFactory as _


class IProductView(Interface):
    """
    Product view methods and attributes exposed to templates
    """

    def image_browser():
        """
        @return: ProductImagePreviewsView instance for this product.
        """

class ProductView(BrowserView):
    """
    Product browser view
    """
    implements(IProductView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()


    def image_browser(self):
        browser = self.unrestrictedTraverse("@@productimagepreviews_view")
        return browser


