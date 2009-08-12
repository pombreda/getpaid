from zope.interface import implements
from zope.component import adapts

from getpaid.core.interfaces import IStore
from getpaid.core.interfaces import keys

from interfaces import IRemovalsalesProcessor, IRemovalsalesOptions

class RemovalsalesProcessor(object):

    implements(IRemovalsalesProcessor)
    adapts(IStore)

    options_interface = IRemovalsalesOptions
    
    def __init__(self, context):
        self.context = context

    def capture(self, order, price):
        # Release sales have no monetary transactions, hence they're always successful
        return keys.results_success

    def authorize(self, order, payment):
        pass

