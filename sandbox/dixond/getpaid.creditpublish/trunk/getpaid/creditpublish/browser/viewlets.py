from zope.component import getUtility

from plone.app.layout.viewlets import ViewletBase

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

from getpaid.creditpublish.interfaces import IOneWeekPublishedCredit
from getpaid.creditregistry.interfaces import ICreditRegistry


class NoOneWeekPublishedCreditsViewlet(ViewletBase):
    """Notification viewlet for when the user is viewing credit published content
       but has no credit
    """

    render = ViewPageTemplateFile("viewlet_nooneweekpublishedcredits.pt")

    def __init__(self, context, request, view, manager):
        super(NoOneWeekPublishedCreditsViewlet, self).__init__(context, request, view, manager)
        self.pmt = getToolByName(self.context, 'portal_membership')
        self.wft = getToolByName(self.context, 'portal_workflow')
        self.cr = getUtility(ICreditRegistry)
      
    def update(self):
        self.current_credit = self.cr.queryCredit(self.pmt.getAuthenticatedMember().getId(), IOneWeekPublishedCredit.__identifier__)

    def show(self):
        self.current_credit = self.cr.queryCredit(self.pmt.getAuthenticatedMember().getId(), IOneWeekPublishedCredit.__identifier__)
        self.context.plone_log("Current credit is: %d" % self.current_credit)
        # They must not be anonymous, must not have any credit, the item must not be published, and they must be its creator
        return not self.pmt.isAnonymousUser() and \
               not self.current_credit and \
               not (self.wft.getInfoFor(self.context, 'review_state') == 'published') and \
               (self.pmt.getAuthenticatedMember().getId() == self.context.Creator())

