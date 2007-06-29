"""
"""

from zope import component
from zope.app.publisher.browser import BrowserView
from getpaid.core.interfaces import IPaymentProcessor
from getpaid.core.interfaces import IShoppingCartUtility

class GoogleCheckoutButton( BrowserView ):

    def __call__( self ):
        processor = component.getAdapter( self.context,
                                          IPaymentProcessor,
                                          "Google Checkout" )
        cart_manager = component.getUtility( IShoppingCartUtility )
        cart = cart = cart_manager.get( self.context )
        return processor.cart_post_button( cart )
