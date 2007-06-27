
from Products.Five.viewlet import manager, viewlet
from Products.Five.formlib.formbase import FormBase, SubPageForm
from Products.PloneGetPaid import interfaces

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
        return sorted(viewlets)
        
ShoppingCartManager = manager.ViewletManager( "ShoppingCart",
                                              interfaces.IGetPaidCartViewletManager,
                                              GetPaidShoppingCartTemplate,
                                              bases=(ViewletManagerShoppingCart,)
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

