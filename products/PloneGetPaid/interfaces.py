"""
$Id$
"""

from zope import schema
from zope.interface import Interface
from zope.schema import Iterable
from getpaid.core.fields import PhoneNumber

import getpaid.core.interfaces as igetpaid
import zope.viewlet.interfaces

from zope.i18nmessageid import MessageFactory
_ = MessageFactory('plonegetpaid')

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
    
    allow_anonymous_checkout = schema.Bool( title = _(u"Allow anonymous checkout"),
                                            required = True,
                                            default = False
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
                                
    contact_state = schema.Choice( title = _(u"Contact State/Province"),
                                   required = False,
                                   default = u"",
                                   vocabulary = "getpaid.states"
                                 )

    contact_postalcode = schema.TextLine( title = _(u"Contact Zip/Postal Code"),
                                          required = False,
                                          default = u""
                                        )

    contact_country = schema.Choice( title = _(u"Contact Country"),
                                     required = False,
                                     default = u"",
                                     vocabulary = "getpaid.countries"
                                   )

    contact_phone = schema.TextLine( title = _(u"Contact Phone"),
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
    #TODO: Compatibility field, to be removed
    #Returns the first one active processor
    payment_processor = schema.Choice( title = _(u"Payment Processor"),
                                       source = "getpaid.payment_methods" )

    payment_processors = schema.List( 
        title = _(u"Payment Processors"),
        default = [],
        description = _(u"The payment processors available for checkout."),
        value_type = schema.Choice( title=_(u"payment_methods"), source= "getpaid.payment_methods" )
        )

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


class ICheckoutInfoUtility( Interface ):
    """An utility for storing checkout details
    """
    def get( create=False ):
        """
        Return the user's checkout details or None if no details are set.
        If create is passed then create an empty set of checkout details.
        """

    def destroy( ):
        """
        Removes the current user's checkout details from the session.
        """
        
class IBuyerInfo( Interface ):
    """Contains the necessary fields for identifying a buyer
    """
    full_name = schema.TextLine( title=_(u"Full name"),
                                 description=_(u"Enter full name, eg. John Smith."),
                                 required=True )
                                 
    company = schema.TextLine( title=_(u"Company name"),
                              description=_(u"Enter your company name."),
                              required=False )

    email = schema.TextLine( title=_(u"Email"),
                            description=_(u"Enter a valid email address to receive the order confirmation."),
                            required=True )

class IBuyerTaxInfo ( Interface ):
    """Describes additional buyer attributes which can have a direct influence on order receipt / price calculation.
    """
    vat_id = schema.TextLine( title=_(u"VAT ID"),
                              description=_(u"Enter your VAT ID."),
                              required = False )

#Taken from ore.member
class IBuyerMemberInfo( IBuyerInfo ):
    """Describes a buyer which wants to register on the store after a successfull anonymous checkout.
    """

    login = schema.ASCIILine(title=u"User Name",
                             description=u"Enter a user name, usually something like 'jsmith'. No spaces or special characters. Usernames and passwords are case sensitive, make sure the caps lock key is not enabled. This is the name used to log in.")

    password = schema.ASCIILine(title=u"Password",
                                description=u"Minimum 5 characters.",                                
                                min_length=5)

    password_confirm = schema.ASCIILine( title=u"Password Confirmation",
                                         description=u"Re-enter the password. Make sure the passwords are identical.",
                                         min_length=5)

    mail_me = schema.Bool( title=u"Send a mail with the password",
                           required=False )

class IAddressActions( Interface ):
    """Temporary interface for exposing a custom "copy billing address to shipping address" field.
    """
    
    single_address = schema.Bool(title=u"Same as Billing address",
                                 required=False)