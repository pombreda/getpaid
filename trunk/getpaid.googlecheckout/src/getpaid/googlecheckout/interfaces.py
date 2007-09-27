"""
$Id: interfaces.py 10 2007-05-10 15:34:29Z kapilt $
"""

from getpaid.core import interfaces
from zope import schema

from zope.i18nmessageid import MessageFactory
_ = MessageFactory('getpaid.googlecheckout')

class IGoogleCheckoutProcessor( interfaces.IPaymentProcessor ):
    """
    Google Checkout Processor
    """

class IGoogleCheckoutOptions( interfaces.IPaymentProcessorOptions ):
    """
    Google Checkout Options
    """
    server_url = schema.Choice(
        title = _(u"Google Checkout Server URL"),
        values = ( "Sandbox", "Production" ),
        )

    merchant_id = schema.ASCIILine( title = _(u"Merchant Id"))
    merchant_key = schema.ASCIILine( title = _(u"Merchant Key"))
