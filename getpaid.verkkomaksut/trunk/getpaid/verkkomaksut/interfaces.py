from zope import schema
from zope.interface import Interface
from getpaid.core.interfaces import IPaymentProcessor,IPaymentProcessorOptions
from getpaid.verkkomaksut import VerkkomaksutMessageFactory as _

class IVerkkomaksutProcessor(IPaymentProcessor):
    """
    Verkkomaksut Processor
    """

class IVerkkomaksutOptions(IPaymentProcessorOptions):
    """
    Verkkomaksut Options
    """

    merchant_id = schema.ASCIILine( 
                        title = _(u"Merchant ID"),
                        description = _("Input merchant ID provided by Verkkomaksut. For test, use 13466."),
                        required=True,
                        )

    merchant_authentication_code = schema.ASCIILine( 
                        title = _(u"Merchant Authentication Code"),
                        description = _("Input marchant authentication code provided by Verkkomaksut."),
                        required=True,
                        )

### Adapters
class IVerkkomaksutOrderInfo(Interface):
    def __call__():
        """Returns information of order."""
