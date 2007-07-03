"""
temporary module for sprint, fold back into admin.py

or better split admin.py into getpaid.admin

order administration
"""

import datetime, os, inspect

from zope.app.container.interfaces import IContainer, IOrderedContainer
from zope.app.traversing.interfaces import ITraversable, TraversalError
from zope import component, schema, interface
from zope.viewlet.interfaces import IViewlet
from zope.formlib import form

from zc.table import table, column
from ore.viewlet import core

from getpaid.core import interfaces
from getpaid.core.order import OrderQuery as query

from OFS.SimpleItem import SimpleItem
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.Five.viewlet import manager as viewlet_manager
from Products.Five.traversable import FiveTraversable

from Products.PloneGetPaid import interfaces as ipgp

from base import BaseView

def renderOrderId( item, formatter ):
    return '<a href="@@admin-manage-order/%s">%s</a>'%( item.order_id, item.order_id )

class AttrColumn( object ):

    def __init__(self, name):
        self.name = name
        
    def __call__( self, item, formatter ):
        value = getattr( item, self.name, '')
        if callable( value ):
            return value()
        return value

class DateColumn( AttrColumn ):

    def __call__( self, item, formatter ):
        value = super( DateColumn, self).__call__( item, formatter )
        return value.isoformat()

class OrderListingComponent( core.EventViewlet ):

    template = ZopeTwoPageTemplateFile('templates/orders-listing.pt')
    
    columns = [
        column.GetterColumn( title="Order Id", getter=renderOrderId ),
        column.GetterColumn( title="Status", getter=AttrColumn("finance_state") ),
        column.GetterColumn( title="Fufillment", getter=AttrColumn("fulfillment_state") ),
        column.GetterColumn( title="Price", getter=AttrColumn("getTotalPrice") ),
        column.GetterColumn( title="Created", getter=DateColumn("creation_date") )
        ]

    order = 3
    
    def render( self ):
        return self.template()
    
    def listing( self ):
        columns = self.columns
        values = self.manager.get('orders-search').results
        formatter = table.StandaloneFullFormatter( self.context,
                                                   self.request,
                                                   values,
                                                   prefix="form",
                                                   visible_column_names = [c.name for c in columns],
                                                   #sort_on = ( ('name', False)
                                                   columns = columns )
        formatter.cssClasses['table'] = 'listing'
        return formatter()
    
class OrderCSVComponent( core.ComponentViewlet ):

    template = ZopeTwoPageTemplateFile('templates/orders-export-csv.pt')
    
    order = 2
    
    def render( self ):
        return self.template()
    
    @form.action("Export Search", condition=form.haveInputWidgets)
    def export_search( self ):
        
        search = self.manager['order-search']
        listing = self.manager['order-listing']
        
        io = StringIO()
        writer = csv.writer( io )
        writer.writerow( [c.name for c in listing.columns ] )

        field_getters = []
        for column in listing.columns:
            if isinstance( column, AttrColumn ):
                field_getters.append( column.getter )
            else:
                field_getters.append( AttrColumn( c.name ) )
            
        for order in search.results:
            writer.writerow( [getter( order, None ) for getter in field_getters ] )

        # um.. send to user
        return io.getvalue()

def define( **kw ):
    kw['required'] = False
    return kw        

class OrderSearchComponent( core.ComponentViewlet ):

    form_template = ZopeTwoPageTemplateFile('templates/form.pt')
    template = ZopeTwoPageTemplateFile('templates/orders-search-filter.pt')

    order = 1
    
    date_search_order = (
        ("last 7 days", datetime.timedelta( 7 )),
        ("last month", datetime.timedelta( 30 )),
        ("last 3 months", datetime.timedelta( 90 )),
        ("last year", datetime.timedelta( 365 )),
        )

    date_search_map = dict( date_search_order )

    results = None
    filtered = False
    _finance_values = [ m[1] for m in inspect.getmembers( interfaces.finance_states ) if m[0].isupper() ]
    _fulfillment_values = [ m[1] for m in inspect.getmembers( interfaces.fulfillment_states ) if m[0].isupper() ]
    
    form_fields = form.Fields( 
        schema.Choice( **define( title=u"Created", __name__=u"creation_date",
                                 values=( [ d[0] for d in date_search_order ] ) ) ),
        schema.Choice( **define( title=u"Status", __name__=u"finance_state", values= _finance_values ) ),
        schema.Choice( **define( title=u"Fufillment", __name__=u"fulfillment_state", values= _fulfillment_values ) ),
        schema.TextLine( **define( title=u"User Id", __name__=u"user_id") ),
        )

    def setUpWidgets(self, ignore_request=False):
        self.adapters = {}
        self.widgets = form.setUpDataWidgets(
            self.form_fields, self.prefix, self.context, self.request,
            ignore_request=ignore_request
            )

    @form.action("Filter", condition=form.haveInputWidgets)
    def handle_filter_action( self, action, data ):
        if data.get('creation_date'):
            data['creation_date'] = self.date_search_map.get( data['creation_date'] )
        self.filtered = True
        self.results = query.search( data )

    def update( self ):
        super( OrderSearchComponent, self).update()
        if not self.filtered:
            self.results = query.search( {'creation_date' : datetime.timedelta(7) } )
            self.request.set('form.creation_date', 'last 7 days')
        if self.results is None:
            self.results = []
            
    def render( self ):
        return self.template()

    def renderMENOW( self ):
        return self.form_template()


class OrderAdminManagerBase( object ):

    viewlets_map = ()
    
    def sort (self, viewlets ):
        viewlets.sort( lambda x, y: cmp(x[1].order, y[1].order ) )
        return viewlets

    def get( self, name ):
        if name in self.viewlets_map:
            return self.viewlets_map[ name ]
        return None

    def update(self):
        """See zope.contentprovider.interfaces.IContentProvider"""
        self.__updated = True

        # Find all content providers for the region
        viewlets = component.getAdapters(
            (self.context, self.request, self.__parent__, self),
            IViewlet)

        viewlets = self.filter(viewlets)
        viewlets = self.sort(viewlets)
        self.viewlets_map = dict( viewlets )
        
        # Just use the viewlets from now on
        self.viewlets = [viewlet for name, viewlet in viewlets]

        # Update all viewlets
        [viewlet.update() for viewlet in self.viewlets]
        

OrdersAdminManager = viewlet_manager.ViewletManager(
    "OrdersAdmin",
    ipgp.IOrdersAdminManager,
    os.path.join( os.path.dirname( __file__ ),
                  "templates",
                  "viewlet-manager.pt"),
    bases=( OrderAdminManagerBase, )
    )
    

class ManageOrders( BrowserView ):
    # admin the collection of orders
    def __call__( self ):
        self.manager = OrdersAdminManager( self.context, self.request, self )
        self.manager.update()
        return super( ManageOrders, self).__call__()

_marker = object()

class TraversableWrapper( SimpleItem ):
    """ simple indeed
    """
    
    interface.implements( interfaces.IOrder )
    
    def __init__( self, object ):
        self.__object = object

    def __getattr__( self, name ):
        value =  getattr( self.__object, name, _marker )
        if value is not _marker:
            return value
        return super( TraversableWrapper, self).__getattr__( name )

class AdminOrder( BrowserView ):

    def __init__( self, context, request ):
        self.context = context
        self.request = request
    
class AdminOrderRoot( BrowserView, FiveTraversable ):

    interface.implements( ITraversable )
    
    def __init__( self, context, request ):
        self.context = context
        self.request = request

    def __bobo_traverse__( self, request, name ):
        value = getattr( self, name, _marker )
        if value is not _marker:
            return value
        manager = component.getUtility( interfaces.IOrderManager )
        order = manager.get( name )
        if order is None:
            raise AttributeError( name )
        return TraversableWrapper( order ).__of__( self.context )
    
    # admin a single order
    def __call__( self ):
        #self.manager = AdminOrderManager( self.context, self.request, self )
        #self.manager.update()
        return super( AdminOrderRoot, self).__call__()
    
        
