"""

    Portal setup pages.

"""

__author__ = "Mikko Ohtamaa <mikko.ohtamaa@twinapex.fi>"
__docformat__ = "epytext"

from zope import component
from zope.formlib import form
from zope.viewlet.interfaces import IViewlet
from zope import schema
from zope.component import getMultiAdapter

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.Five.browser import BrowserView
from Products.Five.formlib import formbase
from Products.Five.viewlet import manager

from Products.PloneGetPaid import interfaces, pkg_home

from getpaid.paymentprocessors.registry import paymentProcessorRegistry

import Products.PloneGetPaid.browser.admin as base
import Products.PloneGetPaid.interfaces as igetpaid
from Products.PloneGetPaid.browser.widgets import SelectWidgetFactory, CountrySelectionWidget, StateSelectionWidget

from Products.PloneGetPaid.i18n import _ # TODO: Check which texts goes to getpaid.paymentprocessors code


class IGetPaidManagementMultiplePaymentOptions( igetpaid.IGetPaidManagementPaymentOptions ):
    """
    """

    # Add field which supports picking multiple payment options
    # schema.List(value_type=schema.Choice(vocabulary=SimpleVocabulary(terms=[])), required=False)
    payment_processors = schema.List( title = _(u"Enabled payment processors"), value_type=schema.Choice(source = "getpaid.payment_methods"))


class PaymentOptions( base.PaymentOptions ):
    """
    get paid management interface
    """
    form_fields = form.Fields(IGetPaidManagementMultiplePaymentOptions)
    form_fields['accepted_credit_cards'].custom_widget = SelectWidgetFactory
    form_name = _(u'Payment Options')


class PaymentProcessorsConfigurationView(BrowserView):
    """ The user goes to payment processor settings in GetPaid setup.

    Print available payment processors and see if they are enabled. Allow users
    to choose which processors to enable. Print links to individual processor setting
    pages.

    Payment processors are stored in portal_properties.payment_processor_properties.

    TODO: This form is not protected against XSS attacks.
    """
    def getCheckedForProcessor(self, processor):
        """

        @param processsor: Processor class instance
        """

        # See profiles/default/propertiestool.xml
        if processor.name in self.context.portal_properties.payment_processor_properties.enabled_processors:
            return "CHECKED"
        else:
            return None

    def getProcessors(self):
        """ Called from the template.

        @return: Iterable of Processor objects
        """
        return papaymentProcessorRegistryProcessors()

    def processForm(self):
        """ Manage HTTP post """
        actived = self.request["active-payment-processors"]

        # Add some level of safety
        for a in actived:
            if not a in paympaymentProcessorRegistrymes():
                raise RuntimeError("Tried to enable unsupported processor %s" % a)

        self.context.portal_properties.payment_processor_properties.enabled_processors = actived

    def __call__(self):

        if self.request["REQUEST_METHOD"] == "GET":
            return self.index() # render page
        else:
            # Assume POST, user is changing active payment methods
            self.processForm()
            return self.index() # render page


class PaymentProcessor( base.BaseSettingsForm ):
    """
    get paid management interface, slightly different because our form fields
    are dynamically set based on the store's setting for a payment processor.
    """

    form_fields = form.Fields()
    form_name = _(u'Payment Processor Settings')

    def __call__( self ):
        self.setupProcessorOptions()
        return super( PaymentProcessor, self).__call__()

    def setupProcessorOptions( self ):
        manage_options = interfaces.IGetPaidManagementOptions( self.context )

        # Processor name should be received as HTTP GET query parameter from the previous screen
        processor_name = self.request.get("payment_processor", None)

        if not processor_name:
            self.status = _(u"Please Select Payment Processor in Payment Options Settings")
            return

        #NOTE: if a processor name is saved in the configuration but the corresponding payment method package
        # doesn't exist anymore, a corresponding adapter will not be found.
        try:
            processor = component.getAdapter( self.context,
                                              igetpaid.IPaymentProcessor,
                                              processor_name )
        except:
            self.status = _(u"The currently configured Payment Processor cannot be found; please check if the corresponding package is installed correctly.")
            return

        self.form_fields = form.Fields( processor.options_interface )


