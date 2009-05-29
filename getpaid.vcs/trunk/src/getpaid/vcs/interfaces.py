from getpaid.core import interfaces
from zope import schema
from getpaid.vcs import _


class IVcsStandardOptions(interfaces.IPaymentProcessorOptions):
    """
    VCS Standard Options
    """
    server_url = schema.Choice(title = _(u"VCS Website Payments Server"),
                               vocabulary = "getpaid.vcs.server_urls")

    pspid = schema.ASCIILine(
        description = _(u"Enter here your VCS Terminal ID"),
        required = True,
        title = _(u"VCS Terminal Id"))

    orderdesc = schema.TextLine(
        description = _(u"Enter a description for all orders"),
        required = True,
        title = _(u"Description of Goods"))

    currency = schema.Choice(
        title = _(u"Currency"),
        vocabulary = "getpaid.vcs.currencies")
    

## The following code is commented out and not removed for future use.
##
##    accept_url = schema.URI(
##        title = _("Accept URL"),
##        required = False,
##        description = _(u"The url of the page that display the success of the payment"))
##
##    cancel_url = schema.URI(
##        title = _("Cancel URL"),
##        required = False,
##        description = _(u"The url of the page which is displayed when the payment is cancelled"))
##
##    decline_url = schema.URI(
##        title = _("Decline URL"),
##        required = False,
##        description = _(u"The url of the page which is displayed when the payment is refused by the band card company"))
##
##    error_url = schema.URI(
##        title = _("Error URL"),
##        required = False,
##        description = _(u"The url of the page which is displayed when there is an error in the payment transation"))#
##
##    use_portal_css = schema.Bool(
##        title = _(u"Use css defined in this portal ?"),
##        required = False)


class IVcsStandardProcessor(interfaces.IPaymentProcessor):
    """
    VCS Standard Processor
    """
