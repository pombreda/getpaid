import logging

from ZODB.POSException import ConflictError
from zope.component import getMultiAdapter, getUtility

from getpaid.creditregistry.interfaces import ICreditRegistry, ICreditRegistryItem

from interfaces import IPurchasableCreditLineItem

log = logging.getLogger('getpaid.purchasablecredits')

def handlePurchasableCreditPurchase(object, event):
    if event.destination == 'CHARGED':
        log.info('Charged event')
        cr = getUtility(ICreditRegistry)
        for item in object.shopping_cart.values():
            if IPurchasableCreditLineItem.providedBy(item):
                try:
                    # Basically, we want to adapt IOrder with IPurchasableCreditLineItem
                    credit_details = getMultiAdapter((object, item), ICreditRegistryItem)
                    cr.addCredit(credit_details.user_name,
                                 credit_details.credit_name,
                                 credit_details.credit_amount,
                                 define=True)
                except ConflictError, e:
                    raise
                except Exception, e:
                    # We absolutely must record a failure here. People get grumpy
                    # if their credit doesn't turn up.
                    log.info('Unable to process the credit for user: %s, processor_order_id: %s, processor_id: %s. Error is: %s, details were: %s' % (object.user_id,
                                                                                                                                                      object.processor_order_id,
                                                                                                                                                      object.processor_id,
                                                                                                                                                      e.__class__,
                                                                                                                                                      str(e)))
