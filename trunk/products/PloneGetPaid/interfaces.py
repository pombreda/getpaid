"""
$Id$
"""

from zope import schema
from zope.interface import Interface

import getpaid.core.interfaces as igetpaid
import zope.viewlet.interfaces

class IGetPaidManageViewletManager( zope.viewlet.interfaces.IViewletManager ):
    """ viewlet manager for get paid management ui
    """

class IGetPaidCartViewletManager( zope.viewlet.interfaces.IViewletManager ):
    """ viewlet manager for get paid shopping cart ui
    """

class IBuyableMarker( Interface ):
    """ marker interface added to buyable content """

class IPremiumMarker( Interface ):
    """ marker interface added to premium content """

class IShippableMarker( Interface ):
    """ shippable interface added to shippable content """

class IDonatableMarker( Interface ):
    """ donate-able interface added to shippable content """

PayableMarkers = [ IBuyableMarker, IPremiumMarker, IShippableMarker, IDonatableMarker ]

PayableMarkerMap = dict(
     (
      (IBuyableMarker, igetpaid.IBuyableContent),
      (IPremiumMarker, igetpaid.IPremiumContent),
      (IShippableMarker, igetpaid.IShippableContent),
      (IDonatableMarker, igetpaid.IDonationContent),
    )
)    

class IGetPaidManagementOptions( igetpaid.IPersistentOptions ):

    payment_processor = schema.Choice( title = u"Payment Processor",
                                       source = "getpaid.payment_methods" )

    currency = schema.Choice( title = u"Currency",
    						  required = True,
					          source = "getpaid.currencies" )

    accepted_credit_cards = schema.List( title = u"Accepted Credit Cards",
     									 required = False,
    									 default = [],
    									 description = u"Credit cards accepted for payment",
                                         value_type = schema.Choice( title=u"accepted_credit_cards", source="getpaid.credit_cards" )
                                       )    
   
    shipping_method = schema.Choice( title = u"Shipping Method",
                                     required = True,
                                     source = "getpaid.shipping_methods" )
                                     
    weight_units = schema.Choice( title = u"Weight Units",
                                  required = True,
                                  source = "getpaid.weight_units" )

    tax_method = schema.Choice( title = u"Tax Method",
                                required = True,
                                source = "getpaid.tax_methods" )
           
    cart_session_timeout = schema.Int( title = u"Session Timeout",
    									 required = True,
    									 description = u"Shopping cart session timeout (in seconds)",
    									 default = 3600,
    								   )

    buyable_types = schema.List(
        title = u"Buyable Types",
        required = False,
        default = [],
        description = u"Buyable Content delivered through the web/virtually",
        value_type = schema.Choice( title=u"buyable_types", source="plone.content_types" )
        )
        
    shippable_types = schema.List(
        title = u"Shippable Product Types",
        required = False,
        default = [],
        description = u"Content Types that represent goods that can be purchased and shipped",        
        value_type = schema.Choice( title=u"shippable_types", source="plone.content_types" )
        )

    premium_types = schema.List(
        title = u"Premium Content Types",
        required = False,
        default = [],
        description = u"Content Types only available to premium memberships",
        value_type = schema.Choice( title=u"premium_types", source="plone.content_types" )
        )
                                     
    donate_types = schema.List(
        title = u"Donate Content Types",
        required = False,
        default = [],
        description = u"Content Types available for donation",
        value_type = schema.Choice( title=u"donate_types", source="plone.content_types" )
        )
        

class IGetPaidManagementIdentificationOptions( igetpaid.IPersistentOptions ):

    payment_processor = schema.Choice( title = u"Payment Processor",
                                       source = "getpaid.payment_methods" )
    
