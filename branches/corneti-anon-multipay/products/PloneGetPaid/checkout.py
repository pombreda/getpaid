"""
Session based checkout info management.
"""

from zope.interface import implements

from Products.CMFCore.utils import getToolByName
from getpaid.core import interfaces, options
from Products.PloneGetPaid.interfaces import ICheckoutInfoUtility, IBuyerInfo, IBuyerMemberInfo, IBuyerTaxInfo, IAddressActions

SESSION_KEY = 'plonegetpaid.checkoutdetail'

class CheckoutInfo( options.PropertyBag ):
    pass

class CheckoutInfoUtility( object ):
    
    implements( ICheckoutInfoUtility )

    def get( self, context, create=False ):
        session_manager = getToolByName( context, 'session_data_manager')
        if not session_manager.hasSessionData() and not create:
            return None
        session = session_manager.getSessionData()
        if not session.has_key(SESSION_KEY):
            if create:
                member_tool =  getToolByName( context, 'portal_membership')
                member = member_tool.getAuthenticatedMember()
                #Initialize checkout info with relevant interfaces
                CheckoutInfo.initclass( IBuyerInfo )
                #TODO: IBuyerTaxInfo should be configurable from the control panel, not used ad the moment.
                #CheckoutInfo.initClass( IBuyerTaxInfo )
                CheckoutInfo.initclass( interfaces.IShippingAddress )
                CheckoutInfo.initclass( IAddressActions )
                CheckoutInfo.initclass( interfaces.IBillingAddress )
                session[SESSION_KEY] = checkout_info = CheckoutInfo()
                if member:
                    #TODO: after implementing additional member data storage (remember or possibly something simpler), 
                    # this block would automatically fill relevant checkout_info fields.
                    CheckoutInfo.full_name = member.getProperty('fullname')
                    CheckoutInfo.email = member.getProperty('email')
                else:
                    #Add member info to allow anonymous users to register on the store after a successfull checkout.
                    CheckoutInfo.initclass( IBuyerMemberInfo )
            else:
                return None
        return session[SESSION_KEY]
        
    def destroy( self, context ):
        session_manager = getToolByName( context, 'session_data_manager')
        if not session_manager.hasSessionData():
            return None
        session = session_manager.getSessionData()
        if not session.has_key(SESSION_KEY):
            return
        del session[SESSION_KEY]