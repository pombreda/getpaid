from zope.interface import implements
from Products.Five.browser import BrowserView

from getpaid.couponcode.interfaces import ICouponCodeUtils

class CouponCodeUtils(BrowserView):
    """a view class that creates a new CustomHSVocabularyTerm in an ATVocabularyManager vocabulary.
    """
    
    implements(ICouponCodeUtils)
    
    def getCouponCodeItems(self, cart):
        results = []
        if cart:
            k = 0
            for payable_line in cart.values():
                ref_obj = payable_line.resolve()
                if ref_obj and ref_obj.portal_type == 'CouponCode':
                    results.append(k)
                k += 1
        return results
