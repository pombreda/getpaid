"""
$Id: interfaces.py 10 2007-05-10 15:34:29Z kapilt $
"""

from getpaid.core import interfaces
from zope import schema

class IGoogleCheckoutProcessor( interfaces.IPaymentProcessor ):
    """
    Google Checkout Processor
    """

class IGoogleCheckoutOptions( interfaces.IPaymentProcessorOptions ):
    """
    Google Checkout Options
    """
    server_url = schema.Choice(
        title = u"Google Checkout Server URL",
        values = ( "Sandbox", "Production" ),
        )

    merchant_id = schema.ASCIILine( title = u"Merchant Id")
    merchant_key = schema.ASCIILine( title = u"Merchant Key")
