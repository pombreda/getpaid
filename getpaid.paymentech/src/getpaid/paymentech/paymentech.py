from zope import interface
from zope.app.annotation.interfaces import IAnnotations

from getpaid.core import interfaces

from interfaces import IPaymentechOptions

import xml.dom.minidom
import zc.ssl

import httplib

CARD_SEC_VAL = ['Visa', 'Discover', 'Mastercard']
LAST_FOUR = "getpaid.paymentech.cc_last_four"
APPROVAL_KEY = "getpaid.paymentech.approval_code"

def createXMLFile(message_type, options, payment, order):
    """
    Creates the XML file to send to the Paymentech Interface
    """
    merchant_id = options.merchant_id
    if len(merchant_id) == 6:
        bin_number = "000001" # corresponds to 6 digit Salem Division Number
    else:
        bin_number = "000002" # corresponds to 12 digit PNS Merchant ID
    terminal_id = options.terminal_id
    card_number = payment.credit_card
    card_exp_date = payment.cc_expiration.strftime('%m%y') # MMYY
    card_sec_val = ""
    if payment.credit_card_type in CARD_SEC_VAL:
        card_sec_val = """<CardSecValInd>1</CardSecValInd>"""
    card_sec_value = payment.cc_cvc
    order_id = order.getOrderId()
    amount = str(order.getTotalPrice() * 100) # $50.00 should be sent as 5000
    xml_text = """\
<Request xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="Request_PTI42.xsd">
  <NewOrder>
    <IndustryType>EC</IndustryType>
    <MessageType>%(message_type)s</MessageType>
    <BIN>%(bin_number)s</BIN>
    <MerchantID>%(merchant_id)s</MerchantID>
    <TerminalID>%(terminal_id)s</TerminalID>
    <AccountNum>%(card_number)s</AccountNum>
    <Exp>%(card_exp_date)s</Exp>
    <CurrencyCode>840</CurrencyCode>
    <CurrencyExponent>2</CurrencyExponent>
    %(card_sec_val)s
    <CardSecVal>%(card_sec_value)s</CardSecVal>
    <CustomerProfileFromOrderInd>O</CustomerProfileFromOrderInd>
    <CustomerProfileOrderOverrideInd>NO</CustomerProfileOrderOverrideInd>
    <OrderID>%(order_id)s</OrderID>
    <Amount>%(amount)s</Amount>
  </NewOrder>
</Request>
""" % locals()
    
    dom = xml.dom.minidom.parseString(xml_text)
    data = dom.toxml('utf-8')
    return data

def getElement(result, tag_name):
    """
    Get the value corresponding to a xml tag
    """
    if result.getElementsByTagName(tag_name):
        node = result.getElementsByTagName(tag_name)[0]
        if node.childNodes:
            child_node = node.childNodes[0]
            return child_node.nodeValue
    return None

class PaymentechConnection(object):
    
    def __init__(self, data, server, options, timeout=None):
        self.server = server
        self.timeout = timeout
        self.data = data
        self.options = options
    
    def sendTransaction(self):
        """
        Creates the HTTPS/POST connection to the Paymentech server
        """
        conn = zc.ssl.HTTPSConnection(self.server, self.timeout)
        
        # setup the MIME HEADERS
        conn.putrequest('POST', '/authorize')
        conn.putheader('content-type', 'application/PTI41')
        conn.putheader('content-length', len(self.data))
        conn.putheader('content-transfer-encoding', 'text')
        conn.putheader('request-number', '1')
        conn.putheader('document-type', 'request')
        conn.putheader('merchant-id', self.options.merchant_id)
        conn.endheaders()
        
        conn.send(self.data)
        return conn.getresponse()

class PaymentechResult(object):
    
    def __init__(self, response):
        self.response = response
        result = xml.dom.minidom.parseString(self.response.read())
        # ProcStatus is the only element that is returned in all response scenarios
        self.proc_status = getElement(result, 'ProcStatus')
        self.approval_status = getElement(result, 'ApprovalStatus')
        self.trans_ref_num = getElement(result, 'TxRefNum')
        self.status_msg = getElement(result, 'StatusMsg')

class PaymentechAdapter(object):
    interface.implements(interfaces.IPaymentProcessor)

    options_interface = IPaymentechOptions

    _sites = dict(
        Production1 = "orbital1.paymentech.net:443",
        Production2 = "orbital2.paymentech.net:443",
        Test1 = "orbitalvar1.paymentech.net:443",
        Test2 = "orbitalvar2.paymentech.net:443",
        )

    def __init__(self, context):
        self.context = context
        self.options = IPaymentechOptions(self.context)
        self.server = self._sites.get(self.options.server_url)

    def authorize(self, order, payment):
        """
        Authorize the supplied information.
        This transaction type should be used for deferred billing transactions.
        """
        # A – Authorization request
        data = createXMLFile('A', self.options, payment, order)
        
        result = self.process(data, timeout=None)
        
        if result.proc_status == "0":
            annotation = IAnnotations(order)
            annotation[interfaces.keys.processor_txn_id] = result.trans_ref_num
            annotation[LAST_FOUR] = payment.credit_card[-4:]
            annotation[APPROVAL_KEY] = result.approval_status
            return interfaces.keys.results_success
        else:
            return result.status_msg

    def capture(self, order, amount):
        #AC – Authorization and Mark for Capture
        data = createXMLFile('AC', self.options, payment, order)
        
        result = self.process(data, timeout=None)
        
        if result.proc_status == "0":
            annotation = IAnnotations(order)
            if annotation.get(interfaces.keys.capture_amount) is None:
                annotation[interfaces.keys.capture_amount] = amount
            else:
                annotation[interfaces.keys.capture_amount] += amount            
            return interfaces.keys.results_success
        else:
            return result.status_msg
    
    def refund(self, order, amount):
        #R – Refund request
        data = createXMLFile('R', self.options, payment, order)
        
        result = self.process(data, timeout=None)
        
        if result.proc_status == "0":
            annotation = IAnnotations(order)
            if annotation.get(interfaces.keys.capture_amount) is not None:
                annotation[interfaces.keys.capture_amount] -= amount                        
            return interfaces.keys.results_success
        else:
            return result.status_msg

    def process(self, data, timeout):
        """
        creates a HTTPS request using SSL, sends the request
        and returns a response
        """
        conn = PaymentechConnection(data, self.server, self.options, timeout=None)
        response = conn.sendTransaction()
        return PaymentechResult(response)
