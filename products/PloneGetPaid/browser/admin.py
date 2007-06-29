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
    


# Profile
class Identification( formbase.EditForm, BaseView ):
    """
    get paid management interface
    """
    template = ZopeTwoPageTemplateFile("templates/admin-identification.pt")
    form_fields = form.Fields(interfaces.IGetPaidManagementIdentificationOptions)
    options = None
    
    def __init__( self, context, request ):
        self.context = context
        self.request = request
        self.setupLocale( request )
        self.setupEnvironment( request )    
        

#Configure
class ContentTypes( formbase.EditForm, BaseView ):
    """
    get paid management interface
    """
    template = ZopeTwoPageTemplateFile("templates/admin-content-types.pt")
    form_fields = form.Fields( interfaces.IGetPaidManagementContentTypes )

    form_fields['buyable_types'].custom_widget = SelectWidgetFactory
    form_fields['premium_types'].custom_widget = SelectWidgetFactory
    form_fields['donate_types'].custom_widget = SelectWidgetFactory
    form_fields['shippable_types'].custom_widget = SelectWidgetFactory

    options = None
    
    def __init__( self, context, request ):
        self.context = context
        self.request = request
        self.setupLocale( request )
        self.setupEnvironment( request )

class ShippingOptions( formbase.EditForm, BaseView ):
    """
    get paid management interface
    """
    template = ZopeTwoPageTemplateFile("templates/admin-shipping-options.pt")
    
    options = None
    
    def __init__( self, context, request ):
        self.context = context
        self.request = request
        self.setupLocale( request )
        self.setupEnvironment( request ) 

class PaymentOptions( formbase.EditForm, BaseView ):
    """
    get paid management interface
    """
    template = ZopeTwoPageTemplateFile("templates/admin-payment-options.pt")
    form_fields = form.Fields(interfaces.IGetPaidManagementPaymentOptions)

    options = None
    
    def __init__( self, context, request ):
        self.context = context
        self.request = request
        self.setupLocale( request )
        self.setupEnvironment( request ) 

class PaymentProcessor( formbase.EditForm, BaseView ):
    """
    get paid management interface
    """
    
    template = ZopeTwoPageTemplateFile("templates/admin-payment-processor.pt")

    form_fields = None
    options = None
    
    def __init__( self, context, request ):
        self.context = context
        self.request = request
        self.setupLocale( request )
        self.setupEnvironment( request )

    def __call__( self ):
        self.setupProcessorOptions()
        return super( Processor, self).__call__()
        
    def setupProcessorOptions( self ):
        manage_options = interfaces.IGetPaidManagementOptions( self.context )
        
        processor_name = manage_options.payment_processor
        if not processor_name:
            return

        processor = component.getAdapter( self.context,
                                          igetpaid.IPaymentProcessor,
                                          processor_name )
        
        self.form_fields = form.Fields( processor.options_interface )
        
# Order Management
class CustomerInformation( formbase.EditForm, BaseView ):
    """
    get paid management interface
    """
    template = ZopeTwoPageTemplateFile("templates/admin-customer-information.pt")
    form_fields = form.Fields(interfaces.IGetPaidManagementCustomerInformation)
    
    options = None
    
    def __init__( self, context, request ):
        self.context = context
        self.request = request
        self.setupLocale( request )
        self.setupEnvironment( request )

class PaymentProcessing( formbase.EditForm, BaseView ):
    """
    get paid management interface
    """
    template = ZopeTwoPageTemplateFile("templates/admin-payment-processing.pt")
    form_fields = form.Fields(interfaces.IGetPaidManagementPaymentProcessing)
    options = None
    
    def __init__( self, context, request ):
        self.context = context
        self.request = request
        self.setupLocale( request )
        self.setupEnvironment( request )
        
class WeightUnits( formbase.EditForm, BaseView ):
    """
    get paid management interface
    """
    template = ZopeTwoPageTemplateFile("templates/admin-weight-units.pt")
    form_fields = form.Fields(interfaces.IGetPaidManagementWeightUnits)
    options = None
    
    def __init__( self, context, request ):
        self.context = context
        self.request = request
        self.setupLocale( request )
        self.setupEnvironment( request )    
        
class SessionTimeout( formbase.EditForm, BaseView ):
    """
    get paid management interface
    """
    template = ZopeTwoPageTemplateFile("templates/admin-session-timeout.pt")
    form_fields = form.Fields(interfaces.IGetPaidManagementSessionTimeout)
    options = None
    
    def __init__( self, context, request ):
        self.context = context
        self.request = request
        self.setupLocale( request )
        self.setupEnvironment( request )    

class SalesTax( formbase.EditForm, BaseView ):
    """
    get paid management interface
    """
    template = ZopeTwoPageTemplateFile("templates/admin-sales-tax.pt")
    form_fields = form.Fields(interfaces.IGetPaidManagementSalesTaxOptions)
    options = None
    
    def __init__( self, context, request ):
        self.context = context
        self.request = request
        self.setupLocale( request )
        self.setupEnvironment( request )  
                
#Currency        
class Currency( formbase.EditForm, BaseView ):
    """
    get paid management interface
    """
    template = ZopeTwoPageTemplateFile("templates/admin-currency.pt")
    form_fields = form.Fields(interfaces.IGetPaidManagementCurrencyOptions)
    options = None
    
    def __init__( self, context, request ):
        self.context = context
        self.request = request
        self.setupLocale( request )
        self.setupEnvironment( request )    
        


#Emails
class Email( formbase.EditForm, BaseView ):
    """
    get paid management interface
    """
    template = ZopeTwoPageTemplateFile("templates/admin-email.pt")
    form_fields = form.Fields(interfaces.IGetPaidManagementEmailOptions)
    options = None
    
    def __init__( self, context, request ):
        self.context = context
        self.request = request
        self.setupLocale( request )
        self.setupEnvironment( request )            
        self.setupEnvironment( request )    

class MerchantNotification( formbase.EditForm, BaseView ):
    """
    get paid management interface
    """
    template = ZopeTwoPageTemplateFile("templates/admin-merchant-notification.pt")
    form_fields = form.Fields(interfaces.IGetPaidManagementMerchantNotificationOptions)
    options = None
    
    def __init__( self, context, request ):
        self.context = context
        self.request = request
        self.setupLocale( request )
        self.setupEnvironment( request )            
        self.setupEnvironment( request )

class CustomerNotification( formbase.EditForm, BaseView ):
    """
    get paid management interface
    """
    template = ZopeTwoPageTemplateFile("templates/admin-customer-notification.pt")
    form_fields = form.Fields(interfaces.IGetPaidManagementCustomerNotificationOptions)
    options = None
    
    def __init__( self, context, request ):
        self.context = context
        self.request = request
        self.setupLocale( request )
        self.setupEnvironment( request )            
        self.setupEnvironment( request )

#Customize Header/Footer        
class HeaderFooter( formbase.EditForm, BaseView ):
    """
    get paid management interface
    """
    template = ZopeTwoPageTemplateFile("templates/admin-headerfooter.pt")
    form_fields = form.Fields(interfaces.IGetPaidManagementHeaderFooterOptions)
    options = None
    
    def __init__( self, context, request ):
        self.context = context
        self.request = request
        self.setupLocale( request )
        self.setupEnvironment( request )    
       
