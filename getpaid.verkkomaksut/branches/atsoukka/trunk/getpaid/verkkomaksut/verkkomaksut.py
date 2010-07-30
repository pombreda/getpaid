"""
Verkkomaksut.fi language utility
"""

__version__ = "$Revision$"
# $Id$
# $URL$

from persistent import Persistent

from zope import schema, interface

from getpaid.core import interfaces
from getpaid.core.interfaces import workflow_states as wf

from getpaid.verkkomaksut.interfaces import IVerkkomaksutProcessor, IVerkkomaksutOptions


class VerkkomaksutProcessor(Persistent):

    interfaces.implements(IVerkkomaksutProcessor,
                          IVerkkomaksutOptions)

    def __init__(self):
        # initialize defaults from schema
        for name, field in schema.getFields( IVerkkomaksutOptions ).items():
            field.set(self, field.query( self, field.default ))
        super(VerkkomaksutProcessor, self).__init__()

    def authorize(self, order, payment):
        # authorization only through payment button
        if order.finance_state == wf.order.finance.CHARGED:
            # return normal "success" if charging was already done
            return interfaces.keys.results_success
        # I dislike the idea of returning "interfaces.keys.results_async" here,
        # because even this is an offsite processor, this can't really do anything
        # asynchronously here, but only through user clicking the payment button.
        return _(u"Authorization failed")

    def capture(self, order, price):
        # capture only with authorization through payment button
        if order.finance_state == wf.order.finance.CHARGED:
            # return normal "success" if charging was already done
            return interfaces.keys.results_success
        # I dislike the idea of returning "interfaces.keys.results_async" here,
        # because even this is an offsite processor, this can't really do anything
        # asynchronously here, but only through user clicking the payment button.
        return _(u"Capture failed")

    def refund(self, order, amount):
        # refund not supported
        return _(u"Refund failed")
