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
        values = ( "Test", "Production" ),
        )

    merchant_id = schema.TextLine( title = u"Merchant Id")
    merchant_key = schema.ASCII( title = u"Merchant Key")
