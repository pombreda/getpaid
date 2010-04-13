from zope import component, interface
from getpaid.core.interfaces import IPluginManager, IPaymentProcessor

from getpaid.nullpayment import interfaces
from getpaid.nullpayment import null

class NullPaymentPlugin( object ):

    interface.implements( IPluginManager )

    title = "Testing Processor"
    description = "A dummy payment processor for testing purposes"

    def __init__( self, context ):
        self.context = context

    def install( self ):
        sm = self.context.getSiteManager()
        utility = sm.queryUtility( IPaymentProcessor, name="nullpayment")
        if utility is not None:
            return
        
        payment_processor = null.NullPaymentProcessor()
        
        sm.registerUtility(component=payment_processor, provided=IPaymentProcessor, name="nullpayment" )
        
    def uninstall( self ):
        pass

    def status( self ):
        return component.queryUtility( IPaymentProcessor, name="nullpayment" ) is not None

def storeInstalled( object, event ):
    return NullPaymentPlugin( object ).install()
