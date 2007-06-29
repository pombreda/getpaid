
from Products.Five.viewlet import manager, viewlet
from Products.Five.formlib.formbase import FormBase, SubPageForm
from Products.PloneGetPaid import interfaces
from zope import component

import os

_prefix = os.path.dirname( __file__ )

## GetPaidManagementTemplate = os.path.join( _prefix, "templates", "admin_viewlet.pt")

## ManagementViewletManager = manager.ViewletManager( "ManagementViewletManager",
##                                                    interfaces.IGetPaidManageViewletManager,
##                                                    GetPaidManagementTemplate )


GetPaidShoppingCartTemplate = os.path.join( _prefix, "templates", "cart-viewlet-manager.pt")

class ViewletManagerShoppingCart( object ):
    """ Shopping Cart Viewlet Manager """

    # for debugging
    #def update( self ):
    #    super( ViewletManagerShoppingCart, self ).update()

    def sort (self, viewlets ):
        """ sort by name """
        return sorted(viewlets)
        
ShoppingCartManager = manager.ViewletManager( "ShoppingCart",
                                              interfaces.IGetPaidCartViewletManager,
                                              GetPaidShoppingCartTemplate,
                                              bases=(ViewletManagerShoppingCart,)
                                              )

GetPaidContentWidgetsTemplate = os.path.join( _prefix, "templates", "contentwidget-viewlet-manager.pt")

class ViewletManagerContent( object ):
    """ Content Widget Viewlet Manager """

    def __init__( self, *args, **kw):
        super( ViewletManagerContent, self).__init__( *args, **kw)
        
        item_id = self.context.UID()

        found = False
        for marker, iface in interfaces.PayableMarkerMap.items():
            if marker.providedBy( self.context ):
                found = True
                break

        if not found:
            raise RuntimeError("Invalid Context For Cart Add")
        
        self.payable = component.getMultiAdapter( ( self.context, self.request ), iface )

    def sort (self, viewlets ):
        """ sort by name """
        return sorted(viewlets)
    
    def payableFields(self):
        return self.payable

ContentWidgetManager = manager.ViewletManager( "ContentViewManager",
                                              interfaces.IGetPaidContentViewletManager,
                                              GetPaidContentWidgetsTemplate,
                                              bases=(ViewletManagerContent,)
                                              )

class FormViewlet( viewlet.SimpleAttributeViewlet, SubPageForm ):
    """ a viewlet which utilize formlib
    """
    form_template = FormBase.template    
    renderForm = FormBase.render
    
    __page_attribute__ = "template"
    
    def update( self ):
        super( viewlet.SimpleAttributeViewlet, self).update()
        super( SubPageForm, self).update()

