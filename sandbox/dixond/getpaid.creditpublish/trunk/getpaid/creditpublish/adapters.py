from zope.component import adapts
from zope.interface import implements

from getpaid.core.interfaces import IOrder, ILineItem
from getpaid.creditregistry.interfaces import ICreditRegistryItem
from interfaces import IOneWeekPublishedCredit, IMonthlyMembershipCredit

class OneWeekPublishedCreditRegistryAdapter(object):
    """The adapter for IOneWeekPublishedCredit to ICreditRegistryItem
    """
    adapts(IOrder, ILineItem, IOneWeekPublishedCredit)
    implements(ICreditRegistryItem)

    def __init__(self, order, item, object):
        self.order = order
        self.item = item
        self.object = object

    @property
    def credit_name(self):
        return IOneWeekPublishedCredit.__identifier__

    @property
    def credit_amount(self):
        return self.item.quantity

    @property
    def user_name(self):
        return self.order.user_id

class MonthlyMembershipCreditRegistryAdapter(object):
    """The adapter for IMonthlyMembershipCredit to ICreditRegistryItem
    """
    adapts(IOrder, ILineItem, IMonthlyMembershipCredit)
    implements(ICreditRegistryItem)

    def __init__(self, order, item, object):
        self.order = order
        self.item = item
        self.object = object

    @property
    def credit_name(self):
        return IMonthlyMembershipCredit.__identifier__

    @property
    def credit_amount(self):
        return self.item.quantity

    @property
    def user_name(self):
        return self.order.user_id

