from Products.Five import BrowserView
from getpaid.core.interfaces import IOrderManager
from zope.component import getUtility


class OgoneCheck(BrowserView):
    """
    A class which check
    """

    def __call__(self):
        """
        This takes the order Id and returns
        the XML to Ogone
        """
        orderId = self.request.orderID
        orderManager = getUtility(IOrderManager)
        order = orderManager.get(orderId)
        shippingType = order.deliveryInformations.shipping
        countryId = order.countryId
        ogonePrice = int(order.getTotalPrice(countryId,
                                             shippingType) * 100)
        return '<orderid="%s" amount="%s" currency="%s">' % (order.getOrderId(),
                                                             ogonePrice,
                                                             order.currencyId)
