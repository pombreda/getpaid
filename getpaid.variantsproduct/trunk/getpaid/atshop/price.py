# -*- coding: utf-8 -*-
"""

    Price related utility functions.

"""

__author__ = "Mikko Ohtamaa <mikko.ohtamaa@twinapex.com> http://www.twinapex.com"
__docformat__ = "epytext"
__license__ = "GPL"
__copyright__ = "2009 Twinapex Research"

import types

import zope.interface

from getpaid.atshop.currency import format_currency
from getpaid.atshop.interfaces import IProductImageProvider, IMultiImageProduct, IVariantProduct
from getpaid.atshop import atshopMessageFactory as _

def get_price_text(object):
    """ Get the price text for the end user.

    @param object: Any product object

    @return: string or None if price is not available
    """

    if IMultiImageProduct.providedBy(object):
        try:
            price = object.price
        except KeyError:
            # Object is unitialized and will give out
            # KeyError: 'Cannot find field with name price'
            return None

        return format_currency(price)
    elif IVariantProduct.providedBy(object):
        price = object.getCheapestPrice()

        if price is not None:
            return _("Starting from " ) + format_currency(price)
    else:
        return None

    return None
