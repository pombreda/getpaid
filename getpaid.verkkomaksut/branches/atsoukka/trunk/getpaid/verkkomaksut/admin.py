from zope import component
from zope.formlib import form

from getpaid.core.interfaces import IPaymentProcessor

from getpaid.verkkomaksut import interfaces

from Products.PloneGetPaid.browser.base import EditFormViewlet

class VerkkomaksutOptions( EditFormViewlet ):

    form_name = u"Verkkomaksut Options"
    form_description = u"Configuration of Verkkomaksut Processor"
    form_fields = form.Fields( interfaces.IVerkkomaksutOptions )
    prefix = "verkkomaksut"

    def setUpWidgets( self, ignore_request=False ):
        self.adapters = {
            interfaces.IVerkkomaksutOptions: component.getUtility( IPaymentProcessor, name="verkkomaksut" )
            }
        self.widgets = form.setUpEditWidgets(
            self.form_fields, self.prefix, self.context, self.request,
            adapters=self.adapters, ignore_request=ignore_request
            )
