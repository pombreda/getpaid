"""
Paid Content Support

Premium Content can be done either for a particular content type or for any individual piece
of content.

BuyableContent uses Content Flavors, to apply an archetypes schema and a zope 3 interface
to content. The archetypes schema allows to use archetype widgets to create a user interface
for the content's commerce-related information. The applied zope3 interface allows us to
use an adapter to add the component architecture to create views and adapters for the content.
BuyableContent is delivered virtually, such as electronic PDF or simply viewing the content on
the site.

ShippableContent describes a physical, tangible item that must be shipped to an address. 
Gift cards, products like T-Shirts, or paper-based content that goes into an envelope are 
all examples of ShippableContent. This allows a content object to be added to a shopping cart, 
shipped, etc.

PremiumContent implies that the consumer of the content has a local role of Premium Member for the
content.  This role is granted if the consumer has a certain subscription level (set in the product
configuration.) *** this section needs to be explained better ***

To allow for per instance application of content types, we provide an action for archetypes
under the content actions drop down to apply a (ala iterate), the condition for this action
invokes a premium content control view which in turn checks the control panel configuration
for this content, by interface or content type.

content security, we want to set local roles for users who buy content, we do this via

content view snippets.. we still need to figure out if we can override the default view
of a content object via applying an interface to it.

$Id$
"""
from Products.Archetypes import atapi

from zope import interface
from getpaid.core.interfaces import IBuyableContent, IShippableContent, IPremiumContent
from getpaid.core import cart
from getpaid.core import options

class ContentLineItem( cart.PayableLineItem ):
    """ A line item with a reference to an archetype content that can be placed in a cart
    """
    reference_id = None
    
    def resolve( self, context ):
        resolve = getToolByName( context, 'reference_catalog').lookupObject
        return resolve( self.reference_id )

def ContentLineItemFactory( cart, content ):
    item = cart.PayableLineItem()
    item.name = "%s : %s"%( content.Type(), content.Title())
    item.cost = content.getBuyableContentPrice()
    item.quantity = 1
    item.reference_id = content.UID()
    return item

#################################
# Buyable Content

"""
when buyable content is deleted, we still want to be able to keep a reference to it
for those who have paid, or at least replace any shopping cart / transaction references
with information.
"""

BuyableContentStorage = options.PersistentOptions.wire( "BuyableContentStorage", "getpaid.content.buyable", IBuyableContent )

class BuyableContentAdapter( BuyableContentStorage ):
    """
    Default Adapter between Content and IBuyable. This implementation stores attributes
    of a buyable in an annotation adapter
    """
    interface.implements( IBuyableContent )
    
    def __init__( self, context, request ):
        self.context = context
        self.request = request
    

#################################
# Shippable Content
"""
shippable deletions need to track orders not shipped 
"""

ShippableContentStorage = options.PersistentOptions.wire( "ShippableContentStorage", "getpaid.content.shippable", IShippableContent )

class ShippableContentAdapter( object ):

    interface.implements( IShippableContent )
    
    def __init__( self, context, request ):
        self.context = context
        self.request = request

#################################
# Premium Content    

PremiumContentStorage = options.PersistentOptions.wire( "ShippableContentStorage", "getpaid.content.buyable", IPremiumContent )

class PremiumContentAdapter( object ):

    interface.implements( IPremiumContent )
    
    def __init__( self, context, request ):
        self.context = context
        self.request = request

        
    


    
    

