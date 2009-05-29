from Products.CMFCore.utils import getToolByName
from getpaid.core.options import PersistentOptions
from getpaid.core.interfaces import IOrderManager, IShoppingCartUtility
from getpaid.vcs.interfaces import IVcsStandardProcessor, IVcsStandardOptions
from zope.i18n.interfaces import IUserPreferredLanguages
from zope.interface import implements
from zope.component import getUtility
from getpaid.core.interfaces import keys
import interfaces
import urllib
import urllib2
import sha

VcsStandardOptions = PersistentOptions.wire("VcsStandardOptions",
                                              "getpaid.vcs",
                                              interfaces.IVcsStandardOptions)


class VcsStandardProcessor(object):
    """
    VCS Standard Processor
    """
    implements(IVcsStandardProcessor)

    options_interface = IVcsStandardOptions

    def __init__(self, context):
        self.context = context

    def cart_post_button(self, cart):
        options = IVcsStandardOptions(self.context)

    def authorize(self, order, payment_information):
        """
        authorize an order, using payment information.
        """
        order_manager = getUtility(IOrderManager)
        order_manager.store(order)
        base_url = self.context.absolute_url()
        url = base_url + '/@@getpaid-vcs-redirect?orderid=%s' % (order.order_id)
        self.context.request.response.redirect(url)

    def capture(self, order, amount):
        """
        capture amount from order.
        """
        return keys.results_async

    def refund(self, order, amount):
        """
        reset
        """
