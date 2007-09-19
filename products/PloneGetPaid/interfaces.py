"""
$Id$
"""

from zope import schema
from zope.interface import Interface
from zope.schema import Iterable
from zope.app.event.interfaces import IObjectEvent
from getpaid.core.fields import PhoneNumber

import getpaid.core.interfaces as igetpaid
import zope.viewlet.interfaces

from zope.i18nmessageid import MessageFactory
_ = MessageFactory('plonegetpaid')

class IBeforeCheckoutEvent( IObjectEvent ):
    """
    an event fired before the checkout process begins
    """

class IGetPaidManageViewletManager( zope.viewlet.interfaces.IViewletManager ):
    """ viewlet manager for get paid management ui
    """

class IGetPaidCartViewletManager( zope.viewlet.interfaces.IViewletManager ):
    """ viewlet manager for get paid shopping cart ui
    """

class IGetPaidOrderHistoryViewletManager( zope.viewlet.interfaces.IViewletManager ):
    """ viewlet manager for get paid order history ui
    """

class IOrdersAdminManager( zope.viewlet.interfaces.IViewletManager ):
    """ viewlet manager for collections of orders admin management
    """

class IAdminOrderManager( zope.viewlet.interfaces.IViewletManager ):
    """ viewlet manager for admin of a single order
    """ 

class IOrderDetailsManager( zope.viewlet.interfaces.IViewletManager ):
    """ viewlet manager for a single order
    """ 

class IGetPaidContentViewletManager( zope.viewlet.interfaces.IViewletManager ):
    """ viewlet manager for content that is marked with one of the getpaid Marker interfaces
    """

class IOrderHistoryManager( zope.viewlet.interfaces.IViewletManager ):
    """ viewlet manager for user order history
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


class IStoreMember( Interface ):
    """ marker interface so we can adapt to members """
    
class INotificationMailTemplate( Interface ):

    def __call__( from_email, to_email, store_name, store_settings, store_url, order ):
        """
        return a rendered template suitable for passing to a mailhost.send
        """
        

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

    store_name = schema.TextLine( title = _(u"Store/Organization Name"),
                                  required = True,
                                  default = u""
                                )

    contact_name = schema.TextLine( title = _(u"Contact Name"),
                                  required = False,
                                  default = u""
                                )

    contact_email = schema.TextLine( title = _(u"Contact Email"),
                                  required = False,
                                  default = u""
                                )
                                
    contact_company = schema.TextLine( title = _(u"Contact Company"),
                              required = False,
                              default = u""
                            )

    contact_address = schema.TextLine( title = _(u"Contact Address"),
                                       required = False,
                                       default = u""
                                     )
                                
    contact_address2 = schema.TextLine( title = _(u"Contact Address2"),
                                        required = False,
                                        default = u""
                                      )

    contact_city = schema.TextLine( title = _(u"Contact City"),
                                    required = False,
                                    default = u""
                                  )

    contact_country = schema.Choice( title = _(u"Contact Country"),
                                     required = False,
                                     vocabulary = "getpaid.countries"
                                   )

    contact_state = schema.Choice( title = _(u"Contact State/Province"),
                                   required = False,
                                   vocabulary = "getpaid.states"
                                 )

    contact_postalcode = schema.TextLine( title = _(u"Contact Zip/Postal Code"),
                                          required = False,
                                          default = u""
                                        )

    contact_phone = PhoneNumber( title = _(u"Contact Phone"),
                                 description = _(u"Only digits allowed"),
                                     required = False,
                                     default = u""
                                   )

    contact_fax = schema.TextLine( title = _(u"Contact Fax"),
                                   required = False,
                                   default = u""
                                 )
# Configure
class IGetPaidManagementContentTypes( igetpaid.IPersistentOptions ):

    buyable_types = schema.List(
        title = _(u"Buyable Types"),
        required = False,
        default = [],
        description = _(u"Buyable Content delivered through the web/virtually"),
        value_type = schema.Choice( title=u"buyable_types", source="plone.content_types" )
        )
        
    premium_types = schema.List(
        title = _(u"Premium Content Types"),
        required = False,
        default = [],
        description = _(u"Content Types only available to premium memberships"),
        value_type = schema.Choice( title=u"premium_types", source="plone.content_types" )
        )
                                     
    donate_types = schema.List(
        title = _(u"Donatable Content Types"),
        required = False,
        default = [],
        description = _(u"Content Types available for donation"),
        value_type = schema.Choice( title=u"donate_types", source="plone.content_types" )
        )

    shippable_types = schema.List(
        title = _(u"Shippable Product Types"),
        required = False,
        default = [],
        description = _(u"Content Types that represent goods that can be purchased and shipped"),        
        value_type = schema.Choice( title=u"shippable_types", source="plone.content_types" )
        )

class IGetPaidManagementShippingOptions( igetpaid.IPersistentOptions ):
    """
    """
    shipping_method = schema.Choice( title = _(u"Shipping Method"),
                                     required = True,
                                     source = "getpaid.shipping_methods" )

class IGetPaidManagementPaymentOptions( igetpaid.IPersistentOptions ):
    """
    """
    payment_processor = schema.Choice( title = _(u"Payment Processor"),
                                       source = "getpaid.payment_methods" )
                                       
    allow_anonymous_checkout = schema.Bool( title=_(u"Allow Anonymous Checkout"), default=False)
                                    

##     accepted_credit_cards = schema.List( title = _(u"Accepted Credit Cards"),
##                                          required = False,
##                                          default = [],
##                                          description = _(u"Credit cards accepted for payment"),
##                                          value_type = schema.Choice( title=u"accepted_credit_cards", source="getpaid.credit_cards" )
##                                        )    

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
    weight_units = schema.Choice( title = _(u"Weight Units"),
                                  required = True,
                                  source = "getpaid.weight_units" )
                                  
class IGetPaidManagementSessionTimeout( igetpaid.IPersistentOptions ):
    """
    """
    cart_session_timeout = schema.Int( title = _(u"Session Timeout"),
                                     required = True,
                                     description = _(u"Shopping cart session timeout (in seconds)"),
                                     default = 3600,
                                   )

class IGetPaidManagementSalesTaxOptions( igetpaid.IPersistentOptions ):
    """
    """
    tax_method = schema.Choice( title = _(u"Tax Method"),
                                required = True,
                                source = "getpaid.tax_methods" )

# Currency    
class IGetPaidManagementCurrencyOptions( igetpaid.IPersistentOptions ):
    """
    """
    currency_symbol = schema.TextLine( title = _(u"Currency Symbol"),
                                   required = True,
                                   default = u"$"
                                 )
                                 
    positive_currency_format = schema.TextLine( title = _(u"Positive Currency Format"),
                                   required = False,
                                   default = u""
                                 )                                 
                                   
    negative_currency_format = schema.TextLine( title = _(u"Negative Currency Format"),
                                   required = False,
                                   default = u""
                                 )   
                                   
    digit_grouping_symbol = schema.TextLine( title = _(u"Digit Grouping Symbol"),
                                   required = False,
                                   default = u""
                                 )   
                                   
    digit_grouping_symbol = schema.TextLine( title = _(u"Number of Digits in Group"),
                                   required = False,
                                   default = u""
                                 )   
                                   
    digit_grouping_symbol = schema.TextLine( title = _(u"Decimal Symbol"),
                                   required = False,
                                   default = u""
                                 )   
                                   
    digits_after_decimal = schema.TextLine( title = _(u"Number of Digits After Decimal"),
                                   required = False,
                                   default = u""
                                 )   
                                   
    us_currency_formatting = schema.TextLine( title = _(u"US Currency Formatting"),
                                   required = False,
                                   default = u""
                                 ) 

# Emails
class IGetPaidManagementEmailOptions( igetpaid.IPersistentOptions ):
    """ Email Notification Options
    """
    merchant_email_notification = schema.Choice( title = _(u"Merchant Email Notifications"),
                                                 default = u'notification',
                                                 source = "getpaid.merchant_notification_choices" )

    customer_email_notification = schema.Choice( title = _(u"Customer Email Notifications"),
                                                 default = u'notification',
                                                 source = "getpaid.customer_notification_choices" )

# Customize Header/Footer
class IGetPaidManagementLegalDisclaimerOptions( igetpaid.IPersistentOptions ):
    """
    """
    disclaimer = schema.Text( title = _(u"Disclaimer"),
                              required = False, )
                        
                                 
    privacy_policy = schema.Text( title = _(u"Privacy Policy"),
                                  required = False )
                                  

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
                                 IGetPaidManagementLegalDisclaimerOptions
                                ):
    """ One-stop configuration access from a single interface 
    """

class ICountriesStates(Interface):
    countries = Iterable(
        title = _(u"countries"),
        description=_(u"A list of countries")
        )
    states = Iterable(
        title = _(u"states"),
        description=_(u"A list of states")
        )

class IMonthsAndYears(Interface):
    months = Iterable(
        title = _(u"months"),
        description=_(u"The list of months")
        )
    years = Iterable(
        title = _(u"years"),
        description=_(u"A list of years")
        )
