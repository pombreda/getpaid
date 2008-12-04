import urllib, urllib2
import socket
import logging

from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from zope.component import getUtility

from getpaid.core.interfaces import IOrderManager

from getpaid.paypal.interfaces import IPaypalStandardOptions
from getpaid.paypal.paypal import _sites

from notification import Notification

logger = logging.getLogger("Plone")

class IPNListener(BrowserView):
    """Listener for Paypal IPN notifications - registered as a page view
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.portal = getToolByName(self.context, 'portal_url').getPortalObject()
    
    def process(self):
        this_notification = Notification(self.request)
        is_valid_IPN = self.verify()
        order_manager = getUtility(IOrderManager)
        if this_notification.invoice in order_manager:
            order = order_manager.get(this_notification.invoice)
            if not self.compare_cart(this_notification, order):
                logger.info('getpaid.paypal: received IPN that does match order number %s' % this_notification.invoice)
                # bad IPN - do not apply to transaction
                return
            if this_notification.payment_status == 'Completed':
                order.finance_workflow.fireTransition('charge-charging')
                logger.info('getpaid.paypal: received successful IPN payment notification for order %s' % this_notification.invoice)
                return
            if this_notification.payment_status == 'Failed':
                order.finance_workflow.fireTransition('decline-charging')
                logger.info('getpaid.paypal: received unsuccessful IPN payment notification for order %s' % this_notification.invoice)
                return
            # IPN not of interest to us right now
            logger.info('getpaid.paypal: received IPN for order %s that is not of interest' % this_notification.invoice)
            return
        # invoice not in cart
        logger.info('getpaid.paypal: received IPN that does not apply to any order number')
        return 
        
    def compare_cart(self, notification, order):
        import pdb
        pdb.set_trace()
        for ref in order.shopping_cart.keys():
            cart_item = order.shopping_cart[ref]
            if notification.shopping_cart.has_key(cart_item.product_code):
                notification_item = notification.shopping_cart[cart_item.product_code]
                if int(cart_item.quantity) != int(notification_item.quantity):
                    return False
            else:
                # item not in returned cart - invalid IPN response
                return False
        # everything checks out
        return True
            


    def verify(self):
        options = IPaypalStandardOptions( self.portal )
        
        # get ready to POST back form variables
        
        form = self.request.form
        params =[(key, form[key]) for key in form.keys() if key != 'cmd']
        params = [('cmd', '_notify-validate')] + params
        paramData = urllib.urlencode(params)
        url = "https://%s/cgi-bin/webscr" % _sites[options.server_url]
        
        # TODO: is this dangerous for other products?
        socket.setdefaulttimeout(120)
        try:
            connection = urllib2.urlopen(url, paramData)
        except urllib2.error.URLError:
            raise IOError, 'IPN post-back failed'
        response = connection.read()
        connection.close()
               
        if response == 'VERIFIED':
            return True
        else:
            return False
