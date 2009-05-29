from Products.Five import BrowserView
from getpaid.core.interfaces import IOrderManager
from getpaid.vcs.interfaces import IVcsStandardOptions
from zope.component import getUtility

class VcsCheck(BrowserView):
    """
    A class which check
    """

    def __call__(self):
        """
        This takes the order Id and returns
        the XML to VCS
        """
        orderId = self.request.orderID
        options = IVcsStandardOptions(self.context)
        currency = options.currency
        orderManager = getUtility(IOrderManager)
        order = orderManager.get(orderId)
        vcsPrice = order.getTotalPrice()
        return '<orderid="%s" amount="%s" currency="%s">' % (order.getOrderId(),
                                                             vcsPrice,
                                                             currency)
