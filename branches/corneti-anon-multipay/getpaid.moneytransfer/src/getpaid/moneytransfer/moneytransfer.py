"""
"""
from zope import component
from zope import interface

from interfaces import IMoneyTransferStandardOptions
from interfaces import IMoneyTransferStandardProcessor

class MoneyTransferStandardProcessor( object ):
   
    interface.implements( IMoneyTransferStandardProcessor )

    options_interface = IMoneyTransferStandardOptions

    def __init__( self, context ):
        self.context = context

    def cart_post_button( self, cart ):
        options = IMoneyTransferStandardOptions( self.context )
        cartitems = []        
        raise "Not implemented"

    def authorize( self, order, payment ):
        raise "Not implemented"


