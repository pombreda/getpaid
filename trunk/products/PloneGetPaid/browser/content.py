"""
Content Control

$Id$
"""

import getpaid.core.interfaces as igetpaid

from zope.formlib import form
from zope import component

from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.Five.formlib import formbase
from Products.Five.utilities import marker
from Products.PloneGetPaid import interfaces
from base import BaseView, BaseFormView

class PayableFormView( BaseFormView ):

    adapters = None
    interface = igetpaid.IPayable

    template = ZopeTwoPageTemplateFile('templates/content-template.pt')

    def update( self ):
        self.payable = component.getMultiAdapter( ( self.context, self.request ),
                                                    self.interface )
        self.adapters = { self.interface : self.payable,
                          igetpaid.IPayable : self.payable }
        return super( PayableFormView, self).update()
        
    def setUpWidgets( self, ignore_request=False ):
        self.adapters = self.adapters is not None and self.adapters or {}
        self.widgets = form.setUpEditWidgets(
            self.form_fields, self.prefix, self.context, self.request,
            adapters=self.adapters, ignore_request=ignore_request
            )

class PayableCreation( PayableFormView, formbase.EditForm ):

    form_fields = form.Fields( igetpaid.IPayable )
    marker = None
    
    def update( self ):
        # XXX should do this on form submit success only...
        marker.mark( self.context, self.marker )
        return super( PayableCreation, self).update()

class PayableEdit( PayableFormView, formbase.EditForm  ):
    
    form_fields = form.Fields( igetpaid.IPayable )

class BuyableCreation( PayableCreation ):

    form_fields = form.Fields( igetpaid.IBuyableContent )
    interface = igetpaid.IBuyableContent
    marker = interfaces.IBuyableMarker

class BuyableEdit( PayableEdit ):

    form_fields = form.Fields( igetpaid.IBuyableContent )    
    interface = igetpaid.IBuyableContent    
    
class ShippableCreation( PayableCreation ):

    form_fields = form.Fields( igetpaid.IShippableContent )
    interface = igetpaid.IShippableContent
    marker = interfaces.IShippableMarker
    
class ShippableEdit( PayableEdit ):

    form_fields = form.Fields( igetpaid.IShippableContent )
    interface = igetpaid.IShippableContent

class PremiumCreation( PayableCreation ):

    form_fields = form.Fields( igetpaid.IPremiumContent )
    interface = igetpaid.IPremiumContent
    marker = interfaces.IPremiumMarker
    
class PremiumEdit( PayableEdit ):
    
    form_fields = form.Fields( igetpaid.IPremiumContent )
    interface = igetpaid.IPremiumContent
    
class DonateCreation( PayableCreation ):

    form_fields = form.Fields( igetpaid.IDonationContent )
    interface = igetpaid.IDonationContent
    marker = interfaces.IDonatableMarker

class DonateEdit( PayableEdit ):

    form_fields = form.Fields( igetpaid.IDonationContent )    
    interface = igetpaid.IDonationContent 
    



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

