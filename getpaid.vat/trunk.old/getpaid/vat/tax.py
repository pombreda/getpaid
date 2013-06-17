import decimal
from zope.interface import implements

from getpaid.core.interfaces import ITaxUtility

from getpaid.vat import getpaidgstMessageFactory as _

class TaxUtility(object):
    implements(ITaxUtility)

    def getCost(self, order):
        """Calculate VAT at 14% on the subtotal and any shipping costs"""
        return float(order.getSubTotalPrice() + order.getShippingCost()) * self.tax_rate

    def getTaxes(self, order):
        return [{'value' : self.getCost(order), 'name' : self.tax_name}]


    def getTaxOnSum(self, sum):
        """Return the VAT value of a price, rounded to the nearest cent"""
        return float('%.2f' % (sum * self.tax_rate))

    @property
    def tax_rate(self):
        return 0.14

    @property
    def tax_name(self):
        return _(u"VAT")