"""
Content Control

$Id$
"""

import getpaid.core.interfaces as igetpaid

from zope.formlib import form
from zope import component, event

from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.Five.formlib import formbase
from Products.Five.utilities import marker
from Products.PloneGetPaid import interfaces
from base import BaseView, BaseFormView

class PayableFormView( BaseFormView ):

    adapters = None
    interface = None
    marker = None
    form_fields = form.FormFields()
    template = ZopeTwoPageTemplateFile('templates/content-template.pt')

class PayableForm( PayableFormView, PayableFormView, formbase.EditForm ): pass

class PayableCreation( PayableForm ): 

    _keep_marker = False
    
    @form.action("Activate", condition=form.haveInputWidgets)
    def activate_payable( self, action, data):
        self.handle_edit_action( action, data )
        self._keep_marker = True
    
    @form.action("Cancel")
    def handle_cancel( self, action, data):
        marker.erase( self.context, self.marker )
        self.request.RESPONSE.redirect( self.context.absolute_url() ) 

    def update( self ):
        marker.mark( self.context, self.marker)
        try:
            return super( PayableCreation, self).update()
        finally:
            if not self._keep_marker:
                marker.erase( self.context, self.marker )

class PayableDestruction( BrowserView ):
    
    def __call__(self):
        marker.erase( self.context, self.marker )
        self.request.RESPONSE.redirect( self.context.absolute_url() )


class BuyableForm( PayableForm ):
    form_fields = form.Fields( igetpaid.IBuyableContent )
    interface = igetpaid.IBuyableContent
    marker = interfaces.IBuyableMarker
    
class BuyableCreation( BuyableForm ): pass
class BuyableEdit( BuyableForm ): pass
class BuyableDestruction( PayableDestruction ): pass

    
class ShippableForm( PayableForm ):
    """ shippable content operations """
    form_fields = form.Fields( igetpaid.IShippableContent )
    interface = igetpaid.IShippableContent
    marker = interfaces.IShippableMarker
    
class ShippableCreation( ShippableForm ): pass
class ShippableEdit( ShippableForm ): pass
class ShippableDestruction( PayableDestruction ): pass

    
class PremiumForm( PayableForm ):
    """ premium content operations """
    form_fields = form.Fields( igetpaid.IPremiumContent )
    interface = igetpaid.IPremiumContent
    marker = interfaces.IPremiumMarker

class PremiumCreation( PremiumForm ): pass
class PremiumEdit( PremiumForm ): pass
class PremiumDestruction( PayableDestruction ): pass

    
class DonateForm( PayableForm ):
    """ donation operations """
    form_fields = form.Fields( igetpaid.IDonationContent )
    interface = igetpaid.IDonationContent
    marker = interfaces.IDonatableMarker

class DonateCreation( DonateForm ): pass
class DonateEdit( DonateForm ): pass
class DonateDestruction( PayableDestruction ): pass


class ContentControl( BrowserView ):
    """ conditions for presenting various actions
    """

    __allow_access_to_unprotected_subobjects__ = 1
    __slots__ = ( 'context', 'request', 'options' )
    
    def __init__( self, context, request ):
        self.context = context
        self.request = request

        portal = getToolByName( self.context, 'portal_url').getPortalObject()
        options = interfaces.IGetPaidManagementOptions( portal )
        self.options = options

    def isPayable( self ):
        """ 
        """
        return interfaces.IPayableMarker.providedBy( self.context )

    isPayable.__roles__ = None

    def isBuyable( self ):
        """ 
        """
        return interfaces.IBuyableMarker.providedBy( self.context )

    isBuyable.__roles__ = None

    def isPremium( self ):
        """
        """
        return interfaces.IPremiumMarker.providedBy( self.context )

    isPremium.__roles__ = None

    def isShippable( self ):
        """
        """
        return interfaces.IShippableMarker.providedBy( self.context )
        
    isShippable.__roles__ = None

    def isDonatable( self ):
        """
        """
        return interfaces.IDonatableMarker.providedBy( self.context )
        
    isDonatable.__roles__ = None
        
    def allowChangePayable( self, types ):
        """
        """
        return not (types and not self.context.portal_type in types)
    allowChangePayable.__roles__ = None
    
    def allowMakeBuyable( self ):
        """  
        """
        return self.allowChangePayable(self.options.buyable_types) \
               and not self.isPayable()
    allowMakeBuyable.__roles__ = None
    
    def allowMakeNotBuyable( self ):
        """  
        """
        return self.allowChangePayable(self.options.buyable_types) \
               and self.isBuyable()
    allowMakeNotBuyable.__roles__ = None

    def allowMakeShippable( self ):
        """  
        """
        return self.allowChangePayable(self.options.shippable_types) \
               and not self.isPayable()
    allowMakeShippable.__roles__ = None
    
    def allowMakeNotShippable( self ):
        """  
        """
        return self.allowChangePayable(self.options.shippable_types) \
               and self.isShippable()
    allowMakeNotShippable.__roles__ = None

    def allowMakePremiumContent( self ):
        """  
        """
        return self.allowChangePayable(self.options.premium_types) \
               and not self.isPayable()
    allowMakePremiumContent.__roles__ = None
    
    def allowMakeNotPremiumContent( self ):
        """  
        """
        return self.allowChangePayable(self.options.premium_types) \
               and self.isPremium()
    allowMakeNotPremiumContent.__roles__ = None

    def allowMakeDonatable( self ):
        """  
        """
        return self.allowChangePayable(self.options.donate_types) \
               and not self.isPayable()
    allowMakeDonatable.__roles__ = None
    
    def allowMakeNotDonatable( self ):
        """  
        """
        return self.allowChangePayable(self.options.donate_types) \
               and self.isDonatable()
    allowMakeNotDonatable.__roles__ = None

    def showManageCart( self ):
        utility = component.getUtility( igetpaid.IShoppingCartUtility )
        return utility.get( self.context ) is not None
    showManageCart.__roles__ = None

class ContentPortlet( BrowserView ):
    """ View methods for the ContentPortlet """

    payable = None
    def __init__( self, *args, **kw):
        super( BrowserView, self).__init__( *args, **kw)

        found = False
        for marker, iface in interfaces.PayableMarkerMap.items():
            if marker.providedBy( self.context ):
                found = True
                break

        if found:
            self.payable = iface( self.context )

    def isPayable(self):
        return self.payable is not None
        
    def payableFields(self):
        return self.payable
