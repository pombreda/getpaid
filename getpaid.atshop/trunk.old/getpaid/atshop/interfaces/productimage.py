from zope import schema
from zope.interface import Interface

from zope.app.container.constraints import contains
from zope.app.container.constraints import containers

from getpaid.atshop import atshopMessageFactory as _

class IProductImage(Interface):
    """Image associated withthe product"""
    
    # -*- schema definition goes here -*-
