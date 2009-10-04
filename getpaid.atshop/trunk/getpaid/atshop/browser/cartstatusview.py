# -*- coding: utf-8 -*-
"""

    Render shopping cart status as one line.
    
    Useful for embedding this into viewlets etc.

"""

__author__ = "Mikko Ohtamaa <mikko.ohtamaa@twinapex.com> http://www.twinapex.com"
__docformat__ = "epytext"
__license__ = "GPL"
__copyright__ = "2009 Twinapex Research"


from zope.interface import implements, Interface
from zope import schema

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from getpaid.atshop import atshopMessageFactory as _

from Products.PloneGetPaid.browser.cart import ShoppingCart

from getpaid.atshop.currency import format_currency 
import getpaid.core.interfaces

class ICartStatusView(Interface):
    """
    CartStatus view interface
    """
    
    def empty():
        pass

    def summary_text():
        pass
    
    
class CartStatusView(ShoppingCart):
    """
    CartStatus browser view
    """
    implements(ICartStatusView)

    def summary_text(self):
        
        if self.empty():
            return _(u"Your shopping cart is empty")
        else:    
            totals = getpaid.core.interfaces.ILineContainerTotals(self.cart)            
            items = self.size()
            cost_text = format_currency(totals.getTotalPrice()) 
            return _(u"You have %d items worth of %s" % (items, cost_text))

    def empty(self):
        return self.size() == 0
        
        