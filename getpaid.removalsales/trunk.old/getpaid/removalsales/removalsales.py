from zope.interface import implements
from zope.component import adapts
from Products.CMFCore.utils import getToolByName

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
        siteroot = getToolByName(self.context, "portal_url").getPortalObject()
        options = IRemovalsalesOptions(siteroot)
        if options.removalsalesAuthorize:
            # Release sales have no monetary transactions, hence they're always successful
            return keys.results_success
        else:
            return keys.results_async

    def authorize(self, order, payment):
        pass

