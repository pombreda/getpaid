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

from getpaid.atshop import atshopMessageFactory as _

from productview import ProductView

class IVariantsProductView(Interface):
    """
    Template exposes for variant product view.
    """

    def variations():
        """ List of Variation objects """


class VariantsProductView(ProductView):
    """
    VariantsProduct browser view
    """
    implements(IVariantsProductView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def variations(self):
        return self.context.getProductVariations()
