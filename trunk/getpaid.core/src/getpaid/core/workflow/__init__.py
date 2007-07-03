"""
$Id$
"""

from hurry.workflow import workflow
from cStringIO import StringIO

def toDot( self ):
    """
    export workflow as dot
    """
    io = StringIO()
    states = set()
    print >> io, "digraph workflow {"
    for state, transitions in self._sources.items():
        states.add( state )
        for tid, t in transitions.items():
            states.add(  t.destination )
            print >> io, '  %s -> %s [label="%s", color=red, labeldistance=5];'%(t.source, t.destination, t.transition_id )
            
    for state in states:
        print >> io, "  %s [shape=box ]; "%state
    print >> io, " }"

    return io.getvalue()


workflow.Workflow.toDot = toDot
