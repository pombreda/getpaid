"""

the capture model


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
from getpaid.core.workflow import MultiWorkflowInfo, MultiWorkflowState

from hurry.workflow import interfaces as iworkflow
from hurry.workflow import workflow

from getpaid.core.interfaces import shippment_states

def create_shippment_workflow( ):

    ss = shippment_states

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
        source = ss.NEW
        target = ss.CHARGING
        ) )

    add( workflow.Transition(
        transition_id = 'declined',
        source = ss.CHARGING,
        target = ss.DECLINED
        ) )
        

    add( workflow.Transition(
        transition_id = 'charge',
        source = ss.CHARGING,
        target = ss.CHARGED,
        trigger = iworkflow.SYSTEM
        ) )

    add( workflow.Transition(
        transition_id = 'ship-new',
        source = ss.NEW,
        target = ss.SHIPPED,
        ) )

    add( workflow.Transition(
        transition_id = 'delivered',
        source = ss.SHIPPED,
        target = ss.DELIVERED,
        trigger = iworkflow.SYSTEM
        ) )

    return transitions

class ShipmentWorkflow( workflow.Workflow ):

    def __init__( self ):
        super( ShipmentWorkflow, self).__init__( create_shippment_workflow() )
         
if __name__ == '__main__':
    wf = ShippmentWorkflow()
    print wf.toDot()
    

    

    
