# -*- coding: utf-8 -*-
"""

    Misc. utility functions.
"""

__author__ = "Mikko Ohtamaa <mikko.ohtamaa@twinapex.com> http://www.twinapex.com"
__docformat__ = "epytext"
__license__ = "GPL"
__copyright__ = "2009 Twinapex Research"

import types

import zope.interface

from zope.app.component.hooks import getSite

from Products.PloneGetPaid.interfaces import IGetPaidManagementCurrencyOptions

def format_currency(value):
    """
    @param value: monetary amount as float
    """

    site = getSite()

    assert type(value) == types.FloatType, "Got bad value:" + str(value)

    # TODO: Looks like the management screen is not yet there...
    # currency_options = interfaces.IGetPaidManagementCurrencyOptions(site)

    currency_symbol = u"€"

    return u"%.2f %s" % (value, currency_symbol)