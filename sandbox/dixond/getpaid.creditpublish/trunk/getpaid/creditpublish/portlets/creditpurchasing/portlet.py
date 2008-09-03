__author__ = """Darryl Dixon <darryl.dixon@winterhouseconsulting.com>"""

from zope.interface import implements
from zope.component import getUtility
from zope.formlib import form

from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from plone.memoize.instance import memoize
from cornerstone.browser.base import RequestMixin
from DateTime.DateTime import DateTime

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

from getpaid.creditregistry.interfaces import ICreditRegistry

from getpaid.creditpublish import creditpublishMessageFactory as _
from getpaid.creditpublish.interfaces import IOneWeekPublishedCredit
from getpaid.creditpublish.portlets.interfaces import ICreditPurchasingPortlet

class Assignment(base.Assignment):
    implements(ICreditPurchasingPortlet)

    def __init__(self, representative_object=None):
        self.representative_object = representative_object

    @property
    def title(self):
        return _(u'getpaid.creditpurchasing', default=u'Credit Purchasing')
    
class Renderer(base.Renderer, RequestMixin):
    
    render = ViewPageTemplateFile('purchasing.pt')
    nameprefix = 'getpaid.creditpurchasing'

    def __init__(self, context, request, view, manager, data):
        super(Renderer, self).__init__(context, request, view, manager, data)
        # XXX FIX THIS UP SO THAT WE USE THE VIRTUAL ROOT
        self.sitepath = '/'
        self.pmt = getToolByName(self.context, 'portal_membership')
        self.pct = getToolByName(self.context, 'portal_catalog')
        self.cr = getUtility(ICreditRegistry)

    @property
    def available(self):
        if not self.pmt.isAnonymousUser():
            if self.pct.unrestrictedSearchResults(UID=self.data.representative_object):
                return True
        return False

    def formname(self):
        return "%s.form" % self.nameprefix

    def current_credit(self):
        member = self.pmt.getAuthenticatedMember()
        return self.cr.queryCredit(member.getId(), IOneWeekPublishedCredit.__identifier__)

    def weeks_options(self):
        return range(1, 53)

class AddForm(base.AddForm):
    form_fields = form.Fields(ICreditPurchasingPortlet)
    label = _(u"Add Credit Purchasing Portlet")
    description = _(u"This portlet displays purchasable credits")

    # This method must be implemented to actually construct the object.
    # The 'data' parameter is a dictionary, containing the values entered
    # by the user.

    def create(self, data):
        assignment = Assignment()
        form.applyChanges(assignment, self.form_fields, data)
        return assignment

class EditForm(base.EditForm):
    form_fields = form.Fields(ICreditPurchasingPortlet)
    label = _(u"Edit Credit Purchasing Portlet")
    description = _(u"This portlet displays purchasable credits")
