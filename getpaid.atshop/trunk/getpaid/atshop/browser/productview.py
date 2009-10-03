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
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from getpaid.atshop import atshopMessageFactory as _
from getpaid.atshop.price import get_price_text



class IProductView(Interface):
    """
    Product view methods and attributes exposed to templates
    """

    def image_browser():
        """
        @return: ProductImagePreviewsView instance for this product to render the product images.
        """

    def price():
        """
        @return: Human readable price or price summary
        """

    def extra():
        """
        @return: HTML code to be rendered before image browser or None
        """

class ProductView(BrowserView):
    """
    Abstract base class to render product views.
    """
    implements(IProductView)

    extra = None

    index = ViewPageTemplateFile("productview.pt")

    def price(self):
        return get_price_text(self.context)

    def image_browser(self):
        browser = self.context.unrestrictedTraverse("@@product_image_previews")
        return browser()

    def __call__(self):
        return self.index()


