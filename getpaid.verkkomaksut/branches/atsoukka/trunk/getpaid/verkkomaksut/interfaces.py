"""
Payment Processor Plugin interfaces
"""

__version__ = "$Revision$"
# $Id$
# $URL$

from zope import schema
from zope.interface import Interface

from getpaid.core.interfaces import IPaymentProcessor,IPaymentProcessorOptions
from getpaid.wizard.interfaces import IWizardController

from zope.i18nmessageid import MessageFactory
_ = MessageFactory('getpaid.verkkomaksut')


class IVerkkomaksutProcessor(IPaymentProcessor):
    """
    Verkkomaksut Processor
    """


### Options
class IVerkkomaksutOptions(IPaymentProcessorOptions):
    """
    Verkkomaksut Options
    """

    verkkomaksut_merchant_id = schema.ASCIILine( 
        title = _(u"Merchant ID"),
        description = _("Input merchant ID provided by Verkkomaksut."),
        required = True)

    merchant_authentication_code = schema.ASCIILine( 
        title = _(u"Merchant Authentication Code"),
        description = _("Input marchant authentication code provided by Verkkomaksut."),
        required = True)

### Adapters
class IVerkkomaksutPayload(Interface):
    """ Adapts order for Verkkomaksut.fi."""

class IVerkkomaksutPayment(Interface):
    """ Adapts request from Verkkomaksut.fi."""

### Utilities
class ILanguageCulture(Interface):
    def __call__(language_bindings):
        """Returns Verkkomaksut.fi culture code."""
