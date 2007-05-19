
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

class ViewletManagerDebug( object ):
    """ mixin for debugging a viewlet manager """
    
    def update( self ):
        super( ViewletManagerDebug, self ).update()

        
ShoppingCartManager = manager.ViewletManager( "ShoppingCart",
                                              interfaces.IGetPaidCartViewletManager,
                                              GetPaidShoppingCartTemplate,
                                              bases=(ViewletManagerDebug,)
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

