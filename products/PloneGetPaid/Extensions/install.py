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


coci_actions = [

       ( dict(  id = 'getpaid_make_buyable',
                name = 'Make Buyable',
                action = 'string:$object_url/@@activate-buyable',
                category ='object_buttons',
                permission = "Modify portal content",
                condition = "python:path('object/@@getpaid_control').allowChangeBuyable()",
                visible = True ),
         "user.gif" ),

      ( dict(  id = 'getpaid_make_shippable',
                name = 'Make Shippable Product',
                action = 'string:$object_url/@@activate-shippable',
                category ='object_buttons',
                permission = "Modify portal content",
                condition = "python:path('object/@@getpaid_control').allowChangeShippable()",
                visible = True ),
         "user.gif" ),

      ( dict(  id = 'getpaid_make_premium',
                name = 'Make Premium Members Only',
                action = 'string:$object_url/@@activate-premium-content',
                category ='object_buttons',
                permission = "Modify portal content",
                condition = "python:path('object/@@getpaid_control').allowChangePremiumContent()",
                visible = True ),
         "user.gif" ),

      ( dict(  id = 'getpaid_manage_cart',
                name = 'Manage Cart',
                action = 'string:$object_url/@@getpaid-cart',
                category ='user',
                permission = "View",
                condition = "python:path('object/@@getpaid_control').showManageCart",
                visible = True ),
         None ),


        ]

def setup_actions( self ):
    actions = getToolByName( self, 'portal_actions')
    action_icons = getToolByName( self, 'portal_actionicons')
    
    for action, image in coci_actions:
        actions.addAction( **action )

        if not image:
            continue
        
        if action_icons.queryActionIcon( action['category'], action['id'], None) is None:
            action_icons.addActionIcon( action['category'],
                                        action['id'],
                                        image,
                                        action['name'] )

def install_control_panel( self ):

    manage_ui= getToolByName( self, 'portal_controlpanel')

    manage_ui.addAction(
        id = "getpaid",
        name = "Commerce",
        action = "string:${portal_url}/@@manage-getpaid-overview",
        appId = "PloneGetPaid",
        imageUrl = "++resource++getpaid.png",
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

def install_cart_portlet( self ):
    portal = self.portal_url.getPortalObject()
    right_slots = portal.getProperty('right_slots')
    if isinstance( right_slots, str):
        right_slots = right_slots.split('\n')
    else:
        right_slots = list( right_slots )
    right_slots.append('here/@@portlet-shopping-cart/index/macros/portlet')
    portal._updateProperty( 'right_slots', '\n'.join( right_slots ) )    

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

    print >> out, "Installing Cart Portlet"
    install_cart_portlet( self )

    print >> out, "Installing Actions"
    setup_actions( self )
    
    return out.getvalue()

def uninstall( self ):
    uninstall_control_panel( self )

    uninstall_member_schemas( self )

    return "Uninstalled"
        
    


    
