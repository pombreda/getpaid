from zope import component, interface
from getpaid.core.interfaces import IPluginManager, IPaymentProcessor

from getpaid.nullpayment import interfaces
from getpaid.nullpayment import null


class NullPaymentPluginManager( object ):
    """ A simple plugin manager, which  manages plugins as local persistent object """
    interface.implements( IPluginManager )

    title = "Testing Processor"
    description = "A dummy payment processor for testing purposes"

    def __init__( self, context ):
        self.context = context

    def install( self ):
        """ Create and register payment processor as local persistent utility """
        sm = self.context.getSiteManager()
        util = sm.queryUtility( IPaymentProcessor, name="nullpayment")
        if util is None:
            payment_processor = null.NullPaymentProcessor()
            sm.registerUtility(component=payment_processor, provided=IPaymentProcessor, name="nullpayment" )
        
    def uninstall( self ):
        """ Delete and unregister payment processor local persistent utility """
        sm = self.context.getSiteManager()
        util = sm.queryUtility( IPaymentProcessor, name="nullpayment" )
        if util is not None:
            sm.unregisterUtility(util, IPaymentProcessor, name="nullpayment" )
            del util # Requires successful transaction to be effective

    def status( self ):
        """ Return payment processor utility registration status """
        sm = self.context.getSiteManager()
        return sm.queryUtility( IPaymentProcessor, name="nullpayment" ) is not None

def storeInstalled( object, event ):
    """ Install at IStore Installation (e.g. when PloneGetPaid is installed) """
    return NullPaymentPluginManager( object ).install()
