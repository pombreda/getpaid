"""
$Id: $
"""

from zope import schema, interface
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from getpaid.core import interfaces, options
from getpaid.core.interfaces import IShippingRateService, IShippingMethodSettings
from getpaid.core.interfaces import IShippableLineItem

from zope.i18nmessageid import MessageFactory
_ = MessageFactory('getpaid.flatrateshipping2')

MY_SHIPPING_SERVICES = SimpleVocabulary([
        SimpleTerm('01', 'flat-rate', _(u' Flat Rate')),])

class IFlatRateService( IShippingRateService ):
    """
    Flat Rate Shipping Service
    """
    
    def getRates( order ):
        """ return shipping rate options for an order.  this should return:
        - a list of IShippingMethodRate as 'shipments'
        - an error string as 'error'
        """

    def getMethodName( method_id ):
        """
        given a shipping method service code, returns a shipping method label/name
        """

    def getTrackingUrl( track_number ):
        """
        given a track number this should return, if available for this service
        a url that can be used to track the shipment
        """
        
class IFlatRateSettings( interface.Interface ):
    """
    Flate Rate Shipping Service Options
    """

    flatrate_option = schema.Choice(
        title=_(u"Shipping Rate Configuration"),
        description = _(u"Choose either a flat rate for all orders, or calculate shipping as a percentage of total order cost."),
        values = ( "Flat Rate", "Percentage" ),
        default = "Flat Rate",
        required=True,
        )
    
    flatrate_flatrate = schema.Float(
        title=_(u"Flat Shipping Rate"),
        description = _(u"If 'Flat Rate' is selected above, this is the rate applied to all orders."),
        default = 10.0,
        required=True,
        )
        
    flatrate_percentage = schema.Float(
        title=_(u"Flat Shipping Percentage"),
        description = _(u"If 'Percentage' is selected above, this is the percentage of the total order to charge for shipping."),
        default = 10.0,
        required=True,
        )
        
    flatrate_max = schema.Float(
        title=_(u"Max Handling Charge"),
        description = _(u"If 'Percentage' is selected above, the total shipping charge is never greater than this number."),
        default = 10.0,
        required=True,
        )
