"""
$Id$
"""

_GETPAID_DEPENDENCIES_ = [ "ore.member", 'CMFonFive' ]

import os, sys
from Globals import package_home

pkg_home = package_home( globals() )
lib_path = os.path.join( pkg_home, 'lib' )
if os.path.exists( lib_path ):
    sys.path.append( lib_path )


