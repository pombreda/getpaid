"""
$Id$
"""

from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.Five.browser import BrowserView
from Products.Five.formlib import formbase
from Products.PloneGetPaid import interfaces

from zope import component
from zope.formlib import form
from zope.app.form.browser import MultiSelectWidget

import getpaid.interfaces

def SelectWidgetFactory( field, request ):
    vocabulary = field.value_type.vocabulary
    return MultiSelectWidget( field, vocabulary, request ) 

class GetPaidAdmin( formbase.EditForm ):
    """
    get paid management interface
    """
    template = ZopeTwoPageTemplateFile("templates/admin.pt")
    form_fields = form.Fields( interfaces.IGetPaidManagementOptions )

    form_fields['buyable_types'].custom_widget = SelectWidgetFactory
    form_fields['shippable_types'].custom_widget = SelectWidgetFactory

    options = None
    
    def __init__( self, context, request ):
        self.context = context
        self.request = request
        self.setupProcessorOptions()
        
    def setupProcessorOptions( self ):
        manage_options = interfaces.IGetPaidManagementOptions( self.context )
        
        processor_name = manage_options.payment_processor
        if not processor_name:
            return

        processor = component.getAdapter( manage_options,
                                          getpaid.interfaces.IPaymentProcessor,
                                          processor_name )

        form_fields = form.Fields( processor.options_interface )
        self.form_fields = self.form_fields + form_fields

