"""
$Id$
"""

_GETPAID_DEPENDENCIES_ = [ "ore.member", 'CMFonFive' ]

import os, sys
from Globals import package_home

lib_path = os.path.join( package_home( globals() ), 'lib' )
if os.path.exists( lib_path ):
    sys.path.append( lib_path )


