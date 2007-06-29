"""
"""

from getpaid.core.options import PersistentOptions
import interfaces

GoogleCheckoutOptions = PersistentOptions.wire("GoogleCheckoutOptions",
                                               "getpaid.googlecheckout",
                                               interfaces.IGoogleCheckoutOptions )

