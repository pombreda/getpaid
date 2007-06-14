"""
Storage Handling Details for Member Information used by getpaid, default is as annotations on
member data objects, typically shipping and billing address.

how to show information for non current users

$Id$
"""
from AccessControl import getSecurityManager
from getpaid.core import interfaces
from getpaid.core.options import PersistentOptions
from zope import schema 

class _UserPaymentInformation( PersistentOptions ):

    annotation_key = None
    
    def __init__( self, context, member_id=None ):

        if member_id is None:
            member_id = getSecurityManager().getUser().getId()
        member = getToolByName( context, 'portal_membership' ).getMemberById( member_id )
        self.context = member

UserPaymentInformation = _UserPaymentInformation.wire( "UserPaymentInformation",
                                                       "getpaid.user.information",
                                                       interfaces.IBillingAddress )
                                                       
class AdminPaymentInformation( object ):

    def __init__( self, context ):
        self.context = context
        
    def storageForUser( self, user_id ):
        return UserPaymentInformation( self.context, user_id )
        


