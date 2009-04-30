from zope import schema, interface
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from getpaid.core.interfaces import IPaymentProcessor,IPaymentProcessorOptions

from getpaid.luottokunta import LuottokuntaMessageFactory as _

# generate a Zope 3 vocabulary from a sequence of tuples, suitable for use in a drop-down menu
def _vocabulary(*terms):
    return SimpleVocabulary([SimpleTerm(token, token, title)
                             for token, title in terms])

class ILuottokuntaProcessor(IPaymentProcessor):
    """
    Luottokunta Processor
    """

class ILuottokuntaOptions(IPaymentProcessorOptions):
    """
    Luottokunta Options
    """
#    server_url = schema.Choice(
#        title = _(u"Paypal Website Payments Server"),
#        values = ( "Sandbox", "Production" ),
#        )

    merchant_number = schema.ASCIILine( 
                        title = _(u"Merchant Number"),
                        description = _("Input merchant ID provided by Luottokunta.")
                        )

    card_delails_transmit = schema.Bool(
                        title = _(u"Card Details Transmit"),
                        description = _("If card details' input happens at this plone site, check this option. If it happens at Luottokunta's page, leave this blank."),
                        )

    language = schema.Choice(
                        title = _(u"Language"),
                        vocabulary = _vocabulary(
                                    ('FI', u'Finnish'),
                                    ('EN', u'English'),
                                    ('SE', u'Swedish'),
                                    ),
                        description = _(u"This language is used on luottokunta page if card details' input happens at Luottokunta's page."),
                        )

    transaction_type = schema.Bool(
                        title = _(u"Transaction Type"),
                        description = _(u"If money receiver pays the provision to Luottokunta, check this option. If payer pays it, leave this blank.")
                        )

    use_authentication_mac = schema.Bool(
                        title = _(u"Use Authentication MAC"),
                        description = _(u"If authentication MAC is used to the card transactions, check this option, if else leave this blank.")
                        )

    authentication_mac = schema.ASCIILine( 
                        title = _(u"Authenticaition MAC"),
                        description = _("Input marchant's authentication MAC provided by Luottokunta. Remembet to allow MAC authentication at Luottokunta's administration page!!")
                        )

    allow_amex = schema.Bool(
                        title = _(u"American Express"),
                        description = _(u"If you allow AMEX as an payment method, check this option. Remember to read usage of AMEX located in Luottokunta's administaration page.")
                        )
