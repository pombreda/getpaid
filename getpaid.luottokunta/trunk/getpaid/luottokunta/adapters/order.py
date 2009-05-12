from zope.interface import implements
from zope.component import adapts
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
import md5
from zope.app.component.hooks import getSite

from getpaid.core.order import Order

### For implements.
from getpaid.luottokunta.interfaces import ILuottokuntaOrderInfo

### For call.
from getpaid.luottokunta.interfaces import ILuottokuntaOptions

class LuottokuntaOrderInfo(object):

    implements(ILuottokuntaOrderInfo)
    adapts(Order)

    def __init__(self, context):
        self.context = context

    def __call__(self):
        """Returns information of order."""
        site = getSite()
        context = aq_inner(self.context)
        order_id = context.order_id
        price = context.getTotalPrice()
        luottokunta_price = str(int(price * 100))
        options = ILuottokuntaOptions(site)
        merchant_number = options.merchant_number
        if options.use_dossier_id:
            dossier_id = options.dossier_id
        else:
            dossier_id = None
        if options.card_details_transmit:
            card_details_transmit = "1"
            language = None
        else:
            card_details_transmit = "0"
            language = options.language
        if options.transaction_type:
            transaction_type = "1"
        else:
            transaction_type = "0"
        if options.use_authentication_mac:
            m = md5.new()
            m.update(merchant_number)
            m.update(order_id)
            m.update(luottokunta_price)
            m.update(transaction_type)
            m.update(options.authentication_mac)
            authentication_mac = m.hexdigest()
        else:
            authentication_mac = None
        order_info = {
                        'price': luottokunta_price,
                        'authentication_mac': authentication_mac,
                        'order_number': order_id,
                        'card_details_transmit': card_details_transmit,
                        'transaction_type': transaction_type,
                        'language' : language,
        }
        return order_info
