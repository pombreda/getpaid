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

from getpaid.core.interfaces import shipment_states

def CheckAuthorized( wf, context ):
    return True

def CheckCharged( wf, context ):
    return True

def create_shippment_workflow( ):

    ss = shipment_states

    transitions = []
    add = transitions.append
    
    add( workflow.Transition(
        transition_id = 'create',
        title='Create',
        source = None,
        destination = ss.NEW
        ) )

    add( workflow.Transition(
        transition_id = 'charge',
        title="Charge",
        source = ss.NEW,
        destination = ss.CHARGING
        ) )

    add( workflow.Transition(
        transition_id = 'declined',
        title = 'Declined',
        source = ss.CHARGING,
        destination = ss.DECLINED,
        trigger = iworkflow.SYSTEM
        ) )
        
    add( workflow.Transition(
        transition_id = 'charge',
        title = 'Charged',
        source = ss.CHARGING,
        destination = ss.CHARGED,
        trigger = iworkflow.SYSTEM
        ) )

    add( workflow.Transition(
        transition_id = 'already-charged-order',
        title = 'Order Charged',
        condition = CheckCharged,
        trigger = iworkflow.AUTOMATIC,
        source = ss.NEW,
        destination = ss.CHARGED
        ) )

    add( workflow.Transition(
        transition_id = 'ship-charged',
        title = 'Ship',
        source = ss.CHARGED,
        destination = ss.SHIPPED,
        ) )    

    add( workflow.Transition(
        transition_id = 'delivered',
        title = 'Delivered',
        source = ss.SHIPPED,
        destination = ss.DELIVERED,
        trigger = iworkflow.SYSTEM
        ) )

    return transitions

class ShipmentWorkflow( workflow.Workflow ):

    def __init__( self ):
        super( ShipmentWorkflow, self).__init__( create_shippment_workflow() )
         
if __name__ == '__main__':
    wf = ShipmentWorkflow()
    print wf.toDot()
    

    

    
