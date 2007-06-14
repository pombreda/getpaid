"""
order utility implementation
"""

from zope.interface import implements
from zope.app.container.btree import BTreeContainer

from zope.index.field import FieldIndex
from zope.index.keyword  import KeywordIndex
from persistent import Persistent

from getpaid.core.interfaces import IOrderManager
from BTrees.IFBTree import weightedIntersection

class OrderManager( Persistent ):

    implements( IOrderManager )
    
    def __init__( self ):
        self.storage = OrderStorage()

    def getOrdersByItem( self, item_id, **kw):
        return self.query( products = item_id, **kw )

    def getOrdersByUser( self, user_id, **kw):
        return self.query( user_id = user_id, **kw )

    def store( self, order ):
        self.storage[ order ] = order.
    
    def query( self, **kw ):
        return self.storage.query( **kw )

    def get( self, order_id ):
        return self.storage[ order_id ] 


class ResultSet:
    """Lazily accessed set of objects."""

    def __init__(self, uids, storage):
        self.uids = uids
        self.storage = storage

    def __len__(self):
        return len(self.uids)

    def __iter__(self):
        for uid in self.uids:
            yield self.storage[ str( uid ) ]

class OrderStorage( BTreeContainer ):

    def __init__( self ):
        super( OrderStorager, self).__init__()
        self.indexes = dict(
            'order_id' : FieldIndex(),
            'products' : KeywordIndex(),
            'user_id'  : FieldIndex(),
            'status'   : FieldIndex()
            )
        
    def query( self, **args ):
        results = self.apply( args )
        return ResultSet( results, self )

    def apply(self, query):
        results = []
        for index_name, index_query in query.items():
            index = self.indexes[index_name]
            r = index.apply(index_query)
            if r is None:
                continue
            if not r:
                # empty results
                return r
            results.append((len(r), r))

        if not results:
            # no applicable indexes, so catalog was not applicable
            return None

        results.sort() # order from smallest to largest

        _, result = results.pop(0)
        for _, r in results:
            _, result = weightedIntersection(result, r)

        return result
    
    def __setitem__( self, key, object):
        super( OrderStorage, self ).__setitem__( key, object )
        doc_id = int( key )
        
        for attr, index in self.indexes.items():
            value = getattr( object, attr, None)
            if callable( value ):
                value = value()
            if value is None:
                continue
            index.index_doc( doc_id, value )
        
    def __delitem__( self, key ):
        super( OrderStorage, self).__delitem__( key )
        doc_id = int( key )
        for index in self.indexes.values():
            index.unindex_doc( doc_id )
        
        

