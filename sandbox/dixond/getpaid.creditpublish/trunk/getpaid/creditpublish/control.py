from zope.interface import implements
from zope.component import getUtility
from ZODB.POSException import ConflictError
from zope.app.component.hooks import getSite

from Products.CMFCore.utils import getToolByName
from interfaces import IOneWeekCreditPublishedContent, IOneWeekPublishedCredit
from getpaid.creditregistry.interfaces import ICreditRegistry
from DateTime.DateTime import DateTime

def runChecks(event): 
    """This is the enforcer for time-based weekly publishing."""
    site = getSite()
    site.plone_log("getpaid.creditpublish: Running checks, site is: %s" % str(site))
    pct = getToolByName(site, 'portal_catalog')
    put = getToolByName(site, 'portal_url')
    pmt = getToolByName(site, 'portal_membership')
    wft = getToolByName(site, 'portal_workflow')
    mailhost = getToolByName(site, 'MailHost')
    cr = getUtility(ICreditRegistry)
    mfrom = site.get('email_from_address', '')
    mname = site.get('email_from_name', '')
    # Find everything that might need inspecting that expires in the next week:
    all_to_check = pct.unrestrictedSearchResults(object_provides=IOneWeekCreditPublishedContent.__identifier__,
                                                 review_state='published',
                                                 expires={'query' : [DateTime()+7], 'range' : 'max'},
                                                )
    for to_check in all_to_check:
        if to_check.expires.lessThan(DateTime()+1):
            # Expires within the next day
            if not to_check.getWeeksLeftPublished:
                # And they've got no more credit left assigned to it
                if not to_check.getRepublishReminderSent:
                    # And we haven't yet sent a reminder, so:
                    user = pmt.getMemberById(to_check.Creator)
                    mto = user.getProperty('email', '')
                    msubject = "Item about to expire: %s" % to_check.Title
                    msg = """
%s,

Your item '%s' will expire within the next day.

You can choose to extend its listing by logging on to %s.

regards,
%s
""" % (user.getProperty('fullname', ''), to_check.Title, put(), mname)
                    obj = to_check.getObject()
                    obj.Schema()['republishReminderSent'].set(obj, True)
                    obj.reindexObject(idxs=['getRepublishReminderSent'])
                    sendEmail(site, msg, mto, mfrom, msubject)
        elif to_check.expires.lessThan(DateTime()):
            # It has expired, but is still published. We must check if it still has weeks left
            if to_check.getWeeksLeftPublished:
                # We need to extend the expiry date and deduct some credit
                obj = to_check.getObject()
                schema = obj.Schema()
                if cr.queryCredit(to_check.Creator, IOneWeekPublishedCredit.__identifier__):
                    # Relist it
                    obj.setExpirationDate(to_check.expires + 7)
                    schema['weeksLeftPublished'].set(obj, schema['weeksLeftPublished'].get(obj) - 1)
                    cr.useCredit(to_check.Creator, IOneWeekPublishedCredit.__identifier__, 1)
                    obj.reindexObject(idxs=['expires', 'getWeeksLeftPublished'])
                    # Go to the next now
                    continue
                else:
                    # De-publish it and then email no credit
                    wft.doActionFor(obj, 'hide')
                    requested = schema['weeksLeftPublished'].get(obj)
                    schema['weeksLeftPublished'].set(obj, 0)
                    obj.reindexObject(idxs=['getWeeksLeftPublished', 'review_state'])
                    user = pmt.getMemberById(to_check.Creator)
                    mto = user.getProperty('email', '')
                    msubject = "Item expired: %s" % to_check.Title
                    msg = """
%s,

Your item '%s' has expired.

You requested that it continue to be listed for the next %d weeks, but you
currently do not have any credit available to continue listing it. You can log
on to %s and purchase credit to re-list it if you wish.

regards,
%s
""" % (user.getProperty('fullname', ''), to_check.Title, requested, put(), mname)
                    sendEmail(site, msg, mto, mfrom, msubject)
            else:
                # Time to delist - they have not requested that it continue any further
                wft.doActionFor(obj, 'hide')
                obj.reindexObject(idxs=['review_state'])
                user = pmt.getMemberById(to_check.Creator)
                mto = user.getProperty('email', '')
                msubject = "Item expired: %s" % to_check.Title
                msg = """
%s,

Your item '%s' has expired.

You can choose to re-list it by logging on to %s.

regards,
%s
""" % (user.getProperty('fullname', ''), to_check.Title, put(), mname)
                sendEmail(site, msg, mto, mfrom, msubject)
    site.plone_log("getpaid.creditpublish: Finished running checks")



def sendEmail(site, msg, mto, mfrom, msubject): 
    try:
        mailhost.send(msg, mto, mfrom, subject=msubject)
    except ConflictError, e:
        raise
    except Exception, e:
        site.plone_log('Threw an exception sending publish controller email, error was: %s, details are: %s' % (e.__class__, str(e)))


# OK, Items are published
# Items are expired:
#   1) Do they still want it to be published? AND
#   2) Do they still have credit?
#      Yes) ---> REPUBLISH
#      No) ---> EMAIL, DEPUBLISH
# Items are within a day of expiry
#   1) Do they want it to republish? (getWeeksLeft True)
#   2) Do they still have credit?
#      No) EMAIL 
# Items are still more than a day away from expiry
#    ---> Do nothing

