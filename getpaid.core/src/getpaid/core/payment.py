"""

workflow event driven payment processor integration
"""

from getpaid.core import interfaces
from zope import component

def fireAutomaticTransitions( order, event ):
    """ fire automatic transitions for a new state """
    order.finance_workflow.fireAutomatic()


def processorWorkflowSubscriber( order, event ):
    """
    fire off transition from charging to charged or declined based on
    payment processor interaction.
    """

    if order.finance_state == event.destination:
        adapter = component.queryMultiAdapter( interfaces.IWorkflowPaymentProcessorIntegration,
                                               (order, order.finance_workflow) )

    elif order.fulfillment_state == event.fulfillment_state:
        adapter = component.queryMultiAdapter( interfaces.IWorkflowPaymentProcessorIntegration,
                                               (order, order.fulfillment_workflow ) )

    if adapter is None:
        return

    return adapter( event )

class DefaultFinanceProcessorIntegration( object ):

    def __init__( self, order, workflow):
        self.order = order
        self.workflow = workflow

    def __call__( self, event ):
        if event.destination != interfaces.workflow_states.order.finance.CHARGING:
            return

        # ick.. get a hold of the store
        # this is a little gross, we need some access to context, so we fetch line items
        # till we find something that resolves to an object, and try to get the store from that
        #
        context = component.queryUtility( interfaces.IStore )
        if context is None:
            from Products.CMFCore.utils import getToolByName
            ob = None
            for i in self.order.shopping_cart.values():
                if interfaces.IPayableLineItem.providedBy( i ):
                    ob = i.resolve()
            if ob is None:
                raise AttributeError("can't get store, TODO - please switch processors settings to utility adapters")
            context = getToolByName( ob, 'portal_url').getPortalObject()

        processor = component.getAdapter( context,
                                          interfaces.IPaymentProcessor,
                                          order.processor_id )

        result = processor.capture( order, order.getTotalPrice() )

        if result == interfaces.keys.results_async:
            return
        elif result == interfaces.keys.results_success:
            self.workflow.fireTransition('charge-charging')
        else:
            self.workflow.fireTransition('decline-charging', comment=result)
