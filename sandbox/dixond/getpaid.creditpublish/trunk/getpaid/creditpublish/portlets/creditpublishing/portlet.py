__author__ = """Darryl Dixon <darryl.dixon@winterhouseconsulting.com>"""

from zope.interface import implements
from zope.component import getUtility

from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from cornerstone.browser.base import RequestMixin
from DateTime.DateTime import DateTime

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

from getpaid.creditregistry.interfaces import ICreditRegistry

from getpaid.creditpublish import creditpublishMessageFactory as _
from getpaid.creditpublish.interfaces import IOneWeekCreditPublishedContent, IOneWeekPublishedCredit
from getpaid.creditpublish.portlets.interfaces import ICreditPublishingPortlet

class Assignment(base.Assignment):
    implements(ICreditPublishingPortlet)

    title = _(u'getpaid.creditpublishing', default=u'Credit Publishing')
    
class Renderer(base.Renderer, RequestMixin):
    
    nameprefix = 'getpaid.creditpublishing'

    def __init__(self, context, request, view, manager, data):
        super(Renderer, self).__init__(context, request, view, manager, data)
        # XXX FIX THIS UP SO THAT WE USE THE VIRTUAL ROOT
        self.sitepath = '/'
        self.cr = getUtility(ICreditRegistry)
        self.wft = getToolByName(self.context, 'portal_workflow')
        self.pmt = getToolByName(self.context, 'portal_membership')

    @property
    def render(self):
        # This stops us from having convoluted logic in the page templates
        if self.is_listed:
            return ViewPageTemplateFile('published.pt')
        else:
            return ViewPageTemplateFile('unpublished.pt')

    @property
    def available(self):
        """Should this portlet be available?"""
        if IOneWeekCreditPublishedContent.providedBy(self.context):
            if not 'portal_factory' in self.request['ACTUAL_URL']:
                if self.user_is_creator:
                    if self.current_credit:
                        # If they've got credit then show the portlet regardless
                        return True
                    else:
                        # Only show the portlet when they have no credit if the context
                        # is already published - they need to be able to choose to withdraw
                        # it if necessary
                        if self.is_listed:
                            # OK, so we will show it so they can withdraw if necessary
                            return True
                        else:
                            # They have no credit and the context isn't published - instead
                            # of showing this portlet, we will let a more prominent BeforeContentViewlet
                            # inform them of the situation, and they can use the creditpurchasing portlet
                            # to remedy
                            return False
                else:
                    # User isn't creator
                    # XXX Probably this should be policy-pluggable - maybe people in the same group should
                    #     be able to publish each other's stuff?
                    return False
            else:
                # The object is still being added right now
                return False
        else:
            # Not a credit-published item
            return False

    def update(self):
        # Technically, the status=302 lines below should be status=303, except that IE6
        # FAILS IT EPICALLY when receiving a 303. Suck.
        if self.request.get('REQUEST_METHOD', '') == 'POST':
            # Find out if any of our settings were included in this
            if self.formvalue('submitted') is not None:
                # Paranoia:
                if self.user_is_creator:
                    # OK, so what action has been requested?
                    if self.formvalue('publish'):
                        if self.is_listed:
                            # They've probably just tried refreshing the previously submitted
                            # page. Better to just do nothing at this point
                            pass
                        else:
                            self.publishContext(self.formvalue('weeks'))
                            # The page has already rendered with self.context showing as 'private'
                            self.request.RESPONSE.redirect(self.request['ACTUAL_URL'], status=302)
                    elif self.formvalue('update'):
                        self.publishContext(self.formvalue('weeks'), update=True)
                    elif self.formvalue('depublish'):
                        if not self.is_listed:
                            # They've probably just tried refreshing the previously submitted
                            # page. Better to just do nothing at this point
                            pass
                        else:
                            self.depublishContext()
                            # The page has already rendered with self.context showing as 'published'
                            self.request.RESPONSE.redirect(self.request['ACTUAL_URL'], status=302)
        return True

    def publishContext(self, weeks, update=False):
        """Perform the various policy-steps necessary when publishing this context"""
        schema = self.context.Schema()
        if update:
            schema['republishReminderSent'].set(self.context, False)
            schema['weeksLeftPublished'].set(self.context, weeks)
        elif self.current_credit:
            self.wft.doActionFor(self.context, 'publish') 
            self.context.setEffectiveDate(DateTime())
            self.context.setExpirationDate(DateTime()+7)
            schema['republishReminderSent'].set(self.context, False)
            # When initially publishing, the first week is immediately used:
            schema['weeksLeftPublished'].set(self.context, weeks-1)
            self.cr.useCredit(self.pmt.getAuthenticatedMember().getId(), IOneWeekPublishedCredit.__identifier__, 1)
        else:
            return False
        self.context.reindexObject(idxs=['effective', 'expires', 'getWeeksLeftPublished', 'getRepublishReminderSent'])
        return True

    def depublishContext(self):
        """Perform the various policy-steps necessary when depublishing this context"""
        schema = self.context.Schema()
        self.wft.doActionFor(self.context, 'hide')
        schema['weeksLeftPublished'].set(self.context, 0)
        self.context.setExpirationDate(DateTime())
        self.context.reindexObject(idxs=['expires', 'getWeeksLeftPublished'])
        return True

    @property
    def formname(self):
        """stub"""
        return "%s.form" % self.nameprefix

    @property
    def user_is_creator(self):
        return self.pmt.getAuthenticatedMember().getId() == self.context.Creator()

    @property
    def is_listed(self):
        """stub"""
        if self.wft.getInfoFor(self.context, 'review_state') == 'published':
            if DateTime().lessThan(self.context.getExpirationDate()):
                return True
        return False
    
    @property
    def current_weeks(self):
        """stub"""
        # weeksLeftPublished comes from IOneWeekCreditPublishedContent schema extender
        schema = self.context.Schema()
        return schema['weeksLeftPublished'].get(self.context)

    @property
    def current_expiry(self):
        return self.context.getExpirationDate().strftime("%A, %e %B, at %I:%M%P")

    @property
    def current_credit(self):
        """stub"""
        return self.cr.queryCredit(self.pmt.getAuthenticatedMember().getId(), IOneWeekPublishedCredit.__identifier__)

    @property
    def weeks_options(self):
        """stub"""
        ret = []
        # If it's not currently published, weeks starts at least at 1, if it's already
        # listed, they should be able to set the remaining weeks to 0
        start = not self.is_listed and 1 or 0
        for i in range(start, 53):
            ret.append({'value' : i, 'selected' : (i == self.current_weeks) and 'selected' or None})
        return ret

class AddForm(base.NullAddForm):

    def create(self):
        return Assignment()
