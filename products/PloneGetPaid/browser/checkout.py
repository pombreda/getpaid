"""

cart-review checkout

$Id$
"""

"""
random notes

get order

 - create order [ entry points ]
 - dispatch on workflow state
 
Order Workflow

  - created
     - system invariant - make sure we don't create multiple orders from the same cart, need to create cart_id, retrieve order by user_id, cart_id
     - automatic ready
     
  - ready
     - user submit
     
  - pending
     - automatic declined     
     - automatic accepted
     
  - declined
     - user submit pending

  - accepted
     - admin submit processed
     
  - processed

  - re
  
  - status
  
allow linear progression

carry hidden to force transition to required, allow linear links to be used though

"""

import random, sys
from cPickle import loads, dumps

from zope.formlib import form
from zope.schema import getFieldsInOrder
from zope.app.event.objectevent import ObjectCreatedEvent
from zope.event import notify
from zope import component

from yoma.layout import LayoutMixin

from getpaid.core import interfaces, options
from getpaid.core.order import Order

from AccessControl import getSecurityManager

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.Five.formlib import formbase
from Products.CMFCore.utils import getToolByName

from Products.PloneGetPaid.interfaces import IGetPaidManagementOptions

from base import BaseView, GridLayout
from widgets import CountrySelectionWidget, StateSelectionWidget


class BaseCheckoutForm( formbase.EditForm, BaseView ):

    template = ZopeTwoPageTemplateFile("templates/checkout-billing-info.pt")
    
    def __init__( self, context, request ):
        self.context = context
        self.request = request
        self.setupLocale( request )
        self.setupEnvironment( request )   


##############################
# Some Property Bags - transient adapters

class BillingInfo( options.PropertyBag ): pass
class ShipAddressInfo( options.PropertyBag ): pass
class BillAddressInfo( options.PropertyBag ): pass

BillingInfo.initclass( interfaces.IUserPaymentInformation )
ShipAddressInfo.initclass( interfaces.IShippingAddress )
BillAddressInfo.initclass( interfaces.IBillingAddress )

class ImmutableBag( object ):

    def initfrom( self, other, iface ):
        for field_name, field in getFieldsInOrder( iface ):
            setattr( self, field_name, field.get( other ) )
        return self

class CheckoutConfirmed( BrowserView, BaseView ):
    pass

class CheckoutLayouts:

    credit_card_layout = GridLayout(
        ).addText(u'Credit Card', 0, 0
        ).addWidget('name_on_card', 1, 0                                                          
        ).addWidget('credit_card_type', 2, 0
        ).addWidget('credit_card', 3, 0
        ).addWidget('cc_expiration', 4, 0
        ).addWidget('cc_cvc', 5, 0
        ).addWidget('phone_number', 6, 0                                        
        )

    bill_address_layout = GridLayout(
        ).addText(u'Billing Address', 0, 1, colspan=2 
        ).addWidget('bill_first_line', 1, 0
        ).addWidget('bill_second_line', 2, 0
        ).addWidget('bill_city', 3, 0
        ).addWidget('bill_state', 4, 0
        ).addWidget('bill_country', 5, 0
        ).addWidget('bill_postal_code', 6, 0
# use same shipping as billing address
#        ).addWidget('bill_postal_code', 7, 0                                    
        )
        
    shipping_address_layout = GridLayout(

        ).addText(u'Mailing Address', 0, 1, colspan=2 
        ).addWidget('ship_first_line', 1, 0
        ).addWidget('ship_second_line', 2, 0
        ).addWidget('ship_city', 3, 0
        ).addWidget('ship_state', 4, 0
        ).addWidget('ship_country', 5, 0
        ).addWidget('ship_postal_code', 6, 0                            
        )
        
class CheckoutPayment( BaseCheckoutForm, LayoutMixin ):
    """
    browser view for collecting credit card information and submitting it to
    a processor.
    """
    form_fields = form.Fields( interfaces.IBillingAddress,
                               interfaces.IShippingAddress,
                               interfaces.IUserPaymentInformation )
    
    form_fields['ship_country'].custom_widget = CountrySelectionWidget
    form_fields['bill_country'].custom_widget = CountrySelectionWidget
    form_fields['ship_state'].custom_widget = StateSelectionWidget
    form_fields['bill_state'].custom_widget = StateSelectionWidget
    
    form_layout = GridLayout(
        ).addLayout(
           # Billing Address
           CheckoutLayouts.bill_address_layout,
           0, 0
        ).addLayout(
           # Shipping Address
           CheckoutLayouts.shipping_address_layout,           
           0, 1
        ).addLayout(
           # credit card information
           CheckoutLayouts.credit_card_layout,
           1, 1, colspan=2
        ).addAction("make-payment", 2, 1, colspan=2)

    # style it
    form_layout.setCSS( 0, 0, "fieldset")
    form_layout.setStyle( 0, 0, "border:1px solid black;")
    form_layout.setId( 0, 0, "billing")
    
    form_layout.setCSS( 0, 1, "fieldset")
    form_layout.setStyle( 0, 1, "border:1px solid black;")
    form_layout.setId( 0, 1, "shipping")

    form_layout.setCSS( 1, 1, "fieldset")
    form_layout.setStyle( 1, 1, "border:1px solid black;")
    form_layout.setId( 1, 1, "credit_card")



    _next_url = None

    def setupDataAdapters( self ):
	self.adapters = {}
        self.adapters[ interfaces.IBillingAddress ] = BillAddressInfo()
        self.adapters[ interfaces.IShippingAddress ] = ShipAddressInfo()
        self.adapters[ interfaces.IUserPaymentInformation ] = BillingInfo()
	return

    def __call__( self ):
        try:
            self.setupDataAdapters()
            return super( CheckoutPayment, self).__call__()
        except:
            import sys,pdb,traceback
            traceback.print_exc()
            pdb.post_mortem( sys.exc_info()[-1] )
            raise

    def setUpWidgets( self, ignore_request=False ):
        self.adapters = self.adapters is not None and self.adapters or {}
        self.widgets = form.setUpEditWidgets(
            self.form_fields, self.prefix, self.context, self.request,
            adapters=self.adapters, ignore_request=ignore_request
            )

    def render( self ):
        if self._next_url:
            self.request.RESPONSE.redirect( self._next_url )
            return ""
        return super( CheckoutPayment, self).render()


    @form.action(u"Make Payment", name="make-payment", condition=form.haveInputWidgets )
    def makePayment( self, action, data ):
        """ create an order, and submit to the processor
        for async processors we never even got here.???
        """
        manage_options = IGetPaidManagementOptions( self.context )
        processor_name = manage_options.payment_processor
        
        if not processor_name:
            raise RuntimeError( "No Payment Processor Specified" )

        processor = component.getAdapter( self.context,
                                          interfaces.IPaymentProcessor,
                                          processor_name )
        self.extractData( data )
        
        order = self.createOrder()
        order.processor_id = processor_name
        order.finance_workflow.fireTransition( "create" )

        # extract data to our adapters

        
        result = processor.authorize( order, self.adapters[ interfaces.IUserPaymentInformation ] )
        if result is interfaces.keys.results_async:
            # shouldn't ever happen..
            # XXX
            # huh.. we don't ever get here on async, we get async notified
            #
            # for async notified..
            # redirect to async, thank you for order, being reviewed, email confirmation sent, further
            # correspondence by email ?
            # 
            pass
        elif result is interfaces.keys.results_success:
            order_manager = component.getUtility( interfaces.IOrderManager )
            order_manager.store( order )
            order.finance_workflow.fireTransition("authorize")        
            # kill the cart after we create the order
            component.getUtility( interfaces.IShoppingCartUtility ).destroy( self.context )
        else:
            order.finance_workflow.fireTransition('reviewing-declined')
            self.status = result
            self.form_reset = False
            
        self._next_url = self.getNextURL( order )

    def extractData( self, data ):
        for iface, adapter in self.adapters.items():
            for name, field in getFieldsInOrder( iface ):
                if name in data:
                    field.set( adapter, data[ name ] )

    def createOrder( self ):
        order_manager = component.getUtility( interfaces.IOrderManager )
        order = Order()

        shopping_cart = component.getUtility( interfaces.IShoppingCartUtility ).get( self.context )
        # shopping cart is attached to the session, but we want to switch the storage to the persistent
        # zodb, we pickle to get a clean copy to store.
            
        order.shopping_cart = loads( dumps( shopping_cart ) )
        order.shipping_address = ImmutableBag().initfrom( self.adapters[ interfaces.IShippingAddress ],
                                                          interfaces.IShippingAddress ) 
        order.billing_address = ImmutableBag().initfrom( self.adapters[ interfaces.IBillingAddress ],
                                                         interfaces.IBillingAddress )
        while 1:
            order_id = str( random.randint( 0, sys.maxint ) )
            if order_manager.get( order_id ) is None:
                break
        order.order_id = order_id
        order.user_id = getSecurityManager().getUser().getId()
        notify( ObjectCreatedEvent( order ) )
        
        return order

    def getNextURL( self, order ):
        state = order.finance_state
        f_states = interfaces.workflow_states.order.finance
        base_url = self.context.absolute_url()

## we display errors inline on the checkout form, so don't redirect        
##         if state in ( f_states.CANCELLED,
##                       f_states.CANCELLED_BY_PROCESSOR,
##                       f_states.PAYMENT_DECLINED ):
##             return base_url + '/@@checkout-error'

        if state in ( f_states.CHARGEABLE,
                      f_states.REVIEWING,
                      f_states.CHARGED ):
            return base_url + '/@@getpaid-thank-you'
            

class DisclaimerView(BrowserView):
    """ Shows the disclaimer text from the getpaid settings.
    """

    @property
    def disclaimer(self):
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        settings = IGetPaidManagementOptions(portal)
        return settings.disclaimer

class PrivacyPolicyView(BrowserView):
    """ Shows the privacy policy text from the getpaid settings.
    """

    @property
    def privacyPolicy(self):
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        settings = IGetPaidManagementOptions(portal)
        return settings.privacy_policy
