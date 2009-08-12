from zope.component import getUtility, getAdapter
from zope.formlib import form
from Products.CMFCore.utils import getToolByName
from getpaid.core.interfaces import IPaymentProcessor, IOrderManager, IShoppingCartUtility, IFormSchemas, keys
from getpaid.wizard import interfaces as wizard_interfaces
from Products.PloneGetPaid.interfaces import IGetPaidManagementOptions
from AccessControl import getSecurityManager
from Products.PloneGetPaid.browser import checkout as base
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from getpaid.removalsales import _

class CheckoutReviewAndPay(base.CheckoutReviewAndPay):
    """
    Removal Sales payment method review and pay page.
    """
    template = ZopeTwoPageTemplateFile("templates/pay.pt")

    @form.action(_(u"Cancel"), name="cancel", validator=() )
    def handle_cancel( self, action, data):
        url = self.context.portal_url.getPortalObject().absolute_url()
        url = url.replace("https://", "http://")
        return self.request.response.redirect(url)

    @form.action(_(u"Back"), name="back", validator=() )
    def handle_back( self, action, data):
        self.next_step_name = wizard_interfaces.WIZARD_PREVIOUS_STEP

    @form.action(_(u"Make Removal"), name="make-payment", condition=form.haveInputWidgets )
    def makePayment( self, action, data ):
        """ create an order, and submit to the processor
        """

        siteroot = getToolByName(self.context, "portal_url").getPortalObject()
        manage_options = IGetPaidManagementOptions(siteroot)
        processor_name = self.wizard.getActivePaymentProcessor()

        if not processor_name:
            raise RuntimeError( "No Payment Processor Specified" )

        processor = getAdapter( siteroot,
                IPaymentProcessor,
                processor_name )

        adapters = self.wizard.data_manager.adapters

        order = self.createOrder()
        order.processor_id = processor_name
        order.finance_workflow.fireTransition( "create" )
        # extract data to our adapters

        formSchemas = getUtility(IFormSchemas)
        order_manager = getUtility( IOrderManager )
        order_manager.store( order )
        order.finance_workflow.fireTransition("authorize")
        template_key = 'order_template_entry_name'

        order_template_entry = self.wizard.data_manager.get(template_key)
        del self.wizard.data_manager[template_key]

        # if the user submits a name, it means he wants this order named
        if order_template_entry:
            uid = getSecurityManager().getUser().getId()
            if uid != 'Anonymous':
                named_orders_list = getUtility(INamedOrderUtility).get(uid)
                if order_template_entry not in named_orders_list:
                    named_orders_list[order.order_id] = order_template_entry
        # kill the cart after we create the order
        getUtility( IShoppingCartUtility ).destroy( self.context )

        # fulfill the order - this will subtract it from warehouses
        order.fulfillment_workflow.fireTransition('process-order')
        order.fulfillment_workflow.fireTransition('deliver-processing-order')

        self._next_url = self.getNextURL( order )

