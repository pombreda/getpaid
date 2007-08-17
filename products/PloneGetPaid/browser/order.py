"""
Order Admin and Customer History

$Id$
"""
import os

from Products.Five.browser import BrowserView
from Products.Five.viewlet.manager import ViewletManager

from Products.PloneGetPaid import interfaces as ipgp

from zope import component
from zope.viewlet.interfaces import IViewlet

from getpaid.core.order import query
from getpaid.core import interfaces as igpc

# from getpaid.core.interfaces import IOrderManager
from AccessControl import getSecurityManager

class OrderHistoryManagerBase( object ):

    viewlets_map = ()

    def sort( self, viewlets ):
        return viewlets

    def get( self, name ):
        if name in self.viewlets_map:
            return self.viewlets_map[ name ]
        return None

    def update( self ):
        self.__updated = True
        # Find all content providers for the region
        viewlets = component.getAdapters(
            (self.context, self.request, self.__parent__, self),
            IViewlet)

        viewlets = self.filter(viewlets)
        viewlets = self.sort(viewlets)
        self.viewlets_map = dict( viewlets )

        # Just use the viewlets from now on
        self.viewlets = [viewlet for name, viewlet in viewlets]

        # Update all viewlets
        [viewlet.update() for viewlet in self.viewlets]

OrderHistoryManager = ViewletManager("OrderHistory",
                                     ipgp.IOrderHistoryManager,
                                     os.path.join( os.path.dirname( __file__ ),
                                                   "templates",
                                                   "viewlet-manager.pt"),
                                     bases=( OrderHistoryManagerBase, ))

class UserOrderHistory( BrowserView ):
    def __call__( self ):
        uid = getSecurityManager().getUser().getId()
        if not uid:
            self.request.response.redirect("login_form?came_from=@@getpaid-order-history")
            return ""
        self.manager = OrderHistoryManager( self.context, self.request, self )
        self.manager.update()
        return super( UserOrderHistory, self ).__call__()

class UserOrderHistoryComponent:
    def history( self ):
        # this sucks on many levels:
        #  - do I really need to go fish out my own uid? surely that
        #    is in the context somewhere
        #  - I should be using zc.table / yoma.batching, right?
        #  - does this really benefit from the additional complexity
        #    of being a viewlet?
        uid = getSecurityManager().getUser().getId()
        orders = []
        for order in query.search(user_id=uid):
            orders.append({'id': order.order_id,
                           'date': order.creation_date.strftime('%Y-%m-%d %H:%M'),
                           'finance_state': order.finance_state,
                           'fulfillment_state': order.fulfillment_state,
                           'log': tuple(igpc.IOrderWorkflowLog( order ))})
        return orders


    
#     def __call__( self ):
#         uid = getSecurityManager().getUser().getId()
#         if not uid:
#             self.request.response.redirect("login_form?came_from=@@getpaid-order-history")
#             return ""
#         return super(UserOrderHistory, self).__call__()
        
#     def getUserOrders( self ):
#         uid = getSecurityManager().getUser().getId()
#         order_manager  = component.getUtility( IOrderManager )
#         orders = order_manager.getOrdersByUser( uid )
#         return orders or []

# class OrderAdminListing( BrowserView ):

#     def getOrders( self ):
#         order_manager = component.getUtility( IOrderManager )
#         return list( order_manager.storage.values() )
    

