"""

order line item fulfillment

transition : create

   destination - new

transition : deliver-virtual

   source - new
   condition : not shippable
   state - delivered
   trigger : system

transition : ship

   source - new
   destination - processing

transition : cancel

   source - new
   state - cancelled

transition : cancel - processing

   source - processing
   state - cancelled
   condition - shipment not authorized
    
transition :  system - shipped

   source - processing
   state - shipped

transition : process return

   source - shipped
   state - return in progress
   condition - returnable
   option - restocking fee   
   generate - rma number

   -- returns are there own shipments with workflow ?

transition : received return
  source : return in progress
  condition :
  option : ? 


transition : refund-delievered

   condition : virtual delivery | or refundable
   source : delivered
   state : refund-processing

transition : refund-processed

   state : refunded
   source : refund-processing
   

$Id$
"""

from zope.interface import implements

from hurry.workflow import interfaces as iworkflow
from hurry.workflow import workflow

from getpaid.core.interfaces import item_states

def create_item_fulfillment_workflow( ):

    ss = shippment_states

    transitions = []
    add = transitions.append
    
    add( workflow.Transition(
        transition_id = 'create',
        title='Create',
        source = None,
        destination = ss.NEW
        ) )

class ItemWorkflow( workflow.Workflow ):
    pass


    
