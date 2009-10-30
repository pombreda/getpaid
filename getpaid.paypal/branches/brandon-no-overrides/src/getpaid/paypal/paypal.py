"""
"""

from getpaid.core.processors import OffsitePaymentProcessor
from getpaid.paypal.interfaces import IPayPalStandardOptions


_paypal_hosts = _sites = {
    "Sandbox": "www.sandbox.paypal.com",
    "Production": "www.paypal.com",
    }

class PayPalStandardProcessor(OffsitePaymentProcessor):
    name = 'charge-it'
    title = u'PayPal Checkout'
    options_interface = IPayPalStandardOptions

    checkout_button = 'paypal-checkout-button'

    @property
    def server_url(self):
        url = self.options.server_url
        if url not in _paypal_hosts:
            url = 'Sandbox'
        return _paypal_hosts[url]
