# Copyright (c) 2007 ifPeople, Kapil Thangavelu, and Contributors
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

"""
$Id$
"""

import decimal

from zope import component
from zope.interface import implements

from zope.app.container.ordered import OrderedContainer

try:
    from zope.annotation.interfaces import IAttributeAnnotatable
    from zope.annotation.interfaces import IAnnotations
except ImportError:
    # BBB for Zope 2.9
    from zope.app.annotation.interfaces import IAttributeAnnotatable
    from zope.app.annotation.interfaces import IAnnotations

import interfaces

class ShoppingCart( OrderedContainer ):
    """
    A shopping cart
    """
    implements( interfaces.IShoppingCart, IAttributeAnnotatable )

    last_item = None

    def size( self ):
        return sum(i.quantity for i in self.values())

    def __setitem__( self, key, value ):
        super(ShoppingCart, self).__setitem__( key, value)
        self.last_item = key

    def __delitem__( self, key ):
        if not key in self:
            return
        super( ShoppingCart, self).__delitem__( key )
        if self.last_item == key:
            if len(self)>0:
                self.last_item = self.keys()[-1]
            else:
                self.last_item = None

class CartItemTotals( object ):

    implements( interfaces.ILineContainerTotals )

    def __init__( self, context, price_adjuster ):
        self.shopping_cart = context

        # _v_ for volatile
        self._v_price_adjuster = price_adjuster

    @property
    def price_adjuster(self):
        """
        Make sure that reference to price_adjuster is not stored in to the database.
        """
        if self._v_price_adjuster is None:
            self.doHack()

        return self._v_price_adjuster

    def doHack(self):
        """
        TODO XXX

        GetPaid order has been hardwired to have getTotals(). It is
        called without any context in many different places.
        Since we have no site context available, we cannot
        do things like managing taxes properly there.

        This hack is a solution to get a proper context for the order.
        However, all order code should be rewritten so that it uses
        external adapters with site context to extract price data from the order.

        ORDER MUST NOT MIX-IN WITH CartItemTotals INSTEAD IT SHOULD USE
        ADAPTER WITH SITE CONTEXT.
        """

        if self._v_price_adjuster is None:
            from zope.app.component.hooks import getSite
            site = getSite()
            assert site != None, "WELL IT DIDN'T WORK DID IT? NOW GO AND REWRITE GETPAID CORE"

            self._v_price_adjuster = interfaces.IPriceValueAdjuster(site)


    def getTotalPrice( self ):
        if not self.shopping_cart:
            return 0

        total = 0
        total += float(self.getSubTotalPrice())
        total += float(self.getShippingCost())
        total += self.getSalesTaxCost()

        return float( str( total ) )

    def getItemPrices(self):
        """

        @return: Iterable of tuples (item, tax free price)
        """

        for item in self.shopping_cart.values():
            d = decimal.Decimal ( str(item.cost ) ) * item.quantity
            price = float(d)
            tax_free_price = self.price_adjuster.getTaxFreePrice(price, item)
            yield (item, tax_free_price)

    def getSubTotalPrice( self ):

        if not self.shopping_cart:
            return 0
        total = 0
        for item, price in self.getItemPrices():
            total += price

        return total

    def getShippingCost( self ):
        if not interfaces.IShippableOrder.providedBy( self ):
            return 0
        return decimal.Decimal( str( self.shipping_cost ) )

    def getSalesTaxCost( self ):
        """ Return sales tax for the item. """
        total = 0
        for item, price in self.getItemPrices():
            tax = self.price_adjuster.getTax(price, item)
            total += tax
        return total

    def getTaxtCost(self):
        """
        Get sum of all taxes. Backwards compatibility method.
        """
        return self.getSalesTaxCost()
