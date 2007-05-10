"""
$Id$
"""

from zope import schema
from zope.interface import Interface

import getpaid.interfaces
import zope.viewlet.interfaces

class IGetPaidManageViewletManager( zope.viewlet.interfaces.IViewletManager ):
    """ viewlet manager for get paid management ui
    """

class IGetPaidCartViewletManager( zope.viewlet.interfaces.IViewletManager ):
    """ viewlet manager for get paid shopping cart ui
    """

class IGetPaidManagementOptions( getpaid.interfaces.IPersistentOptions ):

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
        description = u"Buyable Content delivered through the web/virtually",
        value_type = schema.Choice( title=u"buyable_types", source="plone.content_types" )
        )
        
    shippable_types = schema.List(
        title = u"Shippable Product Types",
        required = False,
        description = u"Content Types that represent goods that can be purchased and shipped",        
        value_type = schema.Choice( title=u"shippable_types", source="plone.content_types" )
        )
                                     
        

    
