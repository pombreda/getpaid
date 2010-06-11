from zope import schema, interface
from persistent import Persistent

from getpaid.core import interfaces

from getpaid.verkkomaksut.interfaces import IVerkkomaksutProcessor, IVerkkomaksutOptions, IVerkkomaksutOrderInfo

from urllib import urlencode
from urllib2 import urlopen, Request


class VerkkomaksutProcessor( Persistent ):

    interfaces.implements(IVerkkomaksutProcessor,
                          IVerkkomaksutOptions)

    def __init__( self ):
        # initialize defaults from schema
        for name, field in schema.getFields( IVerkkomaksutOptions ).items():
            field.set( self, field.query( self, field.default ) )
        super( VerkkomaksutProcessor, self).__init__()

    def capture(self, order, price):
        # always returns async - just here to make the processor happy
        return interfaces.keys.results_async

    def authorize( self, order, payment ):
        action_url = "https://ssl.verkkomaksut.fi/payment.svm"
        order_info = IVerkkomaksutOrderInfo(order)()
        data = urlencode(order_info)
        request = Request(action_url, data)
        f = urlopen(request)
        return self.request.response.redirect(f.geturl())
