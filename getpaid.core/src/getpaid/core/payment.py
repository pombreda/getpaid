"""

workflow event driven payment processor integration
"""

from getpaid.core import interfaces 
from zope import component

def fireAutomaticTransitions( order, event ):    
    """ fire automatic transitions for a new state """ 
    order.finance_workflow.fireAutomatic()

def handleCapture( order, event ):
    """
    fire off transition from charging to charged or declined based on
    payment processor interaction.
    """

    if event.destination != interfaces.workflow_states.order.finance.CHARGING:
        return
    
    # ick.. get a hold of the store
    from Products.CMFCore.utils import getToolByName
    ob = None
    for i in order.shopping_cart.values():
        if interfaces.IPayableLineItem.providedBy( i ):
            ob = i.resolve()
    if ob is None:
        raise AttributeError("can't get store, please switch processors settings to utility adapters")
    context = getToolByName( ob, 'portal_url').getPortalObject()
    
    # this is a little gross, we need some access to context, so we fetch line items
    # till we find something that resolves to an object, and try to get the store from that
    processor = component.getAdapter( context,
                                      interfaces.IPaymentProcessor,
                                      order.processor_id )

    result = processor.capture( order, order.getTotalPrice() )
    
    if result == interfaces.keys.results_async:
        return
    elif result == interfaces.keys.results_success:
        order.finance_workflow.fireTransition('charge-charging')
    else:
        order.finance_workflow.fireTransition('decline-charging', comment=result)