"""

cart-review checkout

$Id$
"""

from zope.formlib import form
from getpaid.core.interfaces import IUserPaymentInformation

from base import BaseFormView
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from zope.schema import getFieldsInOrder

from ore.member.browser import MemberContextEdit

class PropertyBag(object):

    schema = IUserPaymentInformation
    title = "Payment Details"
    description = ""
    
    def initclass( cls ):
        for field_name, field in getFieldsInOrder( IUserPaymentInformation ):
            setattr( cls, field_name, field.default )

    initclass = classmethod( initclass )

PropertyBag.initclass()

class CheckoutBillingCollection( MemberContextEdit ):

    form_fields = None
    template = ZopeTwoPageTemplateFile("templates/checkout-billing-info.pt")

    def getFormFields( self, user ):
        form_fields = super( CheckoutBillingCollection, self).getFormFields(user)
        self.adapters[ IUserPaymentInformation ] = self.billing_info
        return form_fields + form.Fields( IUserPaymentInformation )

    def __call__( self ):
        self.billing_info = PropertyBag()        
        return super( CheckoutBillingCollection, self).__call__()

    def setUpWidgets( self, ignore_request=False ):
        self.adapters = self.adapters is not None and self.adapters or {}
        self.widgets = form.setUpEditWidgets(
            self.form_fields, self.prefix, self.context, self.request,
            adapters=self.adapters, ignore_request=ignore_request
            )
    


    
