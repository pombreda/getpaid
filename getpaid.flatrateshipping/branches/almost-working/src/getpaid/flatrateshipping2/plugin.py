"""
$Id: $
"""

from zope import component, interface
from getpaid.core.interfaces import IPluginManager
from getpaid.flatrateshipping2 import interfaces 
from getpaid.flatrateshipping2 import rates

class FlatRatePlugin( object ):

    interface.implements( IPluginManager )
    
    title = "UPS Shipping Method"
    description = "Provides for realtime price estimation for shipping via UPS, requires a UPS account"
    
    def __init__(self, context ):
        self.context = context
        
    def install( self ):
        sm = self.context.getSiteManager()
        utility = sm.queryUtility( interfaces.IShippingRateService, name="flatrate")
        if utility is not None:
            return

        shipping_service = rates.MyShippingRateService()
         
        try:
            sm.registerUtility(component=shipping_service, provided=interfaces.IShippingRateService, name="flatrate" )
        except TypeError:
            # BBB for Zope 2.9
            sm.registerUtility(interface=interfaces.IFlatRateService, utility=shipping_service)
        
    def uninstall( self ):
        pass
        
    def status( self ):
        return component.queryUtility( interfaces.IShippingRateService, name="flatrate" ) is not None
        
def storeInstalled( object, event ):
    return FlatRatePlugin( object ).install()
