from urllib2 import Request, urlopen, URLError
import logging
import elementtree.ElementTree as etree

from zope import interface, schema, component
from zope.app.container.contained import Contained
from persistent import Persistent
from zope.app.interface import queryType, providedBy

from Products.CMFCore.utils import getToolByName

from getpaid.core.interfaces import IShippableLineItem, IStoreSettings, IShippingMethodRate, IOriginRouter,IStore
from getpaid.flatrateshipping2.interfaces import IFlatRateService, IFlatRateSettings
from getpaid.flatrateshipping2.flatrate import FlatRateShippingAdapter


class MyResponse:
    """An object representing a response from me...mimic ups ... will contain status/error info and possibly a list of 
shipments"""
    shipments = []
    error = None


class MyShippingRateService ( Persistent, Contained ):
    """
    cf rates.py ups
    """
    interface.implements(IFlatRateService)
    options_interface = IFlatRateSettings

    def __init__( self ):
        # initialize defaults from schema
        for name, field in schema.getFields( IFlatRateSettings ).items():
            field.set( self, field.query( self, field.default ) )
        super( MyShippingRateService, self).__init__()


    def getRates( self, order ):
        """
        given an order object, return a set of shipping method rate objects
        for available shipping options, on error raises an exception.
        """
        # ick.. get a hold of the store
        # this is a little gross, we need some access to context
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


        FRSA = FlatRateShippingAdapter(context)
        
        temp_settings = IFlatRateSettings(context)
        option = temp_settings.flatrate_option
        flatrate = float(temp_settings.flatrate_flatrate)
        perc = temp_settings.flatrate_percentage
        maxi = temp_settings.flatrate_max
        
        shipments = []  # only one for me 
        shipment = ShippingMethodRate() # ShippingMethodRate a definir separement
        shipment.service_code = "01"
        shipment.service = "flat-rate"
        shipment.currency = "ZAR"
        shipment.cost = FRSA.getCost(order, option, flatrate, perc, maxi) # 

        shipments.append( shipment ) 
        my_response = MyResponse()
        my_response.shipments = shipments 
        return my_response

    def getMethodName(self, method_id ):
        """
        given a shipping method id, return the name of the method name
        """
        term = interfaces.MY_SHIPPING_SERVICES.getTerm( method_id )
        return term.title

    def getTrackingUrl( self, track_number ):
        """
        given a track number this should return, if available for this service
        a url that can be used to track the shipment
        """
        return None


class ShippingMethodRate( object ):
    """A Shipment Option and Price"""
    interface.implements( IShippingMethodRate )

    service_code = ""
    service = ""
    currency = ""
    cost = 10

    def __repr__( self ):
        return  "<My Shipping Method %s>"%(str(self.__dict__))
