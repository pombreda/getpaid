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

from getpaid.atshop.price import get_price_text

class IProductView(Interface):
    """
    Product view methods and attributes exposed to templates
    """

    def image_browser():
        """
        @return: ProductImagePreviewsView instance for this product.
        """

    def price():
        """
        @return: Human readable price or price summary
        """

class ProductView(BrowserView):
    """
    Abstract base class to render product views.
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

    def price(self):
        return get_price_text(self.context)

    def image_browser(self):
        browser = self.unrestrictedTraverse("@@productimagepreviews_view")
        return browser


