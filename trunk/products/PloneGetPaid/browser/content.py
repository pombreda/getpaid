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
        
    def allowChangeBuyable( self ):
        """  
        """
        if not self.context.portal_type in self.options.buyable_types:
            return False
        elif self.isBuyable() or self.isPremium() or self.isShippable():
            return False
        return True

    allowChangeBuyable.__roles__ = None
    
    def allowChangeShippable( self ):
        if not self.context.portal_type in self.options.shippable_types:
            return False
        elif self.isBuyable() or self.isPremium() or self.isShippable():
            return False
        return True
    
    allowChangeShippable.__roles__ = None
    
    def allowChangePremiumContent( self ):
        if not self.context.portal_type in self.options.premium_types:
            return False
        elif self.isBuyable() or self.isPremium() or self.isShippable():
            return False
        return True
    allowChangePremiumContent.__roles__ = None


    def showManageCart( self ):
        utility = component.getUtility( igetpaid.IShoppingCartUtility )
        return utility.get( self.context ) is not None
    
    showManageCart.__roles__ = None

