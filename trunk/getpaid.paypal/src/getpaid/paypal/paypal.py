"""
"""
from zope import component
from zope import interface

from interfaces import IPaypalStandardOptions
from interfaces import IPaypalStandardProcessor

class PaypalStandardProcessor( object ):
   
    interface.implements( IPaypalStandardProcessor )

    options_interface = interfaces.IPaypalStandardOptions

    def __init__( self, context ):
        self.context = context

    def cart_post_button( self, cart ):
        return ""

    def authorize( self, order, payment ):
        pass
