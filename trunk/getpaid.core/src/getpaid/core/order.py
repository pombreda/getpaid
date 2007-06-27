"""
order utility implementation
"""

from zope.interface import implements
from zope.app.container.btree import BTreeContainer

from zope import component
from zope.index.field import FieldIndex
from zope.index.keyword  import KeywordIndex
from persistent import Persistent
from zope.app.annotation.interfaces import IAttributeAnnotatable

from BTrees.IFBTree import weightedIntersection
from hurry.workflow.interfaces import IWorkflowState

import decimal

from getpaid.core import interfaces

class Order( Persistent ):

    implements( interfaces.IOrder, IAttributeAnnotatable )

    order_id = None
    shipping_address = None
    billing_address = None
    shopping_cart = None
    processor_order_id = None

    def getFinanceState( self ):
        return component.getAdapter( self, IWorkflowState, "getpaid.finance.state").getState()

    finance_state = property( getFinanceState )
    
    def getFulfillmentState( self ):
        return component.getAdapter( self, IWorkflowState, "getpaid.fulfillment.state").getState()

    fulfillment_state = property( getFulfillmentState )


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

    
class OrderManager( Persistent ):

    implements( interfaces.IOrderManager )
    
    def __init__( self ):
        self.storage = OrderStorage()

    def getOrdersByItem( self, item_id, **kw):
        return self.query( products = item_id, **kw )

    def getOrdersByUser( self, user_id, **kw):
        return self.query( user_id = user_id, **kw )

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
        self.indexes = {
            'order_id' : FieldIndex(),
            'products' : KeywordIndex(),
            'user_id'  : FieldIndex(),
            'processor_order_id' : FieldIndex(),
            'finance_state'   : FieldIndex(),
            'fufillment_state' : FieldIndex()
            }
        
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


