from Products.Five.browser import BrowserView
from zope.component import getUtility

from Products.PloneGetPaid.interfaces import IGetPaidManagementOptions
from getpaid.core.interfaces import IShoppingCartUtility, IOrderManager
from getpaid.core.order import Order
from getpaid.core import payment

from cPickle import loads, dumps
from AccessControl import getSecurityManager

from getpaid.paypal.paypal import PaypalStandardProcessor

class PayPalCheckoutButton(BrowserView):
    """page for paypal button
    """
    def button_gif(self):
        return u"http://images.paypal.com/images/x-click-but1.gif"

    def action_url(self):
        return 'https://%s/cgi-bin/webscr' % self.context.server_url

    def image_url(self):
        return ('https://%s/en_US/i/btn/x-click-but01.gif'
                % self.context.server_url)

    def cart_fields(self):
        """Return shopping cart contents as fields for PayPal form."""
        fields = []
        for n, item in enumerate(self.context.cart.values()):
            n = n + 1  # start list with 1 rather than 0
            fields.append(('item_name_%d' % n, item.name))
            fields.append(('item_number_%d' % n, item.product_code))
            fields.append(('amount_%d' % n, item.cost))
            fields.append(('quantity_%d' % n, item.quantity))
        return fields

    def getButton(self):
        button = PaypalStandardProcessor(self.context)
        cart_util = getUtility(IShoppingCartUtility)
        cart = cart_util.get(self.context, create=True)
        site = self.context.portal_url.getPortalObject()
        manage_options = IGetPaidManagementOptions( site )
        
        # we'll get the order_manager, create the new order, and store it.
        order_manager = getUtility(IOrderManager)
        new_order_id = order_manager.newOrderId()
        order = Order()
        
        # register the payment processor name to make the workflow handlers happy
        order.processor_id = manage_options.payment_processor
        
        # FIXME: registering an empty contact information list for now - need to populate this from user
        # if possible
        order.contact_information = payment.ContactInformation()
        order.billing_address = payment.BillingAddress()
        order.shipping_address = payment.ShippingAddress()

        order.order_id = new_order_id
        
        # make cart safe for persistence by using pickling
        order.shopping_cart = loads(dumps(cart))
        order.user_id = getSecurityManager().getUser().getId()

        order.finance_workflow.fireTransition('create')
        
        order_manager.store(order)

        # have to wait for the order to be created and the cart added for this to work
        order.finance_workflow.fireTransition('authorize')

        # save html for button - we'll destroy the cart later on
        html = button.cart_post_button(order)
        
        # and destroy the cart
        cart_util.destroy(self.context)

        return html
