"""
$Id$
"""

from Products.Five.browser import BrowserView
from Products.PloneGetPaid import interfaces
from getpaid.core.interfaces import IShoppingCartUtility
from zope import component

class ShoppingCart( BrowserView ):

    _cart = None
    
    __allow_access_to_unprotected_subobjects__ = 1
    
    def getCart( self ):
        if self._cart is not None:
            return self._cart
        cart_manager = component.getUtility( IShoppingCartUtility )
        self._cart = cart = cart_manager.get( self.context, create=False )
        return cart
    
    cart = property( getCart )

    def isContextAddable( self ):
        addable = filter( lambda x, s=self.context: x.providedBy(s), interfaces.PayableMarkers )
        return not not addable 
    
    def size( self ):
        if self.cart is None:
            return 0
        return len( self.cart )
    
