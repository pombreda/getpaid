"""
$Id$
"""

import os
import urllib

from ZTUtils import make_hidden_input

from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.Five.browser import BrowserView
from Products.Five.formlib import formbase
from Products.PloneGetPaid import interfaces, pkg_home

from zope import component
from zope.formlib import form
from zope.app.form.browser import MultiSelectWidget
from zope.i18nmessageid import MessageFactory

import getpaid.core.interfaces as igetpaid

from Products.PloneGetPaid.i18n import _

from base import BaseView
from widgets import SelectWidgetFactory, CountrySelectionWidget, StateSelectionWidget


class Overview( BrowserView ):
    """ overview of entire system
    """
    def __call__( self ):
        self.settings = interfaces.IGetPaidManagementOptions( self.context )
        return super( Overview, self).__call__()
    
    def getVersion( self ):
        fh = open( os.path.join( pkg_home, 'version.txt') )
        version_string = fh.read()
        fh.close()
        return version_string
                
class BaseSettingsForm( formbase.EditForm, BaseView ):

    options = None
    template = ZopeTwoPageTemplateFile("templates/settings-page.pt")
    hidden_form_vars = None # mapping of hidden variables to pass through on the form

    def hidden_inputs( self ):
        if not self.hidden_form_vars: return ''
        return make_hidden_input( **self.hidden_form_vars )

    hidden_inputs = property( hidden_inputs )
    
    def __init__( self, context, request ):
        self.context = context
        self.request = request
        self.setupLocale( request )
        self.setupEnvironment( request )    

    def update( self ):
        try:
            interface = iter( self.form_fields ).next().field.interface
        except StopIteration:
            interface = None
        if interface is not None:
            self.adapters = { interface : interfaces.IGetPaidManagementOptions( self.context ) } 
        super( BaseSettingsForm, self).update()
        
# Profile
class Identification( BaseSettingsForm ):
    """
    get paid management interface
    """
    form_fields = form.Fields(interfaces.IGetPaidManagementIdentificationOptions)
    form_fields['contact_country'].custom_widget = CountrySelectionWidget
    form_fields['contact_state'].custom_widget = StateSelectionWidget

#Configure
class ContentTypes( BaseSettingsForm ):
    """
    get paid management interface
    """
    form_fields = form.Fields( interfaces.IGetPaidManagementContentTypes )
    form_fields = form_fields.omit('premium_types')
    form_fields = form_fields.omit('shippable_types')

    form_fields['buyable_types'].custom_widget = SelectWidgetFactory
    #form_fields['premium_types'].custom_widget = SelectWidgetFactory
    form_fields['donate_types'].custom_widget = SelectWidgetFactory
    #form_fields['shippable_types'].custom_widget = SelectWidgetFactory


class ShippingOptions( BaseSettingsForm ):
    """
    get paid management interface
    """
    form_fields = form.Fields(interfaces.IGetPaidManagementShippingOptions)

class PaymentOptions( BaseSettingsForm ):
    """
    get paid management interface
    """
    form_fields = form.Fields(interfaces.IGetPaidManagementPaymentOptions)
    form_fields['payment_processors'].custom_widget = SelectWidgetFactory
#    form_fields['accepted_credit_cards'].custom_widget = SelectWidgetFactory

class PaymentProcessor( BaseSettingsForm ):
    """
    get paid management interface, slightly different because our form fields
    are dynamically set based on the store's setting for a payment processor.
    """
    template = ZopeTwoPageTemplateFile("templates/payment-settings-page.pt")
    form_fields = form.Fields()
    _edited_processor_name = None

    def __call__( self, processor_name=None ):
        self._edited_processor_name = None
        self.setupProcessorOptions(processor_name)
        return super( PaymentProcessor, self).__call__()
        
    def setupProcessorOptions( self, processor_name=None ):
        """
        Setup form fields for the specified payment processor; 
        if a payment processor is not specified in the request, configure the first one available.
        """
        manage_options = interfaces.IGetPaidManagementOptions( self.context )
        
        processor_names = manage_options.payment_processors
        if len(processor_names) == 0:
            self.status = _(u"Please Select at least a Payment Processor in Payment Options Settings")
            return

        if processor_name is not None and processor_name not in processor_names:
            self.status = _(u"Unknown processor")
            return
        
        if processor_name is None:
            processor_name = processor_names[0]
        
        self._edited_processor_name = processor_name

        #TODO: if a processor name is saved in the configuration and the corresponding payment method packages
        # doesn't exists anymore, processor_name in processor_names will be true but the configuration page will fail.
        processor = None
        try:        
            processor = component.getAdapter( self.context,
                                              igetpaid.IPaymentProcessor,
                                              processor_name )
        except:
            self.status = _(u"The currenly configured Payment Processor cannot be found; please check if the corresponding package is installed correctly.")
            return
        
        self.hidden_form_vars = {'processor_name' : self._edited_processor_name}
        self.form_fields = form.Fields( processor.options_interface )
    
    @property
    def editedProcessorName(self):
        """
        Returns the currenly edited processor name
        """
        return self._edited_processor_name
        
    @property
    def activeProcessorNames( self ):
        """Returns the active payment processors names for the store as dictionaries (url quoted, plain)
        """
        manage_options = interfaces.IGetPaidManagementOptions( self.context )
        processor_names = [{'urlquoted' : urllib.quote(processor_name), 'plain' : processor_name} for processor_name in manage_options.payment_processors]
        return processor_names
        
# Order Management
class CustomerInformation( BaseSettingsForm ):
    """
    get paid management interface
    """
    form_fields = form.Fields(interfaces.IGetPaidManagementCustomerInformation)

class PaymentProcessing( BaseSettingsForm ):
    """
    get paid management interface
    """
    form_fields = form.Fields(interfaces.IGetPaidManagementPaymentProcessing)
        
class WeightUnits( BaseSettingsForm ):
    """
    get paid management interface
    """
    form_fields = form.Fields(interfaces.IGetPaidManagementWeightUnits)
        
class SessionTimeout( BaseSettingsForm ):
    """
    get paid management interface
    """
    form_fields = form.Fields(interfaces.IGetPaidManagementSessionTimeout)

class SalesTax( BaseSettingsForm ):
    """
    get paid management interface
    """
    form_fields = form.Fields(interfaces.IGetPaidManagementSalesTaxOptions)
                
#Currency        
class Currency( BaseSettingsForm ):
    """
    get paid management interface
    """
    form_fields = form.Fields(interfaces.IGetPaidManagementCurrencyOptions)

#Emails
class Email( BaseSettingsForm ):
    """
    get paid management interface
    """
    form_fields = form.Fields(interfaces.IGetPaidManagementEmailOptions)

#Customize Header/Footer        
class LegalDisclaimers( BaseSettingsForm ):
    """
    get paid management interface
    """
    form_fields = form.Fields(interfaces.IGetPaidManagementLegalDisclaimerOptions)
        
        
       

