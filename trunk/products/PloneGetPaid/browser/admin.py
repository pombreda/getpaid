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

import getpaid.core.interfaces as igetpaid

from ore.member.browser import SchemaSelectWidget as SelectWidgetFactory

from base import BaseView

class Overview( BrowserView ):
    """ overview of entire system
    """
    
class Core( formbase.EditForm, BaseView ):
    """
    get paid management interface
    """
    template = ZopeTwoPageTemplateFile("templates/admin-settings.pt")
    form_fields = form.Fields( interfaces.IGetPaidManagementOptions )

    form_fields['buyable_types'].custom_widget = SelectWidgetFactory
    form_fields['shippable_types'].custom_widget = SelectWidgetFactory
    form_fields['premium_types'].custom_widget = SelectWidgetFactory

    options = None
    
    def __init__( self, context, request ):
        self.context = context
        self.request = request
        self.setupLocale( request )
        self.setupEnvironment( request )


class Processor( formbase.EditForm, BaseView ):
    """
    get paid management interface
    """
    
    template = ZopeTwoPageTemplateFile("templates/admin-processor.pt")
    form_fields = None
    options = None
    
    def __init__( self, context, request ):
        self.context = context
        self.request = request
        self.setupLocale( request )
        self.setupEnvironment( request )        
        self.setupProcessorOptions()
        
    def setupProcessorOptions( self ):
        manage_options = interfaces.IGetPaidManagementOptions( self.context )
        
        processor_name = manage_options.payment_processor
        if not processor_name:
            return

        processor = component.getAdapter( manage_options,
                                          igetpaid.IPaymentProcessor,
                                          processor_name )
        
        self.form_fields = form.Fields( processor.options_interface )

