"""
Verkkomaksut.fi language utility
"""

__version__ = "$Revision$"
# $Id$
# $URL$

from persistent import Persistent

from zope import schema, interface

from getpaid.core import interfaces

from getpaid.verkkomaksut.interfaces import IVerkkomaksutProcessor, IVerkkomaksutOptions

from urllib import urlencode
from urllib2 import urlopen, Request


class VerkkomaksutProcessor(Persistent):

    interfaces.implements(IVerkkomaksutProcessor,
                          IVerkkomaksutOptions)

    def __init__(self):
        # initialize defaults from schema
        for name, field in schema.getFields( IVerkkomaksutOptions ).items():
            field.set(self, field.query( self, field.default ))
        super(VerkkomaksutProcessor, self).__init__()

    def authorize(self, order, payment):
        # authorize only if order already paid through button
        # otherwise, 
        #   return interfaces.keys.results_async
        import pdb; pdb.set_trace()
        return "Authorization failed"

    def capture(self, order, price):
        # always returns async - just here to make the processor happy
        return interfaces.keys.results_async

    def refund(self, order, amount):
        return "Refund failed"
