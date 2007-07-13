"""
$Id$
"""

from zope.app.container.ordered import OrderedContainer
from zope.interface import implements
from persistent import Persistent

import interfaces

# backwards compatiblity - remove after next release - 7/5/2007
from item import LineItem

class ShoppingCart( OrderedContainer ):
    """
    A shopping cart
    """
    implements( interfaces.IShoppingCart )


