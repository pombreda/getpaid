from zope.interface import implements
from zope.component import adapts
from Products.CMFCore.interfaces import ISiteRoot
from getpaid.core.interfaces import keys
from getpaid.verkkomaksut.interfaces import IVerkkomaksutProcessor, IVerkkomaksutOptions

from urllib import urlencode, urlopen
import md5

class VerkkomaksutProcessor( object ):

    implements(IVerkkomaksutProcessor)
    adapts(ISiteRoot)

    options_interface = IVerkkomaksutOptions

    def __init__( self, context ):
        self.context = context

    def capture(self, order, price):
        # always returns async - just here to make the processor happy
        return keys.results_async

    def authorize( self, order, payment ):
        pass
