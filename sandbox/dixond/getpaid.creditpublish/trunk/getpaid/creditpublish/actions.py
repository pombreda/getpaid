import logging

from ZODB.POSException import ConflictError
from zope.component import getMultiAdapter, getUtility

from getpaid.core.interfaces import IPayableLineItem
from getpaid.creditregistry.interfaces import ICreditRegistry, ICreditRegistryItem

from zope.interface import alsoProvides, noLongerProvides
from zope.app.component.hooks import getSite
from Products.CMFCore.utils import getToolByName

from interfaces import IOneWeekPublishedCredit, IMonthlyMembershipCredit

log = logging.getLogger('getpaid.creditpublish')

def addOneWeekPublishedCreditPortlet(object, event):
    site = getSite()
    pct = getToolByName(site, 'portal_catalog')
    ro = pct.unrestrictedSearchResults(UID=object.representative_object)
    if ro:
        ro = ro[0].getObject()
        alsoProvides(ro, IOneWeekPublishedCredit)
        ro.reindexObject(idxs=['object_provides'])

def editOneWeekPublishedCreditPortlet(object, event):
    site = getSite()
    pct = getToolByName(site, 'portal_catalog')
    oro = pct.unrestrictedSearchResults(object_provides=IOneWeekPublishedCredit.__identifier__)
    ro = pct.unrestrictedSearchResults(UID=object.representative_object)
    if oro:
        oro = oro[0].getObject()
        noLongerProvides(oro, IOneWeekPublishedCredit)
        oro.reindexObject(idxs=['object_provides'])
    if ro:
	ro = ro[0].getObject()
        alsoProvides(ro, IOneWeekPublishedCredit)
        ro.reindexObject(idxs=['object_provides'])

def handleOneWeekPublishedCreditPurchase(object, event):
    order = object
    if event.destination == 'CHARGED':
        log.info('Charged event')
        cr = getUtility(ICreditRegistry)
        for item in order.shopping_cart.values():
            if IPayableLineItem.providedBy(item):
                payable = item.resolve()
                if IOneWeekPublishedCredit.providedBy(payable):
                    try:
                        # Basically, we want to adapt IOrder with IPurchasableCreditLineItem
                        credit_details = getMultiAdapter((order, item, payable), ICreditRegistryItem)
                        cr.addCredit(credit_details.user_name,
                                     credit_details.credit_name,
                                     credit_details.credit_amount,
                                     define=True)
                    except ConflictError, e:
                        raise
                    except Exception, e:
                        # We absolutely must record a failure here. People get grumpy
                        # if their credit doesn't turn up.
                        from traceback import format_exc
                        log.info('Unable to process the credit for user: %s, processor_order_id: %s, processor_id: %s. Traceback was: %s' % (order.user_id,
                                                                                                                                             order.processor_order_id,
                                                                                                                                             order.processor_id,
                                                                                                                                             format_exc(),))

def handleMonthlyMembershipCredit(object, event):
    order = object
    if event.destination == 'CHARGED':
        log.info('Charged event')
        cr = getUtility(ICreditRegistry)
        for item in order.shopping_cart.values():
            if IPayableLineItem.providedBy(item):
                payable = item.resolve()
                if IMonthlyMembershipCredit.providedBy(payable):
                    try:
                        # Basically, we want to adapt IOrder with IPurchasableCreditLineItem
                        credit_details = getMultiAdapter((order, item, payable), ICreditRegistryItem)
                        cr.addCredit(credit_details.user_name,
                                     credit_details.credit_name,
                                     credit_details.credit_amount,
                                     define=True)
                    except ConflictError, e:
                        raise
                    except Exception, e:
                        # We absolutely must record a failure here. People get grumpy
                        # if their credit doesn't turn up.
                        from traceback import format_exc
                        log.info('Unable to process the credit for user: %s, processor_order_id: %s, processor_id: %s. Traceback was: %s' % (order.user_id,
                                                                                                                                             order.processor_order_id,
                                                                                                                                             order.processor_id,
                                                                                                                                             format_exc(),))

