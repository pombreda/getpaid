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


class ThankYouView(BrowserView):

    def render(self):
        pass


class AbstractPaymentProcessorSelectorButtonView(BrowserView):
    """ Render payment method selector button on checkout page. """

    index = ViewPageTemplateFile("templates/abstract_button.pt")

    def site_url(self):
        return self.context.site_url

    def render(self, processor):
        """ Child classes should override this.

        Normally you want to return rendered template::

            return self.index()

        @param processor: Processor class instance
        @return: HTML code as a string
        """
        self.processor = processor
        return self.index()