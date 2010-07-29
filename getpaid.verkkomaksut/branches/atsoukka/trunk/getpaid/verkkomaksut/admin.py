"""
Payment Processor Options for PloneGetPaid
"""

__version__ = "$Revision$"
# $Id$
# $URL$


from z3c.form import field

from Products.PloneGetPaid.browser.admin_processors import PaymentProcessorOptionsBase

from getpaid.verkkomaksut import NAME, TITLE
from getpaid.verkkomaksut.interfaces import IVerkkomaksutOptions


class VerkkomaksutOptions(PaymentProcessorOptionsBase):
    prefix = NAME
    label = TITLE
    fields = field.Fields(IVerkkomaksutOptions)
