from zope.interface import Interface
from zope import schema

from zope.i18nmessageid import MessageFactory
_ = MessageFactory('getpaid.paymentprocessors')

class IPaymentMethodInformation(Interface):
    """ Store information which payment method user selects on the checkout wizard """

    payment_method = schema.Choice( title = _(u"Payment method"),
                                      source = "getpaid.paymentprocessors.payment_processors",)