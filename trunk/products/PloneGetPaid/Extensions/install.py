"""
$Id$
"""

from Products.Archetypes.Extensions.utils import installTypes
from Products.Archetypes.atapi import listTypes
from Products.CMFCore.utils import getToolByName
from Products.CMFCore import permissions as cmf_perms
from Products.PloneGetPaid.config import *
from StringIO import StringIO

from ore.member.interfaces import ISiteSchemaManager

def install_control_panel( self ):

    manage_ui= getToolByName( self, 'portal_controlpanel')

    manage_ui.addAction(
        id = "getpaid",
        name = "Commerce",
        action = "string:${portal_url}/@@manage-getpaid-overview",
        appId = "PloneGetPaid",
#        imageUrl = "",
        description = "Management Access to Commerce Backend",
        permission=cmf_perms.ManagePortal
        
        )

def uninstall_control_panel( self ):
    manage_ui= getToolByName( self, 'portal_controlpanel')
    manage_ui.unregisterApplication( "PloneGetPaid" )

def install_dependencies( self ):
    quickinstaller = self.portal_quickinstaller
    for dependency in DEPENDENCIES:
        quickinstaller.installProduct( dependency )    

def install_member_schemas( self ):
    manager = ISiteSchemaManager( self )
    schemas = manager.member_schemas
    for s in [u"BillingAddressMemberData", u"ShippingAddressMemberData"]:
        if not s in schemas:
            schemas.append( s )
    manager.member_schemas = schemas
    
def uninstall_member_schemas( self ):
    manager = ISiteSchemaManager( self )
    schemas = manager.member_schemas
    for s in [u"BillingAddressMemberData", u"ShippingAddressMemberData"]:
        if s in schemas:
            schemas.remove( s )
    manager.member_schemas = schemas
    
def install( self ):
    out = StringIO()

    print >> out, "Installing Dependencies"
    install_dependencies( self )
    
    print >> out, "Installing Control Panel"
    install_control_panel( self  )

    print >> out, "Installing Types"
    installTypes( self, out, listTypes( PROJECTNAME), PROJECTNAME )

    print >> out, "Installing Member Schemas"
    install_member_schemas( self )

    return out.getvalue()

def uninstall( self ):
    uninstall_control_panel( self )

    uninstall_member_schemas( self )
    
    return "Uninstalled"
        
    


    
