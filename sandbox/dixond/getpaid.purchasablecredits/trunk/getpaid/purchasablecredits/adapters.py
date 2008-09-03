from zope.component import adapts, getUtility
from zope.interface import implements

from five.intid.intid import IIntIds

from getpaid.core.interfaces import IOrder, IPayableLineItem, ILineItemFactory
from getpaid.core.item import PayableLineItem
from getpaid.creditregistry.interfaces import ICreditRegistryItem
from getpaid.purchasablecredits import purchasablecreditsMessageFactory as _

from Products.PloneGetPaid.content import LineItemFactory

from interfaces import IPurchasableCredit, IPurchasableCreditLineItem, IPurchasableCreditBuyable


class PurchasableCreditBuyableAdapter(object):
    """Trivial adapter from the PurchasableCredit content type to a Buyable
    """
    implements(IPurchasableCreditBuyable)
    adapts(IPurchasableCredit)

    def __init__(self, context):
        self.context = context

    @property
    def price(self):
        return float(self.context.getPrice())


class PurchasableCreditLineItemFactory(LineItemFactory):
    """Custom Line Item factory for IPurchasableCredit items
    """
    implements(ILineItemFactory)

    def checkPayable(self, content):
        # this is where we adapt content to our payable adapter that
        # knowns how to access the required properties.
        if IPurchasableCredit.providedBy(content):
            return IPurchasableCreditBuyable(content)
        else:
            raise RuntimeError(_(u"Unable to add this item to the Cart"))

    def createLineItem(self, payable, quantity):
        # payable should be our IPurchasableCredit item or an adapter for it
        nitem = PurchasableCreditLineItem()
        nitem.item_id = self.content.UID() # archetypes uid
        nitem.safe_id = self.content.getId()

        # we use intids to reference content that we can dereference cleanly
        # without access to context.
        nitem.uid = getUtility(IIntIds).register(self.content)

        # copy over information regarding the item
        nitem.name = self.content.Title()
        nitem.description = self.content.Description()
        nitem.cost = payable.price
        nitem.quantity = int(quantity)
        return nitem

class PurchasableCreditLineItem(PayableLineItem):
    """The Line Item produced by the PurchasableCreditLineItemFactory
    """
    implements(IPurchasableCreditLineItem)

class PurchasableCreditItemAdapter(object):
    """The adapter for IPurchasableCreditLineItem to ICreditRegistryItem
    """
    adapts(IOrder, IPurchasableCreditLineItem)
    implements(ICreditRegistryItem)

    def __init__(self, order, item):
        self.order = order
        self.item = item

    @property
    def credit_name(self):
        return self.item.safe_id

    @property
    def credit_amount(self):
        return self.item.quantity

    @property
    def user_name(self):
        return self.order.user_id
