"""
"""

from getpaid.core.options import PersistentOptions
import interfaces

MoneyTransferStandardOptions = PersistentOptions.wire("MoneyTransferStandardOptions",
                                                      "getpaid.moneytransfer",
                                                      interfaces.IMoneyTransferStandardOptions )

