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

class IOrdersAdminManager( zope.viewlet.interfaces.IViewletManager ):
    """ viewlet manager for collections of orders admin management
    """

class IAdminOrderManager( zope.viewlet.interfaces.IViewletManager ):
    """ viewlet manager for a single order
    """ 

class IGetPaidContentViewletManager( zope.viewlet.interfaces.IViewletManager ):
    """ viewlet manager for content that is marked with one of the getpaid Marker interfaces
    """

class IPayableMarker( Interface ):
    """ marker interface added to any payable content """

class IBuyableMarker( IPayableMarker ):
    """ marker interface added to buyable content """

class IPremiumMarker( IPayableMarker ):
    """ marker interface added to premium content """

class IShippableMarker( IPayableMarker ):
    """ shippable interface added to shippable content """

class IDonatableMarker( IPayableMarker ):
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

class IGetPaidManagementIdentificationOptions( igetpaid.IPersistentOptions ):

    store_name = schema.TextLine( title = u"Store/Organization Name",
                                  required = True,
                                  default = u""
                                )

    contact_name = schema.TextLine( title = u"Contact Name",
                                  required = False,
                                  default = u""
                                )

    contact_email = schema.TextLine( title = u"Contact Email",
                                  required = False,
                                  default = u""
                                )
                                
    contact_company = schema.TextLine( title = u"Contact Company",
                              required = False,
                              default = u""
                            )

    contact_address = schema.TextLine( title = u"Contact Address",
                                       required = False,
                                       default = u""
                                     )
                                
    contact_address2 = schema.TextLine( title = u"Contact Address2",
                                        required = False,
                                        default = u""
                                      )

    contact_city = schema.TextLine( title = u"Contact City",
                                    required = False,
                                    default = u""
                                  )
                                
    contact_state = schema.TextLine( title = u"Contact State/Province",
                                     required = False,
                                     default = u""
                                   )

    contact_postalcode = schema.TextLine( title = u"Contact Zip/Postal Code",
                                          required = False,
                                          default = u""
                                        )

    contact_country = schema.TextLine( title = u"Contact Country",
                                       required = False,
                                       default = u""
                                     )  

    contact_phone = schema.TextLine( title = u"Contact Phone",
                                     required = False,
                                     default = u""
                                   )
                                
    contact_fax = schema.TextLine( title = u"Contact Fax",
                                   required = False,
                                   default = u""
                                 )
# Configure
class IGetPaidManagementContentTypes( igetpaid.IPersistentOptions ):

    buyable_types = schema.List(
        title = u"Buyable Types",
        required = False,
        default = [],
        description = u"Buyable Content delivered through the web/virtually",
        value_type = schema.Choice( title=u"buyable_types", source="plone.content_types" )
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

    shippable_types = schema.List(
        title = u"Shippable Product Types",
        required = False,
        default = [],
        description = u"Content Types that represent goods that can be purchased and shipped",        
        value_type = schema.Choice( title=u"shippable_types", source="plone.content_types" )
        )

class IGetPaidManagementShippingOptions( igetpaid.IPersistentOptions ):
    """
    """
    shipping_method = schema.Choice( title = u"Shipping Method",
                                     required = True,
                                     source = "getpaid.shipping_methods" )

class IGetPaidManagementPaymentOptions( igetpaid.IPersistentOptions ):
    """
    """
    payment_processor = schema.Choice( title = u"Payment Processor",
                                       source = "getpaid.payment_methods" )

    accepted_credit_cards = schema.List( title = u"Accepted Credit Cards",
                                         required = False,
                                         default = [],
                                         description = u"Credit cards accepted for payment",
                                         value_type = schema.Choice( title=u"accepted_credit_cards", source="getpaid.credit_cards" )
                                       )    

# Order Management
class IGetPaidManagementCustomerInformation( igetpaid.IPersistentOptions ):
    """
    """
    
class IGetPaidManagementOrderInformation( igetpaid.IPersistentOptions ):
    """
    """

class IGetPaidManagementPaymentProcessing( igetpaid.IPersistentOptions ):
    """
    """

class IGetPaidManagementWeightUnits( igetpaid.IPersistentOptions ):
    """
    """
    weight_units = schema.Choice( title = u"Weight Units",
                                  required = True,
                                  source = "getpaid.weight_units" )
                                  
class IGetPaidManagementSessionTimeout( igetpaid.IPersistentOptions ):
    """
    """
    cart_session_timeout = schema.Int( title = u"Session Timeout",
                                     required = True,
                                     description = u"Shopping cart session timeout (in seconds)",
                                     default = 3600,
                                   )

class IGetPaidManagementSalesTaxOptions( igetpaid.IPersistentOptions ):
    """
    """
    tax_method = schema.Choice( title = u"Tax Method",
                                required = True,
                                source = "getpaid.tax_methods" )

# Currency    
class IGetPaidManagementCurrencyOptions( igetpaid.IPersistentOptions ):
    """
    """
    currency_symbol = schema.TextLine( title = u"Currency Symbol",
                                   required = True,
                                   default = u"$"
                                 )
                                 
    positive_currency_format = schema.TextLine( title = u"Positive Currency Format",
                                   required = False,
                                   default = u""
                                 )                                 
                                   
    negative_currency_format = schema.TextLine( title = u"Negative Currency Format",
                                   required = False,
                                   default = u""
                                 )   
                                   
    digit_grouping_symbol = schema.TextLine( title = u"Digit Grouping Symbol",
                                   required = False,
                                   default = u""
                                 )   
                                   
    digit_grouping_symbol = schema.TextLine( title = u"Number of Digits in Group",
                                   required = False,
                                   default = u""
                                 )   
                                   
    digit_grouping_symbol = schema.TextLine( title = u"Decimal Symbol",
                                   required = False,
                                   default = u""
                                 )   
                                   
    digits_after_decimal = schema.TextLine( title = u"Number of Digits After Decimal",
                                   required = False,
                                   default = u""
                                 )   
                                   
    us_currency_formatting = schema.TextLine( title = u"US Currency Formatting",
                                   required = False,
                                   default = u""
                                 ) 

# Emails
class IGetPaidManagementEmailOptions( igetpaid.IPersistentOptions ):
    """
    """


class IGetPaidManagementMerchantNotificationOptions( igetpaid.IPersistentOptions ):     
    """
    """
    merchant_email_notification = schema.Choice( title = u"Merchant Email Notifications",
                                  source = "getpaid.merchant_notification_choices" )
    
    


class IGetPaidManagementCustomerNotificationOptions( igetpaid.IPersistentOptions ):     
    """
    """    
    merchant_email_notification = schema.Choice( title = u"Customer Email Notifications",
                                                 source = "getpaid.customer_notification_choices" )

# Customize Header/Footer
class IGetPaidManagementLegalDisclaimerOptions( igetpaid.IPersistentOptions ):
    """
    """
    disclaimer = schema.Text( title = u"Disclaimer",
                          required = False,
                        )
                                 
    privacy_policy = schema.Text( title = u"Privacy Policy",
                          required = False,
                        )                                 

class IGetPaidManagementOptions( IGetPaidManagementIdentificationOptions,
                                 IGetPaidManagementContentTypes,
                                 IGetPaidManagementShippingOptions,
                                 IGetPaidManagementPaymentOptions,
                                 IGetPaidManagementCustomerInformation,
                                 IGetPaidManagementOrderInformation,
                                 IGetPaidManagementPaymentProcessing,
                                 IGetPaidManagementWeightUnits,
                                 IGetPaidManagementSessionTimeout,
                                 IGetPaidManagementSalesTaxOptions,                                 
                                 IGetPaidManagementCurrencyOptions,
                                 IGetPaidManagementEmailOptions,
                                 IGetPaidManagementMerchantNotificationOptions,
                                 IGetPaidManagementCustomerNotificationOptions,
                                 IGetPaidManagementLegalDisclaimerOptions
                                ):
    """ One-stop config variable access
    """
