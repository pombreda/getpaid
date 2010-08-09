"""
Payment Processor Options for PloneGetPaid
"""

__version__ = "$Revision$"
# $Id$
# $URL$

from z3c.form import field

from Products.PloneGetPaid.browser.admin_processors import PaymentProcessorOptionsBase

from getpaid.nullpayment.interfaces import INullPaymentOptions
from getpaid.nullpayment import NullPaymentProcessor as factory


class NullPaymentOptions(PaymentProcessorOptionsBase):
    prefix = factory.name
    label = factory.title
    fields = field.Fields(INullPaymentOptions)
