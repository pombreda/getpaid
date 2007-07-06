"""

$Id$
"""

from persistent import Persistent

from zope.interface import implements
from zope import component
from zope.app.annotation.interfaces import IAttributeAnnotatable
from hurry.workflow.interfaces import IWorkflowState, IWorkflowInfo
from getpaid.core import interfaces


class LineItem( Persistent ):
    """
    an item in the cart

    lineitems are not generically attribute annotatable, which typically requires
    zodb persistence, instead to enable storage in other mediums, we use a specific
    limited set of components that use annotations on line items, specifically the
    workflow engine to enable fulfillment workflows on individual items.
    """
    implements( interfaces.ILineItem, IAttributeAnnotatable )

    name = ""
    description = ""
    quantity = 0
    cost = 0

    @property
    def fulfillment_state( self ):
        return IWorkflowState( self ).getState()

    @property
    def fulfillment_workflow( self ):
        return IWorkflowInfo( self )

    
class PayableLineItem( LineItem ):
    """
    an item in the cart for a payable
    """
    implements( interfaces.IPayableLineItem )
