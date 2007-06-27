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

    currency = schema.Choice(
        title = u"Currency",
        values = ( u"US", ) )


    shipping_method = schema.Choice( title = u"Shipping Method",
                                     required = False,
                                     source = "getpaid.shipping_methods" )

    tax_method = schema.Choice( title = u"Tax Method",
                                required = False,
                                source = "getpaid.tax_methods" )
    
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
        description = u"Content Types available for Donation",
        value_type = schema.Choice( title=u"donate_types", source="plone.content_types" )
        )
        

    
