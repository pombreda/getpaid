"""
$Id$
"""

from zope.app.container.ordered import OrderedContainer
#from zope.app.container.btree import BTreeContainer
from zope.interface import implements
from persistent import Persistent

import interfaces

class LineItem( Persistent ):
    """
    an item in the cart
    """
    implements( interfaces.ILineItem )

    name = ""
    description = ""
    quantity = 0
    cost = 0
    
class PayableLineItem( Persistent ):
    """
    an item in the cart for a payable
    """
    implements( interfaces.IPayableLineItem )

class ShoppingCart( OrderedContainer ):
    """
    A shopping cart
    """
    implements( interfaces.IShoppingCart )


