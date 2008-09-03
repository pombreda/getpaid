from zope import schema
from zope.interface import Interface

from zope.app.container.constraints import contains
from zope.app.container.constraints import containers

from getpaid.core.interfaces import IPayableLineItem, IBuyableContent
from getpaid.purchasablecredits import purchasablecreditsMessageFactory as _

# -*- extra stuff goes here -*-
class IPurchasableCredit(Interface):
    """A content type representing a purchase of credit
    """

class IPurchasableCreditLineItem(IPayableLineItem):
    """Used to mark a line item that is a credit purchase.
    """

class IPurchasableCreditBuyable(IBuyableContent):
    """Implements the buyable interface"""
