"""
$Id$
"""

from zope.interface import Interface
from zope import schema
from zope.app.container.interfaces import IContainer
from ore.member.interfaces import IMemberSchema

#################################
# Stuff To Buy

class IPayable( Interface ):
    """
    An object which can be paid for. Payables are typically gotten via adapation between
    a context and the request, to allow for pricing / display customization on a user
    basis.
    """
    name = schema.TextLine( title=u"Product Name")
    description = schema.Text( title=u"Product Description")
    creation_user = schema.TextLine( title=u"Created By")
    sku = schema.TextLine( title=u"Product SKU/Code")
    price = schema.Float( title=u"Price")

class IDonation( IPayable ):
    """ Donation
    """

class ISubscription( IPayable ):
    """ Subscription
    """

class IBuyableContent( IPayable ):
    """ Purchasable Content Delivered Virtually
    """
    
class IPremiumContent( Interface ):
    """ Premium Content for Subscriptions
    """

class IPhysicalPayable( IPayable ):
    """
    """

class IShippableContent( IPayable ):
    """ Shippable Content
    """

    def getShipWeight( self ):
        """ Shipping Weight
        """

class IPayableAuditLog( Interface ):
    """ ordered container of changes, most recent first, hook on events.
    """
    #modification_date = 
    #changed_by =


#################################
# Stuff to Process Payments
class IPaymentProcessor( Interface ):
    """ A Payment Processor
    """ 

class IPaymentProcessorOptions( Interface ):
    """ Options for a Processor

    """
    
#################################
# Info needed for payment processing


    
#################################
# Shopping Cart Stuff

class IShoppingCartUtility( Interface ):

    def get( create=False ):
        """
        return the user's shopping cart or none if not found.
        if create is passed then create a new one if one isn't found
        """

class ILineItem( Interface ):
    """
    An Item in a Cart
    """
    item_id = schema.TextLine( title= u"Unique Item Id")
    name = schema.TextLine(title = u"Name")
    description = schema.TextLine( title = u"Description")
    cost = schema.Float( title=u"Cost")
    quantity = schema.Int( title = u"Quantity")
    
class IPayableLineItem( ILineItem ):
    """
    A line item linked to a payable
    """

    def resolve( context ):
        """ return the payable object
        """

class IGiftCertificate( ILineItem ):
    """ A Gift Certificate
    """

class ILineItemContainer( IContainer ):
    """ A container for line items
    """

class IShoppingCart( ILineItemContainer ):
    """ A Shopping Cart 
    """

#################################
# Shipping Methods

class IShippingMethod( Interface ):
    pass

#################################
# Payment Information Details

class IAddress( Interface ):
    """ a physical address
    """
    first_line = schema.TextLine( title = u"First Line")
    second_line = schema.TextLine( title = u"Second Line" )
    state = schema.TextLine( title = u"State ")
    city = schema.TextLine( title = u"City" )
    country = schema.TextLine( title = u"Country")
    postal_code = schema.TextLine( title = u"Zip Code")

class IShippingAddress( IMemberSchema ):
    """ where to send goods
    """
    ship_first_line = schema.TextLine( title = u"First Line")
    ship_second_line = schema.TextLine( title = u"Second Line" )
    ship_state = schema.TextLine( title = u"State ")
    ship_city = schema.TextLine( title = u"City" )
    ship_country = schema.TextLine( title = u"Country")
    ship_postal_code = schema.TextLine( title = u"Zip Code")

class IBillingAddress( IMemberSchema ):
    """ where to bill 
    """
    bill_first_line = schema.TextLine( title = u"First Line")
    bill_second_line = schema.TextLine( title = u"Second Line" )
    bill_state = schema.TextLine( title = u"State ")
    bill_city = schema.TextLine( title = u"City" )
    bill_country = schema.TextLine( title = u"Country")
    bill_postal_code = schema.TextLine( title = u"Zip Code")    

class IUserPaymentInformation( Interface ):
    """ A User's payment information to be optionally collected by the
    payment processor view.
    """

    name_on_card = schema.TextLine( title=u"Card Holder Name")
    phone_number = schema.TextLine( title=u"Phone Number")    
    # NOT STORED PERSISTENTLY
    credit_card_type = schema.Choice( title = u"Credit Card Type",
                                      values = ( u"Visa",
                                                 u"MasterCard",
                                                 u"Discover",
                                                 u"American Express" ) )
    
    credit_card = schema.TextLine( title = u"Credit Card Number")
    cc_expiration = schema.TextLine( title = u"Credit Card Expiration Date")
    cc_cvc = schema.TextLine(title = u"Credit Card Verfication Number")


    
class IPaymentTransaction( ILineItemContainer ):
    """  A Payment that's been applied
    """

    status = schema.Choice( title = u"Payment Status",
                            values = ( u"Accepted",
                                       u"Declined",
                                       u"Refunded" ) )
    
class IPersistentOptions( Interface ):
    """ interface
    """
