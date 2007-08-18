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


from zope.dottedname import resolve
from zope.event import notify
from zope.formlib import form
from zope import schema, interface
from zope.interface.interfaces import IInterface
from zope.app.event.objectevent import ObjectCreatedEvent

from zope import component

from getpaid.core import interfaces, options
from getpaid.core.order import Order

from AccessControl import getSecurityManager
from ZTUtils import make_hidden_input

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.Five.formlib import formbase
from Products.CMFCore.utils import getToolByName

from Products.PloneGetPaid.interfaces import IGetPaidManagementOptions, ICheckoutInfoUtility, IBuyerInfo, IAddressActions

from Products.PloneGetPaid.i18n import _

from base import BaseView
from widgets import CountrySelectionWidget, StateSelectionWidget, CopyAddressWidget


class BaseCheckoutForm( formbase.PageForm, BaseView ):
    
    template = None # must be overridden
    hidden_form_vars = None
    _next_url = None
    _checkout_info = None
    
    def __init__( self, context, request ):
        self.context = context
        self.request = request
        self.setupLocale( request )
        self.setupEnvironment( request )
        checkout_manager = component.getUtility( ICheckoutInfoUtility )
        self._checkout_info = checkout_manager.get( self.context, create=True )

    def hidden_inputs( self ):
        if not self.hidden_form_vars: return ''
        return make_hidden_input( **self.hidden_form_vars )
    
    hidden_inputs = property( hidden_inputs )

    def invariantErrors( self ):
        errors = []
        for error in self.errors:
            if isinstance( error, interface.Invalid ):
                errors.append( error )
        return errors
    
    def getAdapters( self ):
        return self.adapters.values()

    def getFieldsByAdapter( self, adapter ):
        return [ff for ff in self.form_fields if ff.field.interface == adapter.schema]

    def getWidgetsByAdapter( self, adapter ):
        return [w for w in self.widgets if w.context.interface == adapter.schema ]

    def getWidgetsByIName( self, name ):
        # XXX only call through unrestricted code..
        iface  = resolve.resolve( name )
        assert IInterface.providedBy( iface )
        return self.getWidgetsByInterface( iface )

    def getWidgetsByInterface( self, interface ):
        return [w for w in self.widgets if w.context.interface == interface ]
        
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
        return super( BaseCheckoutForm, self).render()
    
##############################
# Some Property Bags - transient adapters

class BillingInfo( options.PropertyBag ):
    title = "Billing Information"

BillingInfo.initclass( interfaces.IUserPaymentInformation )

class ImmutableBag( object ):

    def initfrom( self, other, iface ):
        for field_name, field in schema.getFieldsInOrder( iface ):
            setattr( self, field_name, field.get( other ) )
        return self


WIZARD_NEXT_STEP = object()

class CheckoutWizard( BrowserView ):

    steps = ['checkout-address-info', 'checkout-review-pay']

    def __call__( self ):
        import pprint
        pprint.pprint( self.request.form )

        #TODO: hardcoded redirect to checkout wizard after login
        if not self.canCheckout():
            portal = getToolByName( self.context, 'portal_url').getPortalObject()
            url = portal.absolute_url()
            url = "%s/%s?%s=%s/%s"%( url,
                                     'login_form',
                                     'came_from',
                                     url,
                                     '@@getpaid-checkout-wizard' )
            return self.request.RESPONSE.redirect( url )
            
        current_step, next_step = self.getSteps( self.request )
        print 'wizard', current_step, next_step

        current = self.context.restrictedTraverse('@@%s'%current_step)
        current.update()
        
        if current._next_url == WIZARD_NEXT_STEP:
            print "moving to next step", next_step
            assert next_step, "No Next Step Or Redirect"
            next = self.context.restrictedTraverse('@@%s'%next_step )
            return next()

        return current.render()

    #TODO: checkout pages could be protected by configure.zcml, but checkout can take into account other parameters (number of items in cart etc.). Discuss.
    def canCheckout( self ):
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        manage_options = IGetPaidManagementOptions(portal)
        allow_anonymous_checkout = manage_options.allow_anonymous_checkout
        cart_manager = component.getUtility( interfaces.IShoppingCartUtility )
        cart = cart_manager.get( self.context, create=False )
        if cart is not None and len(cart) != 0:
            return allow_anonymous_checkout and True or getSecurityManager().getUser().getId() is not None
        return False
            
    def getSteps( self, request ):
        cur_step = self.request.get('cur_step', self.steps[0] )
        assert cur_step in self.steps
        
        # check last step
        if len(self.steps) -1 == self.steps.index(cur_step):
            return cur_step, None
        
        next_step = self.steps[ self.steps.index( cur_step ) + 1 ]
        return cur_step, next_step

class CheckoutAddress( BaseCheckoutForm ):
    """
    browser view for collecting credit card information and submitting it to
    a processor.
    """

    form_fields = None

    template = ZopeTwoPageTemplateFile("templates/checkout-address.pt")

    _next_url = None

    def __init__(self, context, request):
        super( CheckoutAddress, self ).__init__(context, request)
        self.setupFormFields()

    def setupDataAdapters( self ):
        self.adapters = {}
        if getSecurityManager().getUser().getId() is None:
            self.adapters[ IBuyerInfo ] = self._checkout_info
        self.adapters[ interfaces.IBillingAddress ] = self._checkout_info
        self.adapters[ IAddressActions ] = self._checkout_info
        self.adapters[ interfaces.IShippingAddress ] = self._checkout_info
        return
        
    def setupFormFields( self ):
        self.form_fields = form.Fields( interfaces.IBillingAddress,
                                        IAddressActions,
                                        interfaces.IShippingAddress)

        if getSecurityManager().getUser().getId() is None:
            self.form_fields = form.Fields( IBuyerInfo ) + self.form_fields

        self.form_fields['ship_country'].custom_widget = CountrySelectionWidget
        self.form_fields['bill_country'].custom_widget = CountrySelectionWidget
        self.form_fields['single_address'].custom_widget = CopyAddressWidget
        self.form_fields['ship_state'].custom_widget = StateSelectionWidget
        self.form_fields['bill_state'].custom_widget = StateSelectionWidget
        
    def update( self ):
        self.hidden_form_vars = dict( cur_step = 'checkout-address-info' )
        self.setupDataAdapters()
        super( CheckoutAddress, self).update()
        #HACK: there has to be a better way of doing this but I can't think of one at the moment
        if self.errors and len(self.errors) > 0 and self.widgets.get('single_address').getInputValue():
            for err in self.errors:
                if err.field_name.find('ship_') == 0:
                    cloned_widget = self.widgets.get(err.field_name.replace('ship_', 'bill_'))
                    if cloned_widget.hasValidInput():
                        self.request['form.' + err.field_name.replace('bill_', 'ship_')] = cloned_widget.getInputValue()
            super( CheckoutAddress, self ).update()

    @form.action(_(u"Continue"), name="continue", condition=form.haveInputWidgets )
    def handle_continue( self, action, data ):
        self._next_url = WIZARD_NEXT_STEP


class CheckoutReviewAndPay( BaseCheckoutForm ):

    form_fields = form.Fields( interfaces.IUserPaymentInformation )
    passed_fields = form.Fields( interfaces.IBillingAddress ) + \
                    form.Fields( interfaces.IShippingAddress )

    template = ZopeTwoPageTemplateFile("templates/checkout-review-pay.pt")

    def setupDataAdapters( self ):
        self.adapters = {}
        self.adapters[ interfaces.IBillingAddress ] = self._checkout_info
        self.adapters[ interfaces.IShippingAddress ] = self._checkout_info
        self.adapters[ interfaces.IUserPaymentInformation ] = BillingInfo()

        # extract data that was passed through in the request, using edit widgets
        # for marshalling value extraction. we'll basically throw an error here 
        # if the values aren't found, but that shouldn't happen in normal operation
        data = {}
        widgets = form.setUpEditWidgets( self.passed_fields, self.prefix, self.context,
                                         self.request, adapters=self.adapters,
                                         ignore_request=False )
        form.getWidgetsData( widgets, self.prefix, data )

        # widgets don't nesc. have one to one mapping, greedily pass through
        # all the previous form data in the request.. skip actions
        passed = {}
        for k in self.request.form:
            if k.startswith( self.prefix ) and not 'action' in k:
                passed[ k ] = self.request.form[ k ]
        self.hidden_form_vars = passed

        # save the data to the adapters
        self.extractData( data )
        
    def setUpWidgets( self, ignore_request=False ):
        self.adapters = self.adapters is not None and self.adapters or {}

        # edit widgets for payment info
        self.widgets = form.setUpEditWidgets(
            self.form_fields.select( *schema.getFieldNames( interfaces.IUserPaymentInformation)),
            self.prefix, self.context, self.request,
            adapters=self.adapters, ignore_request=ignore_request
            )

        # display widgets for bill/ship address
        self.widgets += form.setUpEditWidgets(
            self.passed_fields,  self.prefix, self.context, self.request,
            adapters=self.adapters, for_display=True, ignore_request=ignore_request
            )

    def update( self ):
        self.setupDataAdapters()
        self.hidden_form_vars['cur_step'] = 'checkout-review-pay'
        super( CheckoutReviewAndPay, self).update()
                

    # custom validator.. make sure we have all relevant data
    #def validatePayment( self, action, data ):
    #    pass

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
            for name, field in schema.getFieldsInOrder( iface ):
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

            
class CheckoutConfirmed( BrowserView ):
    """ thank you screen after success
    """

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
    def privacy_policy(self):
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        settings = IGetPaidManagementOptions(portal)
        return settings.privacy_policy
