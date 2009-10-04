# -*- coding: utf-8 -*-
"""

    Viewlets used in the shop.

"""

__author__ = "Mikko Ohtamaa <mikko.ohtamaa@twinapex.com> http://www.twinapex.com"
__docformat__ = "epytext"
__license__ = "GPL"
__copyright__ = "2009 Twinapex Research"


import os
from urllib import urlencode

from zope.interface import implements, Interface
from zope import component

from AccessControl import getSecurityManager
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from Products.PloneGetPaid.interfaces import PayableMarkers, IGetPaidCartViewletManager, INamedOrderUtility
from Products.PloneGetPaid.interfaces import IGetPaidManagementOptions, IConditionalViewlet, IVariableAmountDonatableMarker
from Products.PloneGetPaid import sessions
from Products.PloneGetPaid import config

import getpaid.core.interfaces

from getpaid.atshop import atshopMessageFactory as _
from getpaid.atshop.interfaces import IVariationItemFactory, IBuyableMarker

