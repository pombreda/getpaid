"""
Viewlet / Formlib / zc.table Based Shopping Cart

$Id$
"""

from AccessControl import getSecurityManager

from Products.Five.viewlet import viewlet
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.PloneGetPaid.interfaces import PayableMarkers, PayableMarkerMap
from Products.CMFCore.utils import getToolByName

from getpaid.core import interfaces, item as litem
from zope import component
from zope.formlib import form
from zc.table import column
from zc.table import table

from ore.viewlet.container import ContainerViewlet
from ore.viewlet.core import FormViewlet

from viewlet import ShoppingCartManager

class ShoppingCart( BrowserView ):

    _cart = None

    def __call__( self ):
        self.manager = ShoppingCartManager( self.context, self.request, self )
        self.manager.update()
        return super( ShoppingCart, self ).__call__()
    
    def getCart( self ):
        if self._cart is not None:
            return self._cart
        cart_manager = component.getUtility( interfaces.IShoppingCartUtility )
        self._cart = cart = cart_manager.get( self.context, create=True )
        return cart
    
    cart = property( getCart )

    def isContextAddable( self ):
        addable = filter( lambda x, s=self.context: x.providedBy(s), PayableMarkers )
        return not not addable 
    
    def size( self ):
        if self.cart is None:
            return 0
        return len( self.cart )

class ShoppingCartAddItem( ShoppingCart ):
    """
    item we're adding is the context 
    """
    
    def __call__( self ):
        if self.request.has_key('add_item'):
            self.addToCart()
        return super( ShoppingCartAddItem, self ).__call__()
    
    def addToCart( self ):
        item_id = self.context.UID()
        if item_id in self.cart:
            self.cart[ item_id ].quantity += 1
            return 
        found = False
        for marker, iface in PayableMarkerMap.items():
            if marker.providedBy( self.context ):
                found = True
                break

        if not found:
            raise RuntimeError("Invalid Context For Cart Add")
        
        payable = iface( self.context )
        
        item = litem.PayableLineItem()
        item.item_id = self.context.UID()
        item.name = self.context.Title()
        item.description = self.context.Description()
        item.cost = payable.price
        item.quantity = 1
        self.cart[ item.item_id ] = item
        self.cart.last_item = item.item_id
        
        
class LineItemColumn( object ):
    
    def __init__(self, name):
        self.name = name
        
    def __call__( self, item, formatter ):
        value = getattr( item, self.name, '')
        if callable( value ):
            return value()
        return value

def lineItemURL( item, formatter ):
    return '<a href="reference_catalog/lookupObject?uuid=%s">%s</a>'  % (item.item_id, item.name)

def lineItemTotal( item, formatter ):
    return "%0.2f" % (item.quantity * item.cost)

class ShoppingCartListing( ContainerViewlet ):

    columns = [
        column.SelectionColumn( lambda item: item.item_id, name="selection"),
        column.GetterColumn( title="Quantity", getter=LineItemColumn("quantity") ),
        column.GetterColumn( title="Name", getter=lineItemURL ),
        column.GetterColumn( title="Price", getter=LineItemColumn("cost") ),
        column.GetterColumn( title="Total", getter=lineItemTotal ),
       ]
    
    selection_column = columns[0]
    template = ZopeTwoPageTemplateFile('templates/cart-listing.pt')
    
    def __init__( self, *args, **kw):
        super( ShoppingCartListing, self ).__init__( *args, **kw )

    def getContainerContext( self ):
        return self.__parent__.cart
        
    def isOrdered( self, *args ):
        # shopping cart should not be ordered, so override this with False
        return False
    
class ShoppingCartActions( FormViewlet ):

    template = ZopeTwoPageTemplateFile('templates/cart-actions.pt')

    def render( self ):
        return self.template()

    def isLoggedIn( self, *args ):
        return getSecurityManager().getUser().getId() is not None
    
    def isAnonymous( self, *args ):
        return getSecurityManager().getUser().getId() is None


    @form.action("Continue Shopping")
    def handle_continue_shopping( self, action, data ):
        # redirect the user to the last thing they were viewing
        last_item = self.__parent__.cart.last_item
        payable = getToolByName( self.context, 'reference_catalog').lookupObject( last_item )
        return self.request.RESPONSE.redirect(payable.absolute_url()+'/view')

    @form.action("Checkout", condition="isLoggedIn", name="AuthCheckout")
    def handle_checkout( self, action, data ):
        # go to order-create
        # force ssl? redirect host? options
        portal = getToolByName( self.context, 'portal_url').getPortalObject()
        url = portal.absolute_url() + '/@@getpaid-checkout'
        return self.request.RESPONSE.redirect( url )

    @form.action("Checkout", condition="isAnonymous", name="AnonCheckout")
    def handle_login_checkout( self, action, data ):
        # go to sign in with redirect url to checkout
        portal = getToolByName( self.context, 'portal_url').getPortalObject()
        url = portal.absolute_url()
        url = "%s/%s?%s=%s/%s"%( url,
                                 'login_form',
                                 'came_from',
                                 url,
                                 '@@getpaid-checkout' )
        return self.request.RESPONSE.redirect( url )         


