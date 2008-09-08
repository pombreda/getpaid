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
            return ViewPageTemplateFile("viewlet_nooneweekpublishedcredits.pt")
        else:
            return lambda: ''
