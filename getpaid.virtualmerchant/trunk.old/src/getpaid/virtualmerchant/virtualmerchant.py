# Copyright (c) 2007 ifPeople, Kapil Thangavelu, and Contributors
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

"""

notes on error handling, if we haven't talked to the processor then raise an exception,
else return an error message so higher levels can interpret/record/notify user/etc.

$Id: $
"""

from zope import interface
from zope.component import getUtility, getAdapter
from zope.app.annotation.interfaces import IAnnotations

from getpaid.core import interfaces
from elementtree.ElementTree import Element, SubElement, tostring, fromstring
from datetime import date
from logging import getLogger
from urllib import quote
from zc import ssl
from Products.PloneGetPaid.interfaces import IGetPaidManagementPaymentOptions

from interfaces import IVirtualMerchantOptions
from getpaid.virtualmerchant import config

LAST_FOUR = "getpaid.virtualmerchant.cc_last_four"
APPROVAL_KEY = "getpaid.virtualmerchant.approval_code"

log = getLogger('getpaid.virtualmerchant')

class VirtualMerchantAdapter(object):
    interface.implements( interfaces.IPaymentProcessor )

    options_interface = IVirtualMerchantOptions

    _site = "www.myvirtualmerchant.com"
    _path = "/VirtualMerchant/processxml.do"

    def __init__(self, context):
        self.context = context

    def authorize(self, order, payment):
        xml = self.createXML(order, payment)
        xmlresponse = self.process(xml)
        
        if not xmlresponse.find('ssl_result') is None:
            log.info('Received a response from the Virtual Merchant site')
            if xmlresponse.find('ssl_result').text == '0':
                log.info('Transaction was approved')
                annotation = IAnnotations( order )
                annotation[ interfaces.keys.processor_txn_id ] = xmlresponse.find('ssl_txn_id').text
                annotation[ LAST_FOUR ] = payment.credit_card[-4:]
                annotation[ APPROVAL_KEY ] = xmlresponse.find('ssl_approval_code').text
                order.user_payment_info_trans_id = xmlresponse.find('ssl_txn_id').text
                return interfaces.keys.results_success
            else:
                log.error("Transaction wasn't successful")
                return xmlresponse.find('ssl_result_message').text
        
        error = xmlresponse.find('errorMessage').text
        log.error("There was an error: %s" % error)
        return error

    def capture(self, order, amount):
        annotations = IAnnotations(order)
        trans_id = annotations[interfaces.keys.processor_txn_id]
        if annotations.has_key(APPROVAL_KEY):
            annotation = IAnnotations( order )
            if annotation.get( interfaces.keys.capture_amount ) is None:
                annotation[ interfaces.keys.capture_amount ] = amount
            else:
                annotation[ interfaces.keys.capture_amount ] += amount            
            return interfaces.keys.results_success

        return result.response_reason

    def createXML(self, order, payment):
        """Create the xml to be sent to Virtual Merchant"""
        merchantid = IVirtualMerchantOptions(self.context).merchant_id
        if merchantid == '':
            log.error('No Merchant ID has been set in GetPaid, please set one.')
        merchantpin = IVirtualMerchantOptions(self.context).merchant_pin
        if merchantpin == '':
            log.error('No Merchant PIN has been set in GetPaid, please set one.')
        userid = IVirtualMerchantOptions(self.context).merchant_user_id
        if userid == '':
            userid = merchantid
        billing = order.billing_address
        amount = order.getTotalPrice()
        contact = order.contact_information
        order_id = order.getOrderId()
        names = payment.name_on_card.split()
        firstname = names[0]
        if len(names) > 1:
            lastname = names[-1]
        else:
            lastname = ''

        expiration_date = ''
        if hasattr(payment.cc_expiration, 'strftime'):
            expiration_date = payment.cc_expiration.strftime('%m%y')
        else:
            # If cc_expiration is not of type date, then it should be 
            # a string like this: '2011-08-03 00:00'
            # This is a bug in getpaid.formgen's single page checkout
            # and the correct fix is to swap out it's expiration date
            # widget with one that returns a date.
            yearMonthDay = payment.cc_expiration.split(' ')[0].split('-')
            _date = date(int(yearMonthDay[0]), 
                         int(yearMonthDay[1]), 
                         int(yearMonthDay[2]))
            expiration_date = _date.strftime('%m%y')
            
        getpaidoptions = IGetPaidManagementPaymentOptions(self.context)
        if getpaidoptions.store_name:
            storename = getpaidoptions.store_name
        else:
            storename = ''

        options = dict(
            ssl_merchant_id = merchantid,
            ssl_user_id = userid,
            ssl_pin = merchantpin,
            ssl_transaction_type = 'ccsale',         
            ssl_card_number = payment.credit_card,
            ssl_exp_date = expiration_date,
            ssl_amount = str(amount),
            ssl_sales_tax = '0.00',
            ssl_cvv2cvc2_indicator = '1',
            ssl_cvv2cvc2 = payment.cc_cvc,
            ssl_invoice_number = order_id,
            credit = 'Credit to '+storename,
            ssl_credit_card_type = payment.credit_card_type,
            ssl_first_name = firstname,
            ssl_last_name = lastname,
            ssl_avs_address = billing.bill_first_line,
            ssl_city = billing.bill_city,
            ssl_state = billing.bill_state,
            ssl_avs_zip = billing.bill_postal_code,
            ssl_phone = payment.bill_phone_number,
            ssl_email = contact.email
            )
        if billing.bill_second_line:
            options['ssl_address2'] = billing.bill_second_line
        # This ensures test credit card numbers return APPROVED
        if config.TESTING:
            options['ssl_test_mode'] = 'TRUE'

        xml = Element('txn')
        for key, value in options.items():
            subelement = SubElement(xml, key)
            subelement.text = value
        return xml
    
    def refund(self, order, amount):
        return "Not implemented"
    
    def process(self, xml):
        """Initiate an SSL connection and return the
        xmlresponse
        """
        conn = ssl.HTTPSConnection(self._site)

        # setup the HEADERS
        log.info('Setting up request headers')
        conn.putrequest('GET', self._path+'?xmldata='+quote(tostring(xml)))
        conn.putheader('Content-Type', 'text/xml')
        conn.endheaders()

        log.info('Getting the response from the Virtual Merchant site')
        result = conn.getresponse().read()
        xmlresponse = fromstring(result)
        
        return xmlresponse        