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
$Id: null.py 1143 2007-12-31 02:16:19Z kapilt $
"""

from zope import interface, component
from getpaid.core import interfaces, options

from getpaid.flatrateshipping2.interfaces import IFlatRateSettings, IFlatRateService
from getpaid.flatrateshipping2 import interfaces as frinterfaces
from getpaid.flatrateshipping2.interfaces import _

from getpaid.core.interfaces import IShippableLineItem, IStore

FlatRateSettings = options.PersistentOptions.wire(
    "FlatRateSettings",
    "getpaid.flatrateshipping2",
    IFlatRateSettings
    )

class FlatRateShippingAdapter( object ):

    interface.implements( IFlatRateService, IFlatRateSettings )
    options_interface = IFlatRateSettings

    def __init__( context ):
        context = context
        
    def getCost( self, order ):
        context = component.queryUtility( IStore )
        if context is None:
            from Products.CMFCore.utils import getToolByName
            ob = None
            for i in order.shopping_cart.values():
                if IShippableLineItem.providedBy( i ):
                    ob = i.resolve()
            if ob is None:
                raise AttributeError("can't get store, TODO - please switch processors settings to utility adapters")
            context = getToolByName( ob, 'portal_url').getPortalObject()
            
        settings = self.options_interface(context)
        if(settings.flatrate_option != "Percentage"):
            return settings.flatrate_flatrate
        #else: # we're calculating the percentage
            #items = filter( IShippableLineItem.providedBy, order.shopping_cart.values() )
            #cost = 0
            #for item in items:
                #cost += item.cost
            #shipcost = cost * (perc / 100)
            #if shipcost > maxi:
                #shipcost = maxi
            #return shipcost
