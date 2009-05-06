from Products.PloneGetPaid.browser.checkout import CheckoutReviewAndPay
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.PloneGetPaid.interfaces import IGetPaidManagementOptions

from Acquisition import aq_inner

from getpaid.luottokunta import LuottokuntaMessageFactory as _
from getpaid.luottokunta.interfaces import ILuottokuntaOptions, ILuottokuntaOrderInfo

from Products.Five.browser import BrowserView
from zope.component import getMultiAdapter

import datetime
import md5

from getpaid.core.interfaces import IOrderManager
from zope.component import getUtility

class LuottokuntaPay(CheckoutReviewAndPay):

    template = ZopeTwoPageTemplateFile("templates/checkout-luottokunta-pay.pt")

    def is_luottokunta(self):
        """
        Returns true if payment processor is luottokunta.
        """
        siteroot = getToolByName(self.context, "portal_url").getPortalObject()
        manage_options = IGetPaidManagementOptions(siteroot)
        processor_name = manage_options.payment_processor
        if processor_name == u'Luottokunta HTML form interface':
            return True
        else:
            return False

    def years(self):
        this_year = datetime.date.today().year
        return range(this_year, this_year + 30)

    def months(self):
        return ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

    def luottokunta_options(self):
        context= aq_inner(self.context)
        return ILuottokuntaOptions(context)

    def order_info(self):
        order = self.createOrder()
        return ILuottokuntaOrderInfo(order)()

    def success_url(self):
        context= aq_inner(self.context)
        base_url = context.absolute_url()
        order = self.createOrder()
        order.finance_workflow.fireTransition( "create" )
        state = order.finance_state
#        return base_url + '/@@luottokunta-thank-you?order_id=%s' %(order.order_id)
        return base_url + '/@@luottokunta-thank-you?order_id=%s&finance_state=%s' %(order.order_id, state)

    def failure_url(self):
        context= aq_inner(self.context)
        base_url = context.absolute_url()
        return base_url + '/@@getpaid-cancelled-declined'

    def customer_id(self):
        context = aq_inner(self.context)
        membership = getToolByName(context, 'portal_membership')
#        import pdb; pdb.set_trace()
        member_id = membership.getAuthenticatedMember().getId()
        return member_id

class LuottokuntaThankYou(BrowserView):

    def __call__(self):
        order_manager = getUtility(IOrderManager)
        form = self.request.form
        order_id = form.get('order_id')
        order = order_manager.get(order_id)
        order_manager.store( order )
        order.finance_workflow.fireTransition("authorize")
#        template_key = 'order_template_entry_name'
#        order_template_entry = self.wizard.data_manager.get(template_key)
#        del self.wizard.data_manager[template_key]
#        # if the user submits a name, it means he wants this order named
#        if order_template_entry:
#            uid = getSecurityManager().getUser().getId()
#            if uid != 'Anonymous':
#                named_orders_list = component.getUtility(INamedOrderUtility).get(uid)
#                if order_template_entry not in named_orders_list:
#                    named_orders_list[order.order_id] = order_template_entry
            # kill the cart after we create the order
        component.getUtility( interfaces.IShoppingCartUtility ).destroy( self.context )
