"""
Payment Processor Options for PloneGetPaid
"""

__version__ = "$Revision$"
# $Id$
# $URL$


from z3c.form import field

from Products.PloneGetPaid.browser.admin_processors import PaymentProcessorOptionsBase

from getpaid.verkkomaksut.interfaces import IVerkkomaksutOptions
from getpaid.verkkomaksut import VerkkomaksutProcessor as plugin


class VerkkomaksutOptions(PaymentProcessorOptionsBase):
    prefix = plugin.NAME
    label = plugin.TITLE
    fields = field.Fields(IVerkkomaksutOptions)
