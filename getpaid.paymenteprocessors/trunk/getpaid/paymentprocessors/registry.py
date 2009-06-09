"""

    Payment processor registry.

    Register user interface related payment processor settings.

"""

__author__ = "Mikko Ohtamaa <mikko.ohtamaa@twinapex.fi>"
__docformat__ = "epytext"

from zope.component import queryMultiAdapter

class BadViewConfigurationException(Exception):
    """ Thrown when defined view look up fails """

class Entry:
    """ Hold information about payment processor.

    Instance variables correspond one defined in IRegisterPaymentProcessorDirective.
    """
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def _getViewByName(self, context, request, name):
         view = queryMultiAdapter((context, request), name=name)
         if view == None:
             # Do graceful error handling
             raise BadViewConfigurationException("No browser:page implemented for payment processor %s view %s" % (self.name, name))

         return view

    def getButtonView(self, context, request):
        """ Get payment method selection button renderer.

        @return: BrowserView instance
        """
        view = self._getViewByName(context, request, self.selection_view)
        return view

    def getThankYouView(self, context, request):
        """ Get payment complete page renderer.

        @return: BrowserView instance
        """
        view = self._getViewByName(context, request, self.thank_you_view)
        return view

class PaymentProcessorUIRegistry:
    """ Payment processor configuration data holder.

    For possible parameters, see directives.IRegisterPaymentProcessorDirective
    """

    def __init__(self):
        self.clear()

    def register(self, processor):
        """ Put a new payment processor to the global registry """
        self.registry[processor.name] = processor

    def clear(self):
        """ Delete all registry entries """
        self.registry = {}

    def getProcessors(self):
        """ Return list of Entry objects. """
        return self.registry.values()

    def getNames(self):
        """ Return list of payment processor names """
        return self.registry.keys()

paymentProcessorUIRegistry = PaymentProcessorUIRegistry()


