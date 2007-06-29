"""
order utility implementation
"""

from zope.interface import implements
from zope.app.container.btree import BTreeContainer

from zope import component
from zope.index.field import FieldIndex
from zope.index.keyword  import KeywordIndex
from persistent import Persistent
from persistent.dict import PersistentDict
from zope.app.annotation.interfaces import IAttributeAnnotatable

from BTrees.IFBTree import weightedIntersection, intersection
from hurry.workflow.interfaces import IWorkflowState, IWorkflowInfo

import decimal, datetime

from getpaid.core import interfaces

class Order( Persistent ):

    implements( interfaces.IOrder, IAttributeAnnotatable )

    _order_id = None
    shipping_address = None
    billing_address = None
    shopping_cart = None
    processor_order_id = None
    user_id = None
    creation_date = None

    def __init__( self ):
        self.creation_date = datetime.datetime.now()

    def getOrderId( self ):
        return self._order_id

    def setOrderId( self, order_id):
        if self._order_id is not None:
            raise SyntaxError("Order Id already set")
        if not order_id:
            raise TypeError("Invalid Order Id")
        self._order_id = order_id

    order = property( getOrderId, setOrderId )

    def getFinanceState( self ):
        return component.getAdapter( self, IWorkflowState, "getpaid.finance.state").getState()

    finance_state = property( getFinanceState )
    
    def getFulfillmentState( self ):
        return component.getAdapter( self, IWorkflowState, "getpaid.fulfillment.state").getState()

    fulfillment_state = property( getFulfillmentState )

    def getFinanceWorkflow( self ):
        return component.getAdapter( self, IWorkflowInfo, "getpaid.finance.info")

    finance_workflow = property( getFinanceWorkflow )

    def getFulfillmentWorkflow( self ):
        return component.getAdapter( self, IWorkflowInfo, "getpaid.fulfillment.info")

    fulfillment_workflow = property( getFulfillmentWorkflow )

    def getTotalPrice( self ):
        if not self.shopping_cart:
            return 0

        total = 0
        for item in self.shopping_cart.values():
            d = decimal.Decimal ( str(item.cost ) ) * item.quantity
            total += d

        shipping_method = component.getUtility( interfaces.IShippingMethod )
        total += shipping_method.getCost( self )

        tax_utility = component.getUtility( interfaces.ITaxUtility )
        total += tax_utility.getCost( self )
        
        return float( str( total ) )

class OrderQuery( object ):
    """
    simple query construction.. it might be problematic for other storages without collapsing
    sort clauses where possible. best to minimize any query combinations in the released product.
    """

    @staticmethod
    def search( data ):
        """ take a dictionary of key, value pairs, and based on available queries/indexes
        construct query and return results """
        results = None
        for term in [ 'finance_state',
                      'fulfillment_state',
                      'user_id',
                      'creation_date' ]:
            term_value = data.get( term )
            if term_value is None:
                continue
            
            term_results = getattr( query, term )( term_value )
            if term_results is None: # short circuit .. default and intersection
                return []
            if results is None:
                results = term_results
            else:
                results = query.merge( results, term_results )

        # actualize to order objects
        results = query.generate( results )
        
        # reverse sort on creation date
        return query.sort( results, 'creation_date', reverse=True )
    
    @staticmethod
    def generate( results ):
        """ used to actualize results from ifsets to 
        """
        manager = component.getUtility( interfaces.IOrderManager )
        return ResultSet( results, manager.storage )

    @staticmethod
    def sort( results, attribute, reverse=False ):
        results = list( results )
        results.sort( lambda x,y: cmp( getattr( x, attribute ), getattr( y, attribute ) ) )
        if reverse:
            results.reverse()
        return results

    @staticmethod
    def merge( *results  ):
        return reduce( intersection, [res for res in results if res is not None] )
    
    @staticmethod
    def latest( delta = None ):
        if not delta:
            delta = datetime.timedelta(7) 
        manager = component.getUtility( interfaces.IOrderManager )
        now = datetime.datetime.now()
        return manager.storage.apply( { 'creation_date':( now-delta, now ) } )

    creation_date = latest
    
    @staticmethod
    def finance_state( value ):
        manager = component.getUtility( interfaces.IOrderManager )
        return manager.storage.apply( { 'finance_state':( value, value ) } )
    
    @staticmethod
    def fufillment_state( value ):
        manager = component.getUtility( interfaces.IOrderManager )
        return manager.storage.apply( {'fufillment_state':( value, value ) } )        

    @staticmethod
    def products( *products ):
        manager = component.getUtility( interfaces.IOrderManager )
        return manager.storage.apply( {'products':products } )
    
    @staticmethod
    def user_id( value ):
        manager = component.getUtility( interfaces.IOrderManager )
        return manager.storage.apply( {'user_id':( value, value ) } )                

query = OrderQuery

class OrderManager( Persistent ):

    implements( interfaces.IOrderManager )
    
    def __init__( self ):
        self.storage = OrderStorage()

    def getOrdersByUser( self, user_id, **kw):
        return query.search(
            dict( user_id = user_id )
            )

    def store( self, order ):
        self.storage[ order.order_id ] = order
    
    def query( self, **kw ):
        return self.storage.query( **kw )

    def get( self, order_id ):
        return self.storage.get( order_id )

    #################################
    # junk for z2.9 / f 1.4
    def manage_fixupOwnershipAfterAdd(self, *args):
        return

    def manage_setLocalRoles( self, *args ):
        return 


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
        super( OrderStorage, self).__init__()
        self.indexes = PersistentDict( {
            'products' : KeywordIndex(),
            'user_id'  : FieldIndex(),
            'processor_order_id' : FieldIndex(),
            'finance_state'   : FieldIndex(),
            'fufillment_state' : FieldIndex(),
            'creation_date' : FieldIndex() 
            } )
        
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
        self.index( doc_id, object )

    def reset_index( self ):
        # reindex all orders
        for oid in self.keys():
            self.unindex( oid )
            order = self[ oid ]
            self.index( order )
            
    def index( self, order ):
        doc_id = int( order.order_id )
        for attr, index in self.indexes.items():
            value = getattr( object, attr, None)
            if callable( value ):
                value = value()
            if value is None:
                continue
            index.index_doc( doc_id, value )

    def unindex( self, order_id ):
        for index in self.indexes.values():
            index.unindex_doc( int(doc_id) )        
        
    def __delitem__( self, key ):
        super( OrderStorage, self).__delitem__( key )
        doc_id = int( key )
        self.unindex( doc_id )


