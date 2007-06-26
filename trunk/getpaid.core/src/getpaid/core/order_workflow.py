"""

$Id$
"""

from hurry.workflow import interfaces as iworkflow
from hurry.workflow import workflow

from workflow import MultiWorkflowInfo, MultiWorkflowState


def create_fulfillment_workflow( ):

    fs = fulfillment_states

    transitions = []
    add = transitions.append

    add( workflow.Transition( transition_id = 'create',
                              title= 'Create',
                              source = None,
                              destination = fs.NEW ) )

    # needs condition on charged finance state..
    add( workflow.Transition( transition_id = 'process-order',
                              title = 'Process Order',
                              source = fs.NEW,
                              destination = fs.PROCESSING ) )

    add( workflow.Transition( transition_id = 'deliver-processing-order',
                              title = 'Process Order',
                              source = fs.PROCESSING,
                              destination = fs.DELIVERED ) )
    
    add( workflow.Transition( transition_id = 'cancel-order'
                              title = 'Will Not Deliver',
                              source = fs.PROCESSING,
                              trigger = iworkflow.SYSTEM,
                              destination = fs.WILL_NOT_DELIVER ) )


    add( workflow.Transition( transition_id = 'cancel-new-order' ,
                              title = 'Will Not Deliver',
                              source = fs.NEW,
                              destination = fs.WILL_NOT_DELIVER,
                              trigger = iworkflow.SYSTEM) )

    return transitions

def create_finance_workflow( ):

    fs = finance_states

    transitions = []
    add = transitions.append

    # REVIEWING
    add( workflow.Transition( transition_id = 'create',
                              title = 'Create',
                              source = None,
                              destination = fs.REVIEWING ) )

    # CHARGEABLE TRANSITIONS
    add( workflow.Transition( transition_id = 'charge-chargeable',
                              title = 'Charge Order',
                              source = fs.CHARGEABLE,
                              destination = fs.CHARGING ) )

    add( workflow.Transition( transition_id = 'cancel-chargeable',
                              title = 'Cancel Order',
                              source = fs.CHARGABLE,
                              destination = fs.CANCELLED ) )

    add( workflow.Transition( transition_id = 'authorize-chargeable',
                              title = 'Authorize Order',
                              source = fs.CHARGEABLE,
                              destination = fs.CHARGEABLE ) )

    # CHARGED TRANSITIONS
    add( workflow.Transition( transition_id = 'authorize-charged',
                              title = 'Authorize Order',
                              source = fs.CHARGED,
                              destination = fs.CHARGED ) )

    add( workflow.Transition( transition_id = 'refund-order',
                              title = 'Refund Order',
                              source = fs.CHARGED,
                              destination = fs.REFUNDED ) )

    add( workflow.Transition( transition_id = 'charge-charged',
                              title = 'Charge Order',
                              source = fs.CHARGED,
                              destination = fs.CHARGED ) )


    # PAYMENT DECLINED TRANSITIONS

    add( workflow.Transition( transition_id = 'cancel-declined',
                              title='Cancel Order',
                              source = fs.PAYMENT_DECLINED,
                              destination = fs.CANCELLED ) )

    # SYSTEM TRANSITIONS
    
    add( workflow.Transition( transition_id = 'processor-cancelled',
                              title = 'Processor Cancel',
                              source = fs.REVIEWING,
                              destination = fs.CANCELLED_BY_PROCESSOR,
                              trigger = iworkflow.SYSTEM, ) )

    return transitions



class FulfillmentWorkflow( workflow.Workflow ):

    def __init__( self ):
        super( FufillmentWorkflow, self).__init__( create_fulfilliment_workflow() )

class FinanceWorkflow( workflow.Workflow ):

    def __init__( self ):
        super( FinanceWorkflow, self).__init__( create_finance_workflow() )

class FulfillmentState( MultiWorkflowState ):

    state_key = 'getpaid.fulfillment.state'
    id_key = 'getpaid.fulfillment.id'

class FinanceState( MultiWorkflowState ):

    state_key = 'getpaid.finance.state'
    id_key = 'getpaid.finance.id'

class FufillmentInfo( MultiWorkflowInfo ):
    
    state_name = "getpaid.fulfillment"
    workflow_name = "getpaid.fulfillment.workflow"

class FinanceInfo( MultiWorkflowInfo ):
    
    state_name = "getpaid.finance"
    workflow_name = "getpaid.finance.workflow"

    
         
    
                                  
        
