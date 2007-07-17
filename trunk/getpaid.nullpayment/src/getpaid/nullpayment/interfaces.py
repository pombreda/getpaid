"""
$Id$
"""

from zope import schema, interface

from getpaid.core import interfaces

class INullPaymentOptions( interfaces.IPaymentProcessorOptions ):
    """
    Null Payment Options
    """

    allow_authorization = schema.Choice(
        title=u"Allow Authorizations",
        default=u"allow_authorization",
        values = (u"allow_authorization",
                  u"no_authorization")
        )

    allow_capture = schema.Choice(
        title=u"Allow Captures",
        default=u"allow_capture",
        values = (u"allow_capture",
                  u"no_capture" )
        )

    allow_refunds = schema.Choice(
        title=u"Allow Refunds",
        default=u"allow_refund",
        values = (u"allow_refund",
                  u"no_refund" )
        )
        
                  
                  
