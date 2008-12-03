import urllib, urllib2
import socket

from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from zope.component import getUtility

from getpaid.core.interfaces import IOrderManager

from getpaid.paypal.interfaces import IPaypalStandardOptions
from getpaid.paypal.paypal import _sites

from notification import Notification

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
        import pdb
        pdb.set_trace()
        order_manager = getUtility(IOrderManager)
        if this_notification.invoice in order_manager:
            order = order_manager.get(this_notification.invoice)
            if this_notification.payment_status == 'Completed':
                order.finance_workflow.fireTransition('charge-charging')
        # TODO: handle failed transactions 
        
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
