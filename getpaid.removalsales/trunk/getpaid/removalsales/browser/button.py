from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.PloneGetPaid.browser.checkout import BasePaymentMethodButton

class RemovalsalesPaymentButton(BasePaymentMethodButton):
    __call__ = ZopeTwoPageTemplateFile("templates/button.pt")
