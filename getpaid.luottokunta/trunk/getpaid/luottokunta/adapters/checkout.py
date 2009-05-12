from Products.PloneGetPaid.browser.checkout import CheckoutController
#from getpaid.luottokunta.interfaces import ILuottokuntaCheckoutController
from getpaid.luottokunta.interfaces import ILuottokuntaWizard
from zope.interface import implements
from zope.component import adapts
from getpaid.wizard.interfaces import IWizardController

class LuottokuntaCheckoutController(CheckoutController):

#    implements(IWizardController)
#    adapts(ILuottokuntaWizard)

    steps = ['checkout-address-info', 'checkout-select-shipping', 'checkout-luottokunta-pay']

#class LuottokuntaCheckoutController(object):

#    implements(ILuottokuntaCheckoutController)
#    adapts(CheckoutController)

#    def __init__(self, context):
#        self.context = context

#        self.steps = ['checkout-address-info', 'checkout-luottokunta-pay']
