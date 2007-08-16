"""
"""

from getpaid.core import interfaces
from zope import schema
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('getpaid')

class IMoneyTransferStandardProcessor( interfaces.IPaymentProcessor ):
    """
    Money Transfer Standard Processor
    """

class IMoneyTransferStandardOptions( interfaces.IPaymentProcessorOptions ):
    """
    Money Transfer Standard Options
    """
    
    payee = schema.TextLine( title=_(u"The recipient of the money transfer") )
    
    account_details = schema.Text( title=_(u"Recipient account details") )

