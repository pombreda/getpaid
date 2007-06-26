"""

extensions to hurry.workflow to allow for multiple workflows on an object

$Id$
"""


from hurry.workflow import interfaces as iworkflow
from hurry.workflow import workflow

from zope import component
from zope.component.interfaces import ObjectEvent
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent
from zope.security.management import getInteraction, NoInteraction
from zope.security.interfaces import Unauthorized
from hurry.workflow.interfaces import\
     InvalidTransitionError, ConditionFailedError


class MultiWorkflowState( workflow.WorkflowState ):
    # namespaced annotations for multiple workflows
    
    state_key = "getpaid.state"
    id_key = "getpaid.id"

    def setState( self, state ):
        if state != self.getState():
            IAnnotations(self.context)[ self.state_key ] = state

    def setId(self, id):
        # XXX catalog should be informed (or should it?)
        IAnnotations(self.context)[ self.id_key ] = id

    def getState(self):
        try:
            return IAnnotations(self.context)[ self.state_key ]
        except KeyError:
            return None    

    def getId(self):
        try:
            return IAnnotations(self.context)[ self.id_key ]
        except KeyError:
            return None
        
class MultiWorkflowInfo( workflow.WorkflowInfo ):
    # namespaced workflow info
    # DOES NOT ALLOW VERSIONS WORKFLOW 

    state_name = 'getpaid'
    workflow_name = 'getpaid'
    
    def fireTransition(self, transition_id, comment=None, side_effect=None,
                       check_security=True):

        state = component.getAdapter( self.context, iworkflow.IWorkflowState, self.state_name)
        wf = component.getUtility(IWorkflow, self.workflow_name)
        
        # this raises InvalidTransitionError if id is invalid for current state
        transition = wf.getTransition(state.getState(), transition_id)
        # check whether we may execute this workflow transition
        try:
            interaction = getInteraction()
        except NoInteraction:
            checkPermission = workflow.nullCheckPermission
        else:
            if check_security:
                checkPermission = interaction.checkPermission
            else:
                checkPermission = workflow.nullCheckPermission
        if not checkPermission(
            transition.permission, self.context):
            raise Unauthorized(self.context,
                               'transition: %s' % transition_id, 
                               transition.permission)
        # now make sure transition can still work in this context
        if not transition.condition(self, self.context):
            raise ConditionFailedError
        # perform action, return any result as new version
        result = transition.action(self, self.context)
        if result is not None:
            if transition.source is None:
                component.getAdapter( result, iworkflow.IWorkflowState, self.state_name).initialize()
                IWorkflowState(result).initialize()
            # stamp it with version
            state = component.getAdapter( result, iworkflow.IWorkflowState, self.state_name)
            state.setId( component.getAdapter( self.context, iworkflow.IWorkflowState, self.state_name).getId())
            
            # execute any side effect:
            if side_effect is not None:
                side_effect(result)
            event = WorkflowVersionTransitionEvent(result, self.context,
                                                   transition.source,
                                                   transition.destination,
                                                   transition, comment)
        else:
            if transition.source is None:
                component.getAdapter( self.context, iworkflow.IWorkflowState, self.state_name).initialize()
            # execute any side effect
            if side_effect is not None:
                side_effect(self.context)
            event = workflow.WorkflowTransitionEvent(self.context,
                                                     transition.source,
                                                     transition.destination,
                                                     transition, comment)
        # change state of context or new object
        state.setState(transition.destination)
        notify(event)
        # send modified event for original or new object
        if result is None:
            notify(ObjectModifiedEvent(self.context))
        else:
            notify(ObjectModifiedEvent(result))
        return result


    def getFireableTransitionIdsToward(self, state):
        wf = component.getUtility(iworkflow.IWorkflow, self.workflow_name)
        result = []
        for transition_id in self.getFireableTransitionIds():
            transition = wf.getTransitionById(transition_id)
            if transition.destination == state:
                result.append(transition_id)
        return result

    def _getTransitions(self, trigger):
        # retrieve all possible transitions from workflow utility
        wf = component.getUtility(iworkflow.IWorkflow, self.workflow_name)
        transitions = wf.getTransitions(
            component.getAdapter( self.context, iworkflow.IWorkflowState, self.state_name ).getState()
            )
        # now filter these transitions to retrieve all possible
        # transitions in this context, and return their ids
        return [transition for transition in transitions if
                transition.trigger == trigger]    
