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

from interfaces import IVirtualMerchantOptions

from elementtree.ElementTree import Element, SubElement, tostring, fromstring
from datetime import date
from logging import getLogger
import urllib2

LAST_FOUR = "getpaid.virtualmerchant.cc_last_four"
APPROVAL_KEY = "getpaid.virtualmerchant.approval_code"

log = getLogger('getpaid.virtualmerchant')

class VirtualMerchantAdapter(object):
    interface.implements( interfaces.IPaymentProcessor )

    options_interface = IVirtualMerchantOptions

    _site = "https://www.myvirtualmerchant.com/VirtualMerchant/processxml.do"

    def __init__(self, context):
        self.context = context

    def authorize(self, order, payment):
        merchantid = IVirtualMerchantOptions(self.context).merchant_id
        if merchantid == '':
            log.error('No Merchant ID has been set in GetPaid, please set one.')
        merchantpin = IVirtualMerchantOptions(self.context).merchant_pin
        if merchantpin == '':
            log.error('No Merchant PIN has been set in GetPaid, please set one.')
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
            
        options = dict(
            ssl_merchant_id = merchantid,
            ssl_user_id = merchantid,
            ssl_pin = merchantpin,
            ssl_transaction_type = 'ccsale',         
            ssl_card_number = payment.credit_card,
            ssl_exp_date = expiration_date,
            ssl_amount = str(amount),
            ssl_sales_tax = '0.00',
            ssl_cvv2cvc2_indicator = '1',
            ssl_cvv2cvc2 = payment.cc_cvc,
            ssl_invoice_number = order_id,
            ssl_customer_code = '',
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
        
        xml = self.createXML( options )
        url = self._site+'?xmldata='+tostring(xml)
        result = urllib2.urlopen(url)
        xmlresponse = fromstring(result.read())
        import pdb;pdb.set_trace()
        
        if xmlresponse.find('ssl_result'):
            if xmlresponse.find('ssl_result').text == '0':
                annotation = IAnnotations( order )
                annotation[ interfaces.keys.processor_txn_id ] = xmlresponse.find('ssl_txn_id').text
                annotation[ LAST_FOUR ] = payment.credit_card[-4:]
                annotation[ APPROVAL_KEY ] = xmlresponse.find('ssl_approval_code').text
                order.user_payment_info_trans_id = xmlresponse.find('ssl_txn_id').text
                return interfaces.keys.results_success
            else:
                return xmlresponse.find('ssl_result_message').text
        
        return xmlresponse.find('errorMessage').text


    def createXML( self, options ):
        "Create the xml to be sent to Virtual Merchant"
        xml = Element('txn')
        for key, value in options.items():
            subelement = SubElement(xml, key)
            subelement.text = value
        return xml
    
    def capture( self, order, amount ):

        annotations = IAnnotations( order )
        trans_id = annotations[ interfaces.keys.processor_txn_id ]
        approval_code = annotations[ APPROVAL_KEY ]
        
        result = self.processor.captureAuthorized(
            amount = str(amount),
            trans_id = trans_id,
            approval_code = approval_code,
            )

        if result.response == SUCCESS:
            annotation = IAnnotations( order )
            if annotation.get( interfaces.keys.capture_amount ) is None:
                annotation[ interfaces.keys.capture_amount ] = amount
            else:
                annotation[ interfaces.keys.capture_amount ] += amount            
            return interfaces.keys.results_success

        return result.response_reason
    
    def refund( self, order, amount ):

        annotations = IAnnotations( order )
        trans_id = annotations[ interfaces.keys.processor_txn_id ]
        last_four = annotations[ LAST_FOUR ]
        
        result = self.processor.credit(
            amount = str( amount ),
            trans_id = trans_id,
            card_num = last_four
            )
        
        if result.response == SUCCESS:
            annotation = IAnnotations( order )
            if annotation.get( interfaces.keys.capture_amount ) is not None:
                annotation[ interfaces.keys.capture_amount ] -= amount                        
            return interfaces.keys.results_success
        
        return result.response_reason
    
    @property
    def processor( self, xml):
        server = self._site
        return server
