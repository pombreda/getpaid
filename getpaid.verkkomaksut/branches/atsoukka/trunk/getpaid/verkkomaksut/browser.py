"""
Verkkomaksut.fi checkout wizard button
"""

__version__ = "$Revision$"
# $Id$
# $URL$

# from AccessControl import Unauthorized

from zope import component

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

from getpaid.core import interfaces
from getpaid.core.interfaces import workflow_states as wf

from Products.PloneGetPaid.browser.checkout_wizard import PaymentProcessorButtonBase
from Products.PloneGetPaid.browser.checkout_wizard import ICheckoutContinuationKey

from getpaid.verkkomaksut.interfaces import IVerkkomaksutPayload, IVerkkomaksutPayment
from getpaid.verkkomaksut import VerkkomaksutProcessor as plugin

from zope.i18nmessageid import MessageFactory
_ = MessageFactory('getpaid.verkkomaksut')


class VerkkomaksutPaymentButton(PaymentProcessorButtonBase):
    """ Checkout Wizard Payment button """
    render = ViewPageTemplateFile("button.pt")
    title = _("Verkkomaksut.fi")
    
    @property
    def order(self):
        return component.getAdapter(self.wizard._order, IVerkkomaksutPayload)


class VerkkomaksutNotifyView(BrowserView):

    def __init__(self, *args):
        super(VerkkomaksutNotifyView, self).__init__(*args)
        payment = component.getAdapter(self.request, IVerkkomaksutPayment)
        if payment.verified_response:
            manager = component.getUtility(interfaces.IOrderManager)

            order = manager.get(payment.order_id)
            order.processor_id = plugin.NAME

            ## FIXME: This appeared to be a bad idea, but still
            ## this could be added to order as its own annotation..
            # if payment.creation_date is not None:
            #     order.creation_date = payment.creation_date

            if payment.processor_order_id is not None:
                order.processor_order_id = payment.processor_order_id

            if order.fulfillment_state is None:
                order.fulfillment_workflow.fireTransition("create")

            # FIXME: This should happen automatically (via subscriber)
            # when order's "create" transition occurs...
            for item in order.shopping_cart.values():
                if item.fulfillment_state is None:
                    item.fulfillment_workflow.fireTransition("create")

            if order.finance_state == None:
                order.finance_workflow.fireTransition("create")

            if order.finance_state == wf.order.finance.REVIEWING:
                order.finance_workflow.fireTransition("authorize")

            if order.finance_state == wf.order.finance.CHARGING:
                order.finance_workflow.fireTransition("charge-charging")


class VerkkomaksutReturnView(VerkkomaksutNotifyView):

    def __init__(self, *args):
        super(VerkkomaksutReturnView, self).__init__(*args)
        payment = component.getAdapter(self.request, IVerkkomaksutPayment)
        portal_url = getToolByName(self.context, "portal_url")
        site = portal_url.getPortalObject()
        utils = getToolByName(self.context, 'plone_utils')
            
        if not payment.verified_response:
            utils.addPortalMessage(_(u"Response from Verkkomaksut.fi couldn't be verified."),
                                   type='error')
            self.request.response.redirect(site.absolute_url() + "/@@checkout-wizard")
            # raise Unauthorized(_(u"Response from Verkkomaksut.fi couldn't be verified."))
        else:
            utils.addPortalMessage(_(u"The payment was successful."))

            manager = component.getUtility(interfaces.IOrderManager)
            order = manager.get(payment.order_id)
            key = str(ICheckoutContinuationKey(order))
            query = "?order_id=%s&key=%s" % (payment.order_id, key)
            self.request.response.redirect(site.absolute_url() + "/@@checkout-wizard" + query)


class VerkkomaksutCancelledOrDeclinedView(BrowserView):

    def __init__(self, *args):
        super(VerkkomaksutCancelledOrDeclinedView, self).__init__(*args)
        payment = component.getAdapter(self.request, IVerkkomaksutPayment)
        portal_url = getToolByName(self.context, "portal_url")
        site = portal_url.getPortalObject()
        utils = getToolByName(self.context, 'plone_utils')

        if not payment.verified_response:
            utils.addPortalMessage(_(u"Response from Verkkomaksut.fi couldn't be verified."),
                                   type='error')
            self.request.response.redirect(site.absolute_url() + "/@@checkout-wizard")
            # raise Unauthorized(_(u"Response from Verkkomaksut.fi couldn't be verified."))
        else:
            utils.addPortalMessage(_(u"Payment was cancelled or declined by Verkkomaksut.fi."),
                                   type='error')
            query = "?order_id=%s" % (payment.order_id)
            self.request.response.redirect(site.absolute_url() + "/@@checkout-wizard" + query)
