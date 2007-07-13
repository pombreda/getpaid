"""
$Id$
"""

from zope.interface import implements
from zope.app.event.objectevent import ObjectEvent

import interfaces

class PayableCreationEvent( ObjectEvent ):

    implements( interfaces.IPayableCreationEvent )
    
    def __init__( self, object, payable, payable_interface ):
        super( PayableCreationEvent, self).__init__( object )
        self.payable = payable
        self.payable_interface = payable_interface

