"""

    End-user view for variant product.

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

from productview import ProductView

class IVariantProductView(Interface):
    """
    Template exposes for variant product view.
    """

    def variations():
        """ List of Variation objects """


class VariantProductView(ProductView):
    """
    VariantsProduct browser view.

    Use productview.pt tempalte from the parent class.
    """
    implements(IVariantProductView)

    extra = ViewPageTemplateFile("variations.pt")


    def variations(self):
        return self.context.getProductVariations()
