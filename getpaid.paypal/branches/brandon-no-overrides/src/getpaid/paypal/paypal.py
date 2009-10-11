"""
"""

from getpaid.core.processors import OffsitePaymentProcessor
from getpaid.paypal.interfaces import IPaypalStandardOptions


_paypal_hosts = _sites = {
    "Sandbox": "www.sandbox.paypal.com",
    "Production": "www.paypal.com",
    }

class PaypalStandardProcessor(OffsitePaymentProcessor):
    name = 'charge-it'
    title = u'PayPal Checkout'
    options_interface = IPaypalStandardOptions

    checkout_button = 'paypal-checkout-button'

    @property
    def server_url(self):
        return _paypal_hosts[self.options.server_url]
