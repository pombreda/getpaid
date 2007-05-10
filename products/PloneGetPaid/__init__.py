"""
$Id$
"""

from Products.Archetypes.public import process_types, listTypes
from Products.CMFCore import utils, permissions as cmf_perms

import config

def initialize( context ):

    import content_types

    content_types, constructors, ftis = process_types(
        listTypes(config.PROJECTNAME),
        config.PROJECTNAME)

    utils.ContentInit(
        config.PROJECTNAME + ' Content',
        content_types      = content_types,
        permission         = cmf_perms.ManagePortal,
        extra_constructors = constructors,
        fti                = ftis,
        ).initialize(context)

    
