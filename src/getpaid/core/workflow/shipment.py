"""

note we should potentially expand this workflow to show typical elements from the physical shipment
workflow, waiting for pickup, delivery.. hmm.. actually better is just have a shipment status
field, which can be dynamically looked up via the shipping provider.

 transition : create
    state - new

 transition : charge 
    state - charging
    condition - (*)

 transition : charged
    source - chargig
    state - charged
    trigger - system

 transition : charge-declined
    state - 
 
 transition : ship-new
    state - shipped 
    condition - (*)
   
 transition : ship-charged (*)
    state - 
   shipped

 delivered

 (*) the viability of these transitions (conditions), depends on store settings for how to
     capture an order. ie. in a charge before ship model, shipments are first charged, then
     shipped, another might charge the entire order before fulfillment.

$Id$
"""

from zope.interface import implements

from hurry.workflow import interfaces as iworkflow
from hurry.workflow import workflow

from getpaid.core.interfaces import workflow_states
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('getpaid')

def CheckAuthorized( wf, context ):
    return True

def CheckCharged( wf, context ):
    return True

def create_shippment_workflow( ):

    ss = workflow_states.shipment

    transitions = []
    add = transitions.append
    
    add( workflow.Transition(
        transition_id = 'create',
        title=_(u'Create'),
        source = None,
        destination = ss.NEW
        ) )

    add( workflow.Transition(
        transition_id = 'charge',
        title=_(u"Charge"),
        source = ss.NEW,
        destination = ss.CHARGING
        ) )

    add( workflow.Transition(
        transition_id = 'declined',
        title = _(u'Declined'),
        source = ss.CHARGING,
        destination = ss.DECLINED,
        trigger = iworkflow.SYSTEM
        ) )
        
    add( workflow.Transition(
        transition_id = 'charge',
        title = _(u'Charged'),
        source = ss.CHARGING,
        destination = ss.CHARGED,
        trigger = iworkflow.SYSTEM
        ) )

    add( workflow.Transition(
        transition_id = 'already-charged-order',
        title = _(u'Order Charged'),
        condition = CheckCharged,
        trigger = iworkflow.AUTOMATIC,
        source = ss.NEW,
        destination = ss.CHARGED
        ) )

    add( workflow.Transition(
        transition_id = 'ship-charged',
        title = _(u'Ship'),
        source = ss.CHARGED,
        destination = ss.SHIPPED,
        ) )    

    add( workflow.Transition(
        transition_id = 'delivered',
        title = _(u'Delivered'),
        source = ss.SHIPPED,
        destination = ss.DELIVERED,
        trigger = iworkflow.SYSTEM
        ) )

    return transitions

class ShipmentWorkflow( workflow.Workflow ):

    def __init__( self ):
        super( ShipmentWorkflow, self).__init__( create_shippment_workflow() )

ShipmentWorkflowAdapter = workflow.AdaptedWorkflow( ShipmentWorkflow() )

if __name__ == '__main__':
    wf = ShipmentWorkflow()
    print wf.toDot()

