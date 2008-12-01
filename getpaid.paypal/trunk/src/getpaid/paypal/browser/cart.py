from Products.PloneGetPaid.browser.cart import ShoppingCartActions
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility

class Actions(ShoppingCartActions):

    template = ZopeTwoPageTemplateFile('templates/cart-actions.pt')
    
    def render(self):
        html = self.template()
        return html

    def actionsOtherThanCheckout(self):
        return [action for action in self.availableActions()
                if action.label != 'Checkout']

    def doesHaveActions(self):
        return len(self.availableActions()) > 0
    
    def buyNowButton(self):
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        button = """<form action='%s' style="display:inline;">
<input type="submit" class="button context"
    id="getpaid-paypal-button" name="paynow" value="Pay Now" 
    i18n:attributes="value" />
</form>"""
        url = "%s/@@getpaid-paypal-redirect" % portal.absolute_url()
        return button % url
