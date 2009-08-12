from getpaid.core.options import PersistentOptions
from interfaces import IRemovalsalesOptions

RemovalsalesOptions = PersistentOptions.wire("Removalsales",
        "getpaid.removalsales",
        IRemovalsalesOptions)
