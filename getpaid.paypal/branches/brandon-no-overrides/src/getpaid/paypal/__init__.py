"""
"""

from getpaid.core.options import PersistentOptions
import interfaces

PayPalStandardOptions = PersistentOptions.wire("PaypalStandardOptions",
                                               "getpaid.paypal",
                                               interfaces.IPayPalStandardOptions )

