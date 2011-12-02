from Products.Five import BrowserView
from getpaid.core.interfaces import IOrderManager
from getpaid.ogone.interfaces import IOgoneStandardOptions
from logging import getLogger
from pprint import pformat
from zope.component import getUtility
import sha

logger = getLogger('getpaid.ogone')

class ValidatePaymentParameters(object):

    def createShaOutSignature(self):
        """
        Create the sha out signature based on the parameter in the request
        and the sha out password defined in the payment processor parameters
        """
        options = IOgoneStandardOptions(self.context)
        shaPassword = options.shaout
        checkdata = {}
        [checkdata.update({x.upper(): self.request.form[x]})
         for x in self.request.form.keys()]
        keys = checkdata.keys()
        keys.sort()
        shaObject = sha.new()
        for key in keys:
            if checkdata[key] and key not in ['SHASIGN']:
                shaObject.update(("%s=%s%s" % (key, checkdata[key],
                                               shaPassword)))
        hexString = shaObject.hexdigest()
        return hexString.upper()

    def validate(self):
        """
        Validate the SHA OUT signature
        """
        requestShaOut = self.request.get('SHASIGN')
        if not requestShaOut:
            return False
        return self.createShaOutSignature() == requestShaOut


class OgonePostProcessAccepted(BrowserView, ValidatePaymentParameters):
    """
    The Ogone payment has been accepted
    """

    def __call__(self):
        """
        We update the order information and returns the template
        """
        if not self.validate():
            raise Exception('Incorrect SHA OUT Signature')
    # According to ogone manual, status codes starting with 5 or 9 mean
    # something good
	if self.request.form['STATUS'][0] in '59':
	    log_cmd = logger.info
	else:
	    log_cmd = logger.warn
	log_cmd("Received async order update information: " +\
  	    pformat(self.request.form))
        orderId = self.request.orderID
        options = IOgoneStandardOptions(self.context)
        currency = options.currency
        orderManager = getUtility(IOrderManager)
        order = orderManager.get(orderId)
    # According to ogone manual, status code '9' means paid
	if self.request.form['STATUS'] == '9':
            order.finance_workflow.fireTransition("charge-charging")
        return 1


class OgonePostProcessCancelled(BrowserView, ValidatePaymentParameters):
    """
    The Ogone payment has been cancelled
    """

    def __call__(self):
        """
        We update the order information and returns the template
        """
        if not self.validate():
            raise 'Incorrect SHA OUT Signature'
        orderId = self.request.orderID
        options = IOgoneStandardOptions(self.context)
        currency = options.currency
        orderManager = getUtility(IOrderManager)
        order = orderManager.get(orderId)
        order.finance_workflow.fireTransition("decline-charging")
        return 1
