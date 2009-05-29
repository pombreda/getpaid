from Products.Five import BrowserView
from getpaid.core.interfaces import IOrderManager
from getpaid.vcs.interfaces import IVcsStandardOptions
from zope.component import getUtility
import sha


class VcsPostProcessAccepted(BrowserView):
    """
    The Vcs payment has been accepted
    """

    def __call__(self):
        """
        We update the order information and returns the template
        """
        orderId = self.request.orderID
        options = IVcsStandardOptions(self.context)
        currency = options.currency
        orderManager = getUtility(IOrderManager)
        order = orderManager.get(orderId)
        order.finance_workflow.fireTransition("charge-charging")
        return 1


class VcsPostProcessCancelled(BrowserView):
    """
    The Ogone payment has been cancelled
    """

    def __call__(self):
        """
        We update the order information and returns the template
        """
        orderId = self.request.orderID
        options = IVcsStandardOptions(self.context)
        currency = options.currency
        orderManager = getUtility(IOrderManager)
        order = orderManager.get(orderId)
        order.finance_workflow.fireTransition("decline-charging")
        return 1
