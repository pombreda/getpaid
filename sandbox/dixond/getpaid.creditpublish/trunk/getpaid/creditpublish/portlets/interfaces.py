__author__ = """Darryl Dixon <darryl.dixon@winterhouseconsulting.com>"""

from zope import schema

from zope.interface import Interface
from plone.portlets.interfaces import IPortletDataProvider

from getpaid.creditpublish import creditpublishMessageFactory as _

class ICreditPublishingPortlet(IPortletDataProvider):
    """A portlet for publishing an item with credit.
    """

class ICreditPurchasingPortlet(IPortletDataProvider):
    """A portlet for purchasing credit for publishing.
    """

    representative_object = schema.ASCIILine(title=_(u"Representative Object UID"),
                                             description=_(u"The UID of an object which represents the credit to be purchase. It must adapt to IBuyableContent"),
                                             default="")
