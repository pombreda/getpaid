from zope.interface import implements
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from DateTime import DateTime

from getpaid.couponcode.interfaces import IValidateCouponCode
from getpaid.core.interfaces import IShoppingCartUtility
from zope.component import getUtility

class ValidateCouponCode(BrowserView):
    """a view class that creates a new CustomHSVocabularyTerm in an ATVocabularyManager vocabulary.
    """
    
    implements(IValidateCouponCode)
    
    def validate_couponcode(self, couponcode):
        """ ensures that coupon:
               * is not expired, 
               * effective date has already passed, 
               * has required items in cart
            if valid, adds coupon to cart
        """
        valid = False
        status = "error"
        message = ""
        if couponcode:
            # get coupon
            pc = getToolByName(self.context, 'portal_catalog')
            res = pc(portal_type="CouponCode", 
                     getCouponCode=couponcode, 
                     review_state='published')
            if len(res) > 0:
                coupon = res[0]
                import pdb; pdb.set_trace( )
                if self.couponAlreadyExists(couponcode):
                    message = "Coupon already applied."
                if self.checkCouponExpired(coupon):
                    message = "It has already expired."
                if not self.checkCouponEffective(coupon):
                    message = "It is not yet effective."
                eligible_items = self.checkRequiredItemsInCart(coupon)
                if not eligible_items:
                    message = "At least one of the following must be in the cart: " + str(coupon.getCouponRequiredItemTypes)
            else:
                message = "Coupon does not exist"
        else:
            message = "Please input a coupon code."
        if message:
            return """<div class="portalMessage %s">This coupon is not valid: %s</div>""" % (status, message)
        else:
            return coupon.getObject().absolute_url()
    
    def checkCouponExpired(self, coupon):
        ''' returns True if coupon is expired '''
        now = DateTime()
        expiration_date = coupon.getCouponExpirationDate
        if not expiration_date or now < expiration_date:
            return False
        return True
        
    def checkCouponEffective(self, coupon):
        ''' returns False if coupon is not yet effective '''
        now = DateTime()
        effective_date = coupon.getCouponEffectiveDate
        if not effective_date or now > effective_date:
            return True
        return False
        
    def checkRequiredItemsInCart(self, coupon):
        ''' returns False is the required items are not in the cart '''
        required_types = coupon.getCouponRequiredItemTypes
        still_required = set(required_types)
        if len(required_types) == 0:
            return True
        cart = getUtility(IShoppingCartUtility).get(self.context) or {}
        cart_items = cart.values()
        eligible_items = []
        for item in cart_items:
            ref_obj = item.resolve()
            if ref_obj:
                ref_type = ref_obj.portal_type
                if ref_type in required_types:
                    still_required.discard(ref_obj.portal_type)
                    eligible_items.append(item)
        if len(still_required) == 0:
            return eligible_items
        return False

    def couponAlreadyExists(self, couponcode):
        ''' returns True if coupon already exists '''
        cart = getUtility(IShoppingCartUtility).get(self.context) or {}
        cart_items = cart.values()
        for item in cart_items:
            ref_obj = item.resolve()
            if ref_obj:
                if ref_obj.portal_type == "CouponCode" and ref_obj.getCouponCode() == couponcode:
                    return True
        return False

