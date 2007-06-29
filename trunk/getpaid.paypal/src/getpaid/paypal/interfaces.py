"""
"""

from getpaid.core import interfaces
from zope import schema

class IPaypalStandardProcessor( interfaces.IPaymentProcessor ):
    """
    Paypal Standard Processor
    """

class IPaypalStandardOptions( interfaces.IPaymentProcessorOptions ):
    """
    Paypal Standard Options
    """
    server_url = schema.Choice(
        title = u"Paypal Website Payments Server URL",
        values = ( "Sandbox", "Production" ),
        )

    merchant_id = schema.ASCIILine( title = u"Merchant Id")
    merchant_key = schema.ASCIILine( title = u"Merchant Key")
