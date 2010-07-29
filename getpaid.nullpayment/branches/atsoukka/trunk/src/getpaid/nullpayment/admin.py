"""
Payment Processor Options for PloneGetPaid
"""

__version__ = "$Revision$"
# $Id$
# $URL$

from z3c.form import field

from Products.PloneGetPaid.browser.admin_processors import PaymentProcessorOptionsBase

from getpaid.nullpayment import NAME, TITLE
from getpaid.nullpayment.interfaces import INullPaymentOptions


class NullPaymentOptions(PaymentProcessorOptionsBase):
    prefix = NAME
    label = TITLE
    fields = field.Fields(INullPaymentOptions)
