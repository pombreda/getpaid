"""
Viewlet / Formlib / zc.table Based Shopping Cart

$Id$
"""

from Products.Five.viewlet import manager, viewlet
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from AccessControl import getSecurityManager

from getpaid.core import interfaces
from zope import component
from zope.formlib import form
from zc.table import column
from zc.table import table

class LineItemColumn( object ):
    
    def __init__(self, name):
        self.name = name
        
    def __call__( self, item, formatter ):
        value = getattr( item, self.name, '')
        if callable( value ):
            return value()
        return value

CartColumns = [
    column.SelectionColumn( lambda item: str((item.targetUID, item.relationship)), name="selection"),
    column.GetterColumn( title="Name", getter=LineItemColumn("name") ),
    column.GetterColumn( title="Price", getter=LineItemColumn("cost") ),    
    column.GetterColumn( title="Quantity", getter=LineItemColumn("quantity") )
]

SelectionColumn = CartColumns[0]

class ShoppingCartListing( viewlet.ViewletBase ):

    form_fields = form.Fields()
    template = ZopeTwoPageTemplateFile('templates/cart_listing.pt')

    def __init__( self, *args, **kw):
        super( ShoppingCartListing, self ).__init__( *args, **kw )
        self.cart = component.queryMultiAdapter(
            ( self.context, getSecurityManager().getUser() ),
            interfaces.IShoppingCart
            )
        
    def listing( self ):
        formatter = table.StandaloneFullFormatter( self.cart,
                                                   self.request,
                                                   self.cart.values(),
                                                   prefix="cart",
                                                   visible_column_names = [ c.name for c in CartColumns ],
                                                   columns = CartColumns )
        formatter.cssClasses['table'] = 'listing'
        return formatter()

    @form.action("Continue Shopping")
    def handle_continue_shopping( self, action, data ):
        pass
    
    @form.action("Remove")
    def handle_remove_item( self, action, data):
        selected = self._getNodes()
        for i in selected:
            del self.cart[i.name]
            
    @form.action("Checkout")
    def handle_checkout( self, action, data ):
        pass

