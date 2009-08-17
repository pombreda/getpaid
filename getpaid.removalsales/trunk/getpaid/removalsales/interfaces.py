from zope import schema
from zope.interface import Interface
from getpaid.core.interfaces import IPaymentProcessor, IPaymentProcessorOptions

from getpaid.removalsales import _

class IRemovalsalesProcessor(IPaymentProcessor):
    """
    Removalsales Processor
    """

class IRemovalsalesOptions(IPaymentProcessorOptions):
    """
    Removalsales Options
    """
    
    removalsalesAuthorize = schema.Bool(
                                             title=_(u"Authorize Sale"),
                                             description=_(u"Authorize sale on completion."),
                                             required=False,
                                             default=True
                                             )

    removalsalesMarkAsDelivered = schema.Bool(
                                             title=_(u"Mark As Delivered"),
                                             description=_(u"Mark sales as delivered on completion."),
                                             required=False,
                                             default=True
                                             )
