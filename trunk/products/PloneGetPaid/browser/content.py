"""
Content Control

$Id$
"""

import getpaid.interfaces
import Products.ContentFlavors.interfaces

class ContentControl( object ):
    """ determines if we can 
    """

    def __init__( self, context, request ):
        self.context = context
        self.request = request

    def allowChangePremiumContent( self ):

        # if its already there then no
        if getpaid.interfaces.IPremiumContent.providedBy( self.context ):
            return False

        # must allow for content flavors
        if not Products.ContentFlavors.interfaces.IFlavorAware( self.context ):
            return False
            
        portal = getToolByName( self.context, 'portal_url').getPortalObject()
        

