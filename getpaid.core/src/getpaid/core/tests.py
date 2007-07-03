"""Doc test runner
"""

__docformat__ = "reStructuredText"

import doctest
import unittest
from zope.testing.doctestunit import DocFileSuite
from zope.app.testing import placelesssetup, ztapi
from zope.app.annotation import interfaces as annotation_interfaces
from zope.app.annotation import attribute

from hurry.workflow import interfaces

import random, string, datetime

from zope import component

from getpaid.core.interfaces import IOrder, IOrderManager, finance_states
from getpaid.core import order, cart
from getpaid.core.workflow import order as oworkflow

def setUp(test):
    return
    
def tearDown(test):
    return


def createOrders( how_many=10 ):
    manager = component.getUtility( IOrderManager )

    for i in range(1, how_many):
        o = order.Order()
        o.order_id = str(i)

        o.shopping_cart = sc = cart.ShoppingCart()
        
        for i in range(0, 10):
            item = cart.LineItem()
            item.name = "p%s"%random.choice( string.letters )
            item.quantity = random.randint(1,25)
            item.cost = random.randint(30, 100)
            item.item_id = "i%s"%random.choice( string.letters )
            if item.item_id in sc:
                continue
            sc[item.item_id] = item
            
        o.user_id = "u%s"%random.choice( string.letters )
        o.finance_workflow.fireTransition('create')
        o.fulfillment_workflow.fireTransition('create')
        
        manager.store( o )

        yield o

class OrderQueryTests( unittest.TestCase ):

    def setUp( self ):
        placelesssetup.setUp()
        workflowSetUp( None )
        self.orders = list( createOrders() )
        self.manager = component.getUtility( IOrderManager )
        
    def tearDown( self ):
        placelesssetup.tearDown()
        self.orders = None
        self.manager = None
        
    def testDateQuery( self ):
        self.orders[0].creation_date = datetime.datetime.now() - datetime.timedelta( 30 )
        self.manager.storage.reindex( self.orders[0] )
        
        self.orders[1].creation_date = datetime.datetime.now() - datetime.timedelta( 120 )
        self.manager.storage.reindex( self.orders[1] )

        # find orders in the last week
        results = order.query.search( creation_date = datetime.timedelta(7)  )
        self.assertEqual( len(results), 7 )
        
        now = datetime.datetime.now()
        start_date = now - datetime.timedelta( 125 )
        end_date = now - datetime.timedelta( 7 )
        results = order.query.search( creation_date = ( start_date, end_date ) )
        self.assertEqual( len(results), 2 )
        

    def testStateQuery( self ):
        self.orders[0].finance_workflow.fireTransition('authorize')
        self.manager.storage.reindex( self.orders[0] )        
        
        self.orders[1].finance_workflow.fireTransition('authorize')
        self.orders[1].finance_workflow.fireTransition('cancel-chargeable')        
        self.manager.storage.reindex( self.orders[1] )

        self.orders[2].finance_workflow.fireTransition('authorize')
        self.orders[2].finance_workflow.fireTransition('charge-chargeable') 
        self.manager.storage.reindex( self.orders[2] )
        
        self.assertEqual( len( order.query.search( finance_state = finance_states.CHARGEABLE ) ), 1 )
        self.assertEqual( len( order.query.search( finance_state = finance_states.CANCELLED ) ), 1 )
        self.assertEqual( len( order.query.search( finance_state = finance_states.CHARGED ) ), 1 )                

    def testCombinedQuery( self ):
        self.orders[0].finance_workflow.fireTransition('authorize')
        self.orders[0].creation_date = created = datetime.datetime.now() - datetime.timedelta( 30 )
        self.manager.storage.reindex( self.orders[0] )
        self.assertEqual( len( order.query.search( finance_state = finance_states.CHARGEABLE,
                                                   creation_date = ( created - datetime.timedelta(1),
                                                                     created + datetime.timedelta(1) )
                                                   )),
                          1
                          )
        
    
def workflowSetUp(doctest):
    placelesssetup.setUp()

    ztapi.provideAdapter( IOrder,
                          interfaces.IWorkflowState,
                          oworkflow.FinanceState,
                         'getpaid.finance.state')

    ztapi.provideAdapter( IOrder,
                       interfaces.IWorkflowState,
                       oworkflow.FulfillmentState,
                      'getpaid.fulfillment.state')

    ztapi.provideAdapter( IOrder,
                     interfaces.IWorkflowInfo,
                     oworkflow.FinanceInfo,
                    'getpaid.finance.info')

    ztapi.provideAdapter( IOrder,
                     interfaces.IWorkflowInfo,
                     oworkflow.FulfillmentInfo,
                    'getpaid.fulfillment.info')
                    
    ztapi.provideAdapter(annotation_interfaces.IAttributeAnnotatable,
                         annotation_interfaces.IAnnotations,
                         attribute.AttributeAnnotations)

    ztapi.provideUtility(interfaces.IWorkflow,
                         oworkflow.FulfillmentWorkflow(),
                        'getpaid.fulfillment.workflow')
                        
    ztapi.provideUtility(interfaces.IWorkflow,
                        oworkflow.FinanceWorkflow(),
                        'getpaid.finance.workflow')

    ztapi.provideUtility(interfaces.IWorkflowVersions,
                         oworkflow.OrderVersions())
    
    ztapi.provideUtility( IOrderManager, order.OrderManager() )
    

def test_suite():
    return unittest.TestSuite((
        DocFileSuite('order.txt',
                     setUp=workflowSetUp,
                     tearDown=tearDown,
                     optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
                     ),
        unittest.makeSuite( OrderQueryTests ),
        ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
