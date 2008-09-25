__author__ = """Darryl Dixon <darryl.dixon@winterhouseconsulting.com>"""

from zope.component import getUtility
from DateTime.DateTime import DateTime

from plone.app.layout.viewlets import ViewletBase

from cornerstone.browser.base import RequestMixin

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.WorkflowCore import WorkflowException

from getpaid.creditpublish.interfaces import IOneWeekPublishedCredit, IOneWeekCreditPublishedContent
from getpaid.creditregistry.interfaces import ICreditRegistry
from getpaid.creditpublish import creditpublishMessageFactory as _
from getpaid.creditpublish.security import invokeFunctionAsManager

class NoOneWeekPublishedCreditsViewlet(ViewletBase):
    """Notification viewlet for when the user is viewing credit published content
       but has no credit
    """

    def __init__(self, context, request, view, manager):
        super(NoOneWeekPublishedCreditsViewlet, self).__init__(context, request, view, manager)
        self.pmt = getToolByName(self.context, 'portal_membership')
        self.wft = getToolByName(self.context, 'portal_workflow')
        self.cr = getUtility(ICreditRegistry)
      
    @property
    def index(self):
        member_id = self.pmt.getAuthenticatedMember().getId()
        # They must not be anonymous, must not have any credit, the item must not be published, and they must be its creator
        if not self.pmt.isAnonymousUser() and \
           not self.cr.queryCredit(member_id, IOneWeekPublishedCredit.__identifier__) and \
           not (self.wft.getInfoFor(self.context, 'review_state') == 'published') and \
           (member_id == self.context.Creator()):
            return ViewPageTemplateFile("templates/viewlet_nooneweekpublishedcredits.pt")
        else:
            return lambda: ''

class OneWeekCreditPublishingViewlet(ViewletBase, RequestMixin):
    """Viewlet for controlling publish/depublish when credit is available
    """

    nameprefix = 'getpaid.creditpublishing'

    def __init__(self, context, request, view, manager):
        super(OneWeekCreditPublishingViewlet, self).__init__(context, request, view, manager)
        # XXX FIX THIS UP SO THAT WE USE THE VIRTUAL ROOT
        self.sitepath = '/'
        self.pmt = getToolByName(self.context, 'portal_membership')
        self.wft = getToolByName(self.context, 'portal_workflow')
        self.cr = getUtility(ICreditRegistry)

    @property
    def index(self):
        """What should this viewlet show?"""
        # Instead, we need to decide whether this Viewlet is relevant at all
        if IOneWeekCreditPublishedContent.providedBy(self.context):
            if not 'portal_factory' in self.request['ACTUAL_URL']:
                if self.user_is_creator:
                    # First decide if the user just POSTed us some data
                    # Technically, the status=302 lines below should be status=303, except that IE6
                    # FAILS IT EPICALLY when receiving a 303. Suck.
                    if self.request.get('REQUEST_METHOD', '') == 'POST':
                        # Find out if any of our settings were included in this
                        if self.formvalue('submitted') is not None:
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
                                return ViewPageTemplateFile('templates/confirmdepublish.pt')
                            elif self.formvalue('confirmdepublish'):
                                if not self.is_listed:
                                    # They've probably just tried refreshing the previously submitted
                                    # page. Better to just do nothing at this point
                                    pass
                                else:
                                    self.depublishContext()
                                    # The page has already rendered with self.context showing as 'published'
                                    self.request.RESPONSE.redirect(self.request['ACTUAL_URL'], status=302)
                    if self.current_credit:
                        # If they've got credit then show the portlet regardless
                        return self.correctTemplate()
                    else:
                        # Only show the portlet when they have no credit if the context
                        # is already published - they need to be able to choose to withdraw
                        # it if necessary
                        if self.is_listed:
                            # OK, so we will show it so they can withdraw if necessary
                            return self.correctTemplate()
                        else:
                            # They have no credit and the context isn't published - instead
                            # of showing this Viewlet, we will let a more prominent BeforeContentViewlet
                            # inform them of the situation, and they can use the creditpurchasing portlet
                            # to remedy
                            return lambda: ''
                else:
                    # User isn't creator
                    # XXX Probably this should be policy-pluggable - maybe people in the same group should
                    #     be able to publish each other's stuff?
                    return lambda: ''
            else:
                # The object is still being added right now
                return lambda: ''
        else:
            # Not a credit-published item
            return lambda: ''

    def correctTemplate(self):
        """Return the right ViewPageTemplateFile based on the current state of the context, etc
        """
        if self.is_listed:
            return ViewPageTemplateFile('templates/published.pt')
        else:
            return ViewPageTemplateFile('templates/unpublished.pt')


    def publishContext(self, weeks, update=False):
        """Perform the various policy-steps necessary when publishing this context"""
        schema = self.context.Schema()
        if update:
            schema['republishReminderSent'].set(self.context, False)
            schema['weeksLeftPublished'].set(self.context, weeks)
        elif self.current_credit:
            try:
                invokeFunctionAsManager(self.request, self.wft.doActionFor, self.context, 'publish') 
            except WorkflowException, e:
                # Ok, basically this means there isn't a way to make this item 'published'.
                # Possibly, this is because it already *is*. Because the site admin has chosen
                # to make this content type purchasable, we will assume the reason we can't publish
                # it is because it is already published. Lets find out:
                state = self.wft.getInfoFor(self.context, 'review_state')
                if state != 'published':
                    # Log an error and bail: 
                    self.context.plone_log("Unable to publish: %s, current state is: %s" % (self.context.getPhysicalPath(), state))
                    raise
                else:
                    # Our work here is complete:
                    pass
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
