from zope.interface import Interface
from getpaid.core.interfaces import ILineItemFactory

class IOneWeekCreditPublishedContent(Interface):
    """Marker for content published by the week with credits"""

class IPublishController(Interface):
    """Marker"""

class IOneWeekPublishedCredit(Interface):
    """Marker representing the credit required to publish an item for a week"""

class IMonthlyMembershipCreditPublishedContent(Interface):
    """Marker for content published by virtue of group membership"""

class IMonthlyMembershipCredit(Interface):
    """Marker representing the credit required to be a member of the MonthlyMembership group"""

class ICreditPurchasingLineItemFactory(ILineItemFactory):
    """A LineItemFactory that does not use the context"""
