from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from getpaid.atshop import atshopMessageFactory as _

from productview import ProductView

class IMultiImageProductView(Interface):
    """
    MultiImageProduct view interface
    """

class MultiImageProductView(ProductView):
    """
    Render product with multiple images and one price.
    """
    implements(IMultiImageProductView)

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

