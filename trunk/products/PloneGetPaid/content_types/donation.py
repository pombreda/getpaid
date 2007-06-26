"""
$Id$
"""

from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.content.schemata import ATContentTypeSchema
from Products.Archetypes.atapi import *
from Products.PloneGetPaid.config import *
from Products.CMFCore import permissions

from zope.interface import implements

DonationSchema = ATContentTypeSchema.copy() + Schema( (

    TextField(
        name='donationText',
        allowable_content_types=('text/plain', 
            'text/structured', 
            'text/html', 
            'application/msword',),
        widget=RichWidget(
            label       = "Donation Description Text",
            description = """Describe the purpose of the donation.  
                Include any information the donor would need to understand their donation.""",
            label_msgid = 'PloneGetPaid_label_donationText',
            i18n_domain = 'PloneGetPaid',
        ),
        default_output_type='text/html'
    ),

    FixedPointField(
        name='donationAmount',
        widget=DecimalWidget(
            label             = "Donation Amount",
            description       = "Please enter the amount you wish to donate.",
            dollars_and_cents = "True",
            label_msgid       = 'PloneGetPaid_label_donationAmount',
            i18n_domain       = 'PloneGetPaid',
        )
    ),
    
    ) )

class Donation( ATCTContent ):
    """ A Donation Form """

    meta_type = portal_type = archetype_name = "Donation"
    schema = DonationSchema
    global_allow = False    # XXX DEPRECATING NEED FOR A SEPARATE DONATION OBJECT, SO DON'T ALLOW ONE TO ADD

    actions = (
        {'id':'view',
         'name' : 'view',
         'action' : 'string:${object_url}/@@view',
         'permissions' : permissions.View 
         },
        )
        


registerType( Donation, PROJECTNAME )
