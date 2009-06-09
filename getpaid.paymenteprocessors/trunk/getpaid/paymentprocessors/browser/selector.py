"""

    Views to render payment processor selectors.

"""

__author__ = "Mikko Ohtamaa <mikko.ohtamaa@twinapex.fi>"
__docformat__ = "epytext"

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from getpaid.paymentprocessors.registry import paymentProcessorUIRegistry

class MultipleProcessorsBrowserView(BrowserView):
    """ Base class for HTML pages which use multiple payment processors code in UI.

    Contains helper functions to deal with processors.
    """

    def getProcessors(self):
        """ Called from the template.

        @return: Iterable of Processor objects
        """
        return paymentProcessorUIRegistry.getProcessors()


    def getActiveProcessor(self):
        """ Get the selectd payment processor.

        """
        pass

class PaymentMethodSelectionView(MultipleProcessorsBrowserView):
    """ The user has clicked checkout and now he/she must choose the payment method.

    Render HTML page containing all payment processor selectors.
    """

    def renderProcessor(self, processor):
        """ Create selection button renderer view and call it.

        @param processor: registry.Entry instance
        """
        view = processor.getButtonView(self.context, self.request)
        return view()

    def __call__(self):
        pass

class ThankYouView(BrowserView):

    def render(self):
        pass

