from Acquisition import aq_base

from interfaces import IOneWeekCreditPublishedContent

def getWeeksLeftPublished(object, portal, **kwargs):
    """Index the atschemaextender attribute"""
    object = aq_base(object)
    if IOneWeekCreditPublishedContent.providedBy(object):
        return object.Schema()['weeksLeftPublished'].get(object)
    else:
        return None

def getRepublishReminderSent(object, portal, **kwargs):
    """Index the atschemaextender attribute"""
    object = aq_base(object)
    if IOneWeekCreditPublishedContent.providedBy(object):
        return object.Schema()['republishReminderSent'].get(object)
    else:
        return None
