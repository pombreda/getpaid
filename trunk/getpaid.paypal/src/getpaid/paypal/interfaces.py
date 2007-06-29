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
        title = u"Paypal Website Payments Server",
        values = ( "Sandbox", "Production" ),
        )

    merchant_id = schema.ASCIILine( title = u"Paypal Id")
