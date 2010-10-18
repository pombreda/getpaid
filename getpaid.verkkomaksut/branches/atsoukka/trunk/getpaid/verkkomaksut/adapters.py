"""
Verkkomaksut.fi order adapter
"""

__version__ = "$Revision$"
# $Id$
# $URL$

from zope import component, interface

from Products.CMFCore.utils import getToolByName

from getpaid.core import interfaces

from hashlib import md5
from datetime import datetime
import time

from getpaid.verkkomaksut.interfaces import IVerkkomaksutPayload, IVerkkomaksutPayment
from getpaid.verkkomaksut.interfaces import IVerkkomaksutOptions, ILanguageCulture
from getpaid.verkkomaksut import VerkkomaksutProcessor as factory

from zope.i18nmessageid import MessageFactory
_ = MessageFactory('getpaid.verkkomaksut')


# FIXME: Describe interface on IVerkkomaksutPayload

# API version: S1 
# See: http://www.verkkomaksut.fi/index.php?id=48

# Merchant ID                         MERCHANT_ID           11   N    R
# Payment amount                      AMOUNT                10   F    -(R)
# Order number                        ORDER_NUMBER          64   AN   R
# Reference number                    REFERENCE_NUMBER      50   N    O
# Order description                   ORDER_DESCRIPTION 65 000   AN   O
# Currency                            CURRENCY               3   A    R
# Return address / Successful payment RETURN_ADDRESS       255   AN   R
# Return address / Failed payment     CANCEL_ADDRESS       255   AN   R
# Return address / Pending payment    PENDING_ADDRESS      255   AN   O
# Notify address                      NOTIFY_ADDRESS       255   AN   R
# Type                                TYPE                   3   F    R
# Culture                             CULTURE                8   AN   O
# Preselected payment method          PRESELECTED_METHOD     2   N    O
# Service type                        MODE                   1   N    O
# Visible payment methods.            VISIBLE_METHODS       64   AN   O
# Group code.                         GROUP                 16   AN   O
# Authentication hash                 AUTHCODE              32   AN   R


class VerkkomaksutPayload(object):

    interface.implements(IVerkkomaksutPayload)

    def __init__(self, order):
        options = IVerkkomaksutOptions(component.getUtility(interfaces.IPaymentProcessor,
                                                            name=factory.name))
        site = component.getSiteManager()
        portal = getToolByName(site, "portal_url").getPortalObject()
        
        # Merchant ID and amount to be charged
        self.MERCHANT_ID = options.verkkomaksut_merchant_id
        self.AMOUNT = "%.2f" % interfaces.ILineContainerTotals(order).getTotalPrice()

        # Order ID
        self.ORDER_NUMBER = order.order_id

        # Order reference number
        if order.user_payment_info_trans_id is not None:
            self.REFERENCE_NUMBER = order.user_payment_info_trans_id
        else:
            self.REFERENCE_NUMBER = ""

        # Order description
        # FIXME: Requires possibility to customize with own adapter
        mtool = getToolByName(portal, "portal_membership")
        if not mtool.isAnonymousUser():
            self.ORDER_DESCRIPTION = mtool.getAuthenticatedMember().getId()
        else:
            self.ORDER_DESCRIPTION = "anonymous"

        # Currency is fixed to "EUR"
        self.CURRENCY = "EUR"

        # Verkkomaksut URLs
        base_url = portal.absolute_url()
        self.RETURN_ADDRESS = base_url + "/@@verkkomaksut-thank-you"
        self.CANCEL_ADDRESS = base_url + "/@@verkkomaksut-cancelled-declined"
        self.PENDING_ADDRESS = ""
        self.NOTIFY_ADDRESS = base_url + "/@@verkkomaksut-notify"
 
        # Verkkomaksut API version
        self.TYPE = "S1"

        # Verkkomaksut Culture
        language_tool = getToolByName(portal, "portal_languages")
        language_bindings = language_tool.getLanguageBindings()
        self.CULTURE = component.getUtility(ILanguageCulture)(language_bindings)

        # Verkkomaksut preselected payment method and service type
        self.PRESELECTED_METHOD = ""
        self.MODE = ""

        # Unused options
        self.VISIBLE_METHODS = ""
        self.GROUP = ""

        #Verkkomaksut authcode for API version (TYPE) "S1"
        m = md5()
        m.update(options.merchant_authentication_code)
        m.update("|" + self.MERCHANT_ID)
        m.update("|" + self.AMOUNT)
        m.update("|" + self.ORDER_NUMBER)
        m.update("|" + self.REFERENCE_NUMBER)
        m.update("|" + self.ORDER_DESCRIPTION)
        m.update("|" + self.CURRENCY)
        m.update("|" + self.RETURN_ADDRESS)
        m.update("|" + self.CANCEL_ADDRESS)
        m.update("|" + self.PENDING_ADDRESS)
        m.update("|" + self.NOTIFY_ADDRESS)
        m.update("|" + self.TYPE)
        m.update("|" + self.CULTURE)
        m.update("|" + self.PRESELECTED_METHOD)
        m.update("|" + self.MODE) 
        m.update("|" + self.VISIBLE_METHODS)
        m.update("|" + self.GROUP)
        self.AUTHCODE = m.hexdigest().upper()


class VerkkomaksutPayment(object):
    
    interface.implements(IVerkkomaksutPayment)

    def __init__(self, request):
        # order_id
        self.order_id = request.form.get('ORDER_NUMBER', None)

        # creation_date
        timestamp = request.form.get('TIMESTAMP', None)
        try:
            self.creation_date = datetime(*time.gmtime(float(timestamp))[:-3])
        except:
            self.creation_date = None

        # processor_order_id
        self.processor_order_id = request.form.get('PAID', None)

        # verified
        options = IVerkkomaksutOptions(component.getUtility(interfaces.IPaymentProcessor, name=factory.name))

        authcode = md5()
        authcode.update(request.form.get('ORDER_NUMBER', ""))
        authcode.update('|' + request.form.get('TIMESTAMP', ""))
        if request.form.has_key('PAID'):
            authcode.update('|' + request.form.get('PAID', ""))
        if request.form.has_key('METHOD'):
            authcode.update('|' + request.form.get('METHOD', ""))
        authcode.update('|' + options.merchant_authentication_code)
        
        if authcode.hexdigest().upper() == request.form.get('RETURN_AUTHCODE', ""):
            self.verified_response = True
        else:
            self.verified_response = False
