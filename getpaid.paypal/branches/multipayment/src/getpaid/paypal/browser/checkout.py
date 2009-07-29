from Products.PloneGetPaid.browser.checkout import CheckoutReviewAndPay
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from getpaid.paypal.browser.paypalbutton import PaypalButtonView

class PayPalCheckoutReviewAndPay(CheckoutReviewAndPay, PaypalButtonView):
    template = ZopeTwoPageTemplateFile("templates/checkout-paypal-pay.pt")
