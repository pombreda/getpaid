"""
Order Admin and Customer History

$Id$
"""
from Products.Five.browser import BrowserView
from base import BaseView
from zope import component
from getpaid.core.interfaces import IOrderManager
from AccessControl import getSecurityManager

class UserOrderHistory( BaseView ):

    def getUserOrders( self ):
        uid = getSecurityManager().getUser().getId()
        order_manager  = component.getUtility( IOrderManager )
        orders = order_manager.getOrdersByUser( uid )
        return orders

class OrderAdminListing( BrowserView ):

    def getOrders( self ):
        order_manager = component.getUtility( IOrderManager )
        return list( order_manager.storage.values() )
    

        
