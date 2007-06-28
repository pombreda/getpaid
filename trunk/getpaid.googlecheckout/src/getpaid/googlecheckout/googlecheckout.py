"""
"""
from zope import component
from zope import interface

import gchecky.controller as gcontroller


class GoogleCheckoutProcessor( object ):
   
    implements( interfaces.IGoogleCheckoutProcessor )

    options_interface = interfaces.IGoogleCheckoutOptions

    def __init__( self, context ):
        self.context = context

    def authorize( self, order, payment ):
        options = interfaces.IGoogleCheckoutOptions( self.context )

        controller = gcontroller.Controller(options.merchant_id,
                                            options.merchant_key,
                                            options.server_url == 'Test')

        #controller.charge_order()
