"""
$Id$
"""

from zope import schema, interface

from getpaid.core import interfaces

from zope.i18nmessageid import MessageFactory
_ = MessageFactory('getpaid.nullpayment')

class INullPaymentOptions( interfaces.IPaymentProcessorOptions ):
    """
    Null Payment Options
    """

    allow_authorization = schema.Choice(
        title=_(u"Allow Authorizations"),
        default=u"allow_authorization",
        values = (u"allow_authorization",
                  u"no_authorization")
        )

    allow_capture = schema.Choice(
        title=_(u"Allow Captures"),
        default=u"allow_capture",
        values = (u"allow_capture",
                  u"no_capture" )
        )

    allow_refunds = schema.Choice(
        title=_(u"Allow Refunds"),
        default=u"allow_refund",
        values = (u"allow_refund",
                  u"no_refund" )
        )



