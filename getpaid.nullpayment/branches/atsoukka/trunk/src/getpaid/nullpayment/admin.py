from zope import component
from zope.formlib import form

from getpaid.core.interfaces import IPaymentProcessor

from getpaid.nullpayment import interfaces

from Products.PloneGetPaid.browser.base import EditFormViewlet

class NullPaymentOptions( EditFormViewlet ):

    form_name = u"Null Payment Options"
    form_description = u"Configuration of Null Payment Processor"
    form_fields = form.Fields( interfaces.INullPaymentOptions )
    prefix = "nullpayment"

    def setUpWidgets( self, ignore_request=False ):
        self.adapters = {
            interfaces.INullPaymentOptions: component.getUtility( IPaymentProcessor, name="nullpayment" )
            }
        self.widgets = form.setUpEditWidgets(
            self.form_fields, self.prefix, self.context, self.request,
            adapters=self.adapters, ignore_request=ignore_request
            )
