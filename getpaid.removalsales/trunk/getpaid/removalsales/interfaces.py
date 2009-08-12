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
