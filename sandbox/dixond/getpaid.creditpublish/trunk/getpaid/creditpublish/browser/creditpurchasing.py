i__author__ = """Darryl Dixon <darryl.dixon@winterhouseconsulting.com>"""

from zope.component import getUtility, getMultiAdapter

from plone.memoize.instance import memoize
from cornerstone.browser.base import RequestMixin
from DateTime.DateTime import DateTime

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

from getpaid.core.interfaces import ILineItemFactory
from getpaid.creditpublish import creditpublishMessageFactory as _
from getpaid.creditpublish.interfaces import IOneWeekPublishedCredit #, ICreditPurchasingLineItemFactory

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.PloneGetPaid.browser.cart import ShoppingCart

class CreditPurchasing(ShoppingCart, RequestMixin):
    """A class to handle custom purchases of 'credit' items
       access via @@credit_purchasing
    """

    nameprefix = 'getpaid.creditpurchasing'

    def __call__(self, weeks=0):
        pct = getToolByName(self.context, 'portal_catalog')
        url = self.context.absolute_url()
        if self.request.get('REQUEST_METHOD', '') == 'POST':
            # Find out if this is really for us
            if self.formvalue('submitted') is not None:
                # Yep
                # Always deny anonymous checkout (it's insane for user credits)
                if getToolByName(self.context, 'portal_membership').isAnonymousUser():
                    url = "%s/%s?%s" % (url, 'login_form')
                else:
                    # We'll send the user back here after purchases of this type of credit
                    self.sessionset(IOneWeekPublishedCredit.__identifier__, self.request['ACTUAL_URL'])
                    weeks = self.formvalue('weeks')
                    credititem = self.formvalue('credititem')
                    credititem = pct.unrestrictedSearchResults(UID=credititem)
                    if credititem:
                        credititem = credititem[0].getObject()
                        # create a line item and add it to the cart
                        item_factory = getMultiAdapter((self.cart, credititem), ILineItemFactory)
                        # check quantity from request
                        item_factory.create(quantity=weeks)
                    url += '/@@getpaid-checkout-wizard'
        return self.request.RESPONSE.redirect(url)
