from zope.interface import implements
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName

from getpaid.couponcode.interfaces import IValidateCouponCode

class ValidateCouponCode(BrowserView):
    """a view class that creates a new CustomHSVocabularyTerm in an ATVocabularyManager vocabulary.
    """
    
    implements(IValidateCouponCode)
    
    def validate_couponcode(self, couponcode):
        valid = False
        if couponcode:
            valid = True
        if valid:
            message = "Need logic to add coupon to cart. CouponCode: " + couponcode
            status = 'success'
        else:
            message = "Need logic to add coupon to cart. Either the code isn't valid given the items in your cart or it has expired."
            status = 'error'
        return """<div class="portalMessage %s">%s</div>""" % (status, message)
