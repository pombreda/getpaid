"""

cart-review checkout

$Id$
"""


from cPickle import loads, dumps
from datetime import timedelta

from zope.event import notify
from zope.formlib import form
from zope import schema, interface
from zope.app.event.objectevent import ObjectCreatedEvent
from zope.app.renderer.plaintext import PlainTextToHTMLRenderer

from zope import component

from zc.table import column
from getpaid.wizard import Wizard, ListViewController, interfaces as wizard_interfaces
from getpaid.core import interfaces, options, payment
from getpaid.core.order import Order

import Acquisition
from AccessControl import getSecurityManager
from ZTUtils import make_hidden_input

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.Five.formlib import formbase
from Products.CMFCore.utils import getToolByName

from Products.PloneGetPaid.interfaces import IGetPaidManagementOptions

from Products.PloneGetPaid.i18n import _

from base import BaseView
import cart as cart_core
from widgets import CountrySelectionWidget, StateSelectionWidget, CCExpirationDateWidget

def null_condition( *args ):
    return ()

def named( klass ):
    return "%s.%s"%(klass.__module__, klass.__name__)
    
class BaseCheckoutForm( formbase.EditForm, BaseView ):
    
    template = None # must be overridden

    hidden_form_vars = None
    adapters = None
    next_step_name = None # next step in wizard
    _next_url = None # redirect url
    wizard = None  # wizard
    
    interface.implements( wizard_interfaces.IWizardFormStep )
    
    def __init__( self, context, request ):
        self.context = context
        self.request = request
        self.setupLocale( request )
        self.setupEnvironment( request )

    def hidden_inputs( self ):
        if not self.hidden_form_vars: return ''
        return make_hidden_input( **self.hidden_form_vars )
        
    hidden_inputs = property( hidden_inputs )

    def setExportedVariables( self, mapping ):
        assert isinstance( mapping, dict )
        self.hidden_form_vars = mapping
        
    def getSchemaAdapters( self ):
        return self.adapters
        
    def invariantErrors( self ):
        errors = []
        for error in self.errors:
            if isinstance( error, interface.Invalid ):
                errors.append( error )
        return errors
    
    def getWidgetsByIName( self, name ):
        for iface in self.wizard.data_manager.adapters.keys():
            if name == named( iface ):
                return self._getWidgetsByInterface( iface )

    def _getWidgetsByInterface( self, interface ):
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

    def __init__(self, context):
        # need a context to be able to get the current available credit
        # cards.
        self.context = context

class ShipAddressInfo( options.PropertyBag ):
    title = "Shipping Information"

class BillAddressInfo( options.PropertyBag ):
    title = "Payment Information"

class ContactInfo( options.PropertyBag ):
    title = "Contact Information"    

ContactInfo.initclass( interfaces.IUserContactInformation )
BillingInfo.initclass( interfaces.IUserPaymentInformation )
ShipAddressInfo.initclass( interfaces.IShippingAddress )
BillAddressInfo.initclass( interfaces.IBillingAddress )

class ImmutableBag( object ):
    
    def initfrom( self, other, iface ):
        for field_name, field in schema.getFieldsInOrder( iface ):
            setattr( self, field_name, field.get( other ) )
        return self

class CheckoutWizard( Wizard ):
    """
    a bidirectional checkout wizard. see the controller if you want to customize,
    the sequence, see the viewlets for a given checkout page to customize a single
    ui component.
    
    steps should export all form variables not from themselves as hidden inputs, to 
    allow for prepopulated forms from previous inputs on that step. 
    
    steps are specified in order and by view name. a step view must minimally have a
    an update/render cycle ala content_provider or formlib views.
    
    forms are processed as normal, we depend on a _next_url attribute being present
    and set to the either a url or one of the marker values for next or previous steps.
    
    the form must specify handlers for next / previous / finished steps.
    
    steps can't override call methods, as such logic won't be processed, since we call
    update / render methods directly.
    

    """

    
    def checkShoppingCart(self):
        cart = component.getUtility(interfaces.IShoppingCartUtility).get( self.context )
        if cart is None or not len(cart):
            self.request.response.redirect('@@empty-cart')
            return False
        return True
    
    def checkAuthenticated( self ):
        membership = getToolByName( self.context, 'portal_membership')
        if membership.isAnonymousUser():
            portal = getToolByName( self.context, 'portal_url').getPortalObject()
            if IGetPaidManagementOptions( portal ).allow_anonymous_checkout:
                return True
            self.request.response.redirect('login_form?came_from=@@getpaid-checkout-wizard')
            return False
        return True
    
    def checkOrderId( self ):
        """ get the current order id out of the request,
            and verify it"""
        
        order_id = self.request.get('order_id', None)
        order_manager = component.getUtility( interfaces.IOrderManager )
        
        # if invalid order id, or no order id present 
        # set to first step and give new order id
        if ( order_id is None and not self.controller.hasPreviousStep() ) or \
            not order_manager.isValid( order_id ):
            self.controller.reset()
            self.request['order_id'] = order_id = order_manager.newOrderId()
            self.data_manager['order_id'] = order_id
            return True
            
        # if the order id is already in use check to see if its the same user that
        # owns it    
        if order_id in order_manager:
            # check for already existing order belonging to the same user from the
            # last day, and redirect them to it, else restart them in the wizard
            # all anonymous get restarted.
            user_id = getSecurityManager().getUser().getId()
            if user_id != 'Anonymous':
                results = order_manager.query( user_id = user_id,
                                               order_id = order_id,
                                               creation_date = timedelta(1) )
                if len(results) == 1:
                    order = list( results )[0]
                    base_url = self.context.absolute_url()
                    url = base_url + '/@@getpaid-thank-you?order_id=%s' %(order_id)
                    self.request.response.redirect( url )
                    self.wizard.data_manager.reset()
                    return False
                    
            # redirect and reset form variables
            self.wizard.data_manager.reset()
            self.request.response.redirect('@@checkout-wizard')

            return False
            
        self.data_manager['order_id'] = order_id
        return True
    
    def __call__( self ):
        # if we don't have a shopping cart redirect browser to empty cart view
        if not self.checkShoppingCart():
            return
        
        # if we're not authenticated redirect to login page with camefrom
        # which points back to the checkout wizard, bypassed by admin 
        # option to allow anonymous checkout
        if not self.checkAuthenticated():
            return
        
        # check to make sure we have a valid unused order id associated throughout
        # the checkout process. also stores the order id in the data mangaer for
        # use by other components.
        if not self.checkOrderId():
            return
        
        return super( CheckoutWizard, self).__call__()
    

class CheckoutController( ListViewController ):
    
    steps = ['checkout-address-info', 'checkout-review-pay']    

    def getStep( self, step_name ):
        step = component.getMultiAdapter( 
                    ( self.wizard.context, self.wizard.request ),
                    name=step_name
                    )
        return step.__of__( Acquisition.aq_inner( self.wizard.context ) )
        

class CheckoutAddress( BaseCheckoutForm ):
    """
    browser view for collecting credit card information and submitting it to
    a processor.
    """
    
    form_fields = form.Fields( interfaces.IBillingAddress,
                               interfaces.IShippingAddress,
                               interfaces.IUserContactInformation )
    
    form_fields['ship_country'].custom_widget = CountrySelectionWidget
    form_fields['bill_country'].custom_widget = CountrySelectionWidget
    form_fields['ship_state'].custom_widget = StateSelectionWidget
    form_fields['bill_state'].custom_widget = StateSelectionWidget
    
    template = ZopeTwoPageTemplateFile("templates/checkout-address.pt")
    
    def getSchemaAdapters( self ):
        adapters = {}        
        user = getSecurityManager().getUser()   
        contact_info = component.queryAdapter( user, interfaces.IUserContactInformation )
        if contact_info is None:
            contact_info = ContactInfo()
            
        billing_address = component.queryAdapter( user, interfaces.IBillingAddress)
        if billing_address is None:
            billing_address = BillAddressInfo()
        
        shipping_address = component.queryAdapter( user, interfaces.IShippingAddress )
        if shipping_address is None:
            shipping_address = ShipAddressInfo()
            
        adapters[ interfaces.IUserContactInformation ] = contact_info
        adapters[ interfaces.IShippingAddress ] = shipping_address
        adapters[ interfaces.IBillingAddress ] = billing_address
        return adapters
    
    def update( self ):
        if not self.adapters:
            self.adapters = self.getSchemaAdapters()
        super( CheckoutAddress, self).update()
    
    @form.action(_(u"Cancel"), name="cancel", validator=null_condition)
    def handle_cancel( self, action, data):
        return self.request.response.redirect( self.context.portal_url.getPortalObject().absolute_url() )
        
    @form.action(_(u"Continue"), name="continue")
    def handle_continue( self, action, data ):
        self.next_step_name = wizard_interfaces.WIZARD_NEXT_STEP

class CheckoutReviewAndPay( BaseCheckoutForm ):
    
    form_fields = form.Fields( interfaces.IUserPaymentInformation )
    form_fields['cc_expiration'].custom_widget = CCExpirationDateWidget

    template = ZopeTwoPageTemplateFile("templates/checkout-review-pay.pt")
    
    columns = [
        column.GetterColumn( title=_(u"Quantity"), getter=cart_core.LineItemColumn("quantity") ),
        column.GetterColumn( title=_(u"Name"), getter=cart_core.lineItemURL ),
        column.GetterColumn( title=_(u"Price"), getter=cart_core.lineItemPrice ),
        column.GetterColumn( title=_(u"Total"), getter=cart_core.lineItemTotal ),
       ]
    
    def getSchemaAdapters( self ):
        adapters = {}
        adapters[ interfaces.IUserPaymentInformation ] = BillingInfo(self.context)
        return adapters
        
    def setUpWidgets( self, ignore_request=False ):
        self.adapters = self.adapters is not None and self.adapters or {}
        
        # grab all the adapters and fields from the entire wizard form sequence (till the current step)
        adapters = self.wizard.data_manager.adapters
        adapters.update( self.getSchemaAdapters() )
        fields   = self.wizard.data_manager.fields
        
        # edit widgets for payment info
        self.widgets = form.setUpEditWidgets(
            self.form_fields.select( *schema.getFieldNames( interfaces.IUserPaymentInformation)),
            self.prefix, self.context, self.request,
            adapters=adapters, ignore_request=ignore_request
            )
        
        # display widgets for bill/ship address
        bill_ship_fields = fields.select( *schema.getFieldNamesInOrder( interfaces.IBillingAddress ) ) + \
                           fields.select( *schema.getFieldNamesInOrder( interfaces.IShippingAddress ) )
                           
        # clear custom widgets.. (typically for edit, we want display)
        for field in bill_ship_fields:
            if field.custom_widget is not None:
                field.custom_widget = None
        
        self.widgets += form.setUpEditWidgets(
            bill_ship_fields,  self.prefix, self.context, self.request,
            adapters=adapters, for_display=True, ignore_request=ignore_request
            )
    
    def renderCart( self ):
        cart = component.getUtility( interfaces.IShoppingCartUtility ).get( self.context )
        if not cart:
            return _(u"N/A")
        
        # create an order so that tax/shipping utilities have full order information
        # to determine costs (ie. billing/shipping address ).
        order = self.createOrder()
        formatter = cart_core.CartFormatter( order,
                                             self.request,
                                             cart.values(),
                                             prefix=self.prefix,
                                             visible_column_names = [c.name for c in self.columns],
                                             #sort_on = ( ('name', False)
                                             columns = self.columns )
        
        formatter.cssClasses['table'] = 'listing'
        return formatter()
        
    @form.action(_(u"Cancel"), name="cancel", validator=null_condition)
    def handle_cancel( self, action, data):
        return self.request.response.redirect( self.context.portal_url.getPortalObject().absolute_url() )
        
    @form.action(_(u"Back"), name="back")
    def handle_back( self, action, data):
        self.next_step_name = wizard_interfaces.WIZARD_PREVIOUS_STEP                
        
    @form.action(_(u"Make Payment"), name="make-payment", condition=form.haveInputWidgets )
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
        
        adapters = self.wizard.data_manager.adapters
        
        order = self.createOrder()
        order.processor_id = processor_name
        order.finance_workflow.fireTransition( "create" )
        
        # extract data to our adapters
        
        result = processor.authorize( order, adapters[ interfaces.IUserPaymentInformation ] )
        if result is interfaces.keys.results_async:
            # shouldn't ever happen, on async processors we're already directed to the third party
            # site on the final checkout step, all interaction with an async processor are based on processor
            # adapter specific callback views.
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
        
    def createOrder( self ):
        order_manager = component.getUtility( interfaces.IOrderManager )
        order = Order()
        
        shopping_cart = component.getUtility( interfaces.IShoppingCartUtility ).get( self.context )
        
        # shopping cart is attached to the session, but we want to switch the storage to the persistent
        # zodb, we pickle to get a clean copy to store.
        adapters = self.wizard.data_manager.adapters
                
        order.shopping_cart = loads( dumps( shopping_cart ) )
        order.shipping_address = payment.ShippingAddress.frominstance( adapters[ interfaces.IShippingAddress ] )
        order.billing_address = payment.BillingAddress.frominstance( adapters[ interfaces.IBillingAddress ] )
        order.contact_information = payment.ContactInformation.frominstance( adapters[ interfaces.IUserContactInformation ] )

        order.order_id = self.wizard.data_manager.get('order_id')
        order.user_id = getSecurityManager().getUser().getId()
        notify( ObjectCreatedEvent( order ) )
        
        return order
    
    def getNextURL(self, order):
        state = order.finance_state
        f_states = interfaces.workflow_states.order.finance
        base_url = self.context.absolute_url()

        if state in (f_states.CANCELLED,
                     f_states.CANCELLED_BY_PROCESSOR,
                     f_states.PAYMENT_DECLINED):
            return base_url + '/@@getpaid-cancelled-declined?order_id=%s&finance_state=%s' %(order.order_id, state)
        
        if state in (f_states.CHARGEABLE,
                     f_states.CHARGING,
                     f_states.REVIEWING,
                     f_states.CHARGED):
            return base_url + '/@@getpaid-thank-you?order_id=%s&finance_state=%s' %(order.order_id, state)
        

class StorePropertyView(BrowserView):
    
    def _getProperty(self, name ):
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        settings = IGetPaidManagementOptions(portal)
        value = getattr( settings, name, '')
        if value:
            renderer = PlainTextToHTMLRenderer(value, self.request)
            value = renderer.render().strip()
        return value

class DisclaimerView( StorePropertyView ):
    """ Shows the disclaimer text from the getpaid settings.
    """
    @property
    def disclaimer( self ):
        return self._getProperty( 'disclaimer' )
    
class PrivacyPolicyView( StorePropertyView ):
    """ Shows the privacy policy text from the getpaid settings.
    """
    @property
    def privacy_policy(self):
        return self._getProperty('privacy_policy')
