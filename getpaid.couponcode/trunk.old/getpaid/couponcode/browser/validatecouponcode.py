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
               * has not yet been applied
               * is able to be used if multiple coupons already applied
               * is not expired
               * effective date has already passed
               * has required items in cart
            if valid, adds coupon to cart, otherwise alerts user
        """
        valid = False
        if couponcode:
            pc = getToolByName(self.context, 'portal_catalog')
            res = pc.unrestrictedSearchResults(portal_type="CouponCode", 
                     getCouponCode=couponcode,)
            message = "The code isn’t valid given the items in your cart or it has expired."
            if len(res) > 0:
                coupon = res[0]
                if not self.couponAlreadyExists(couponcode) and \
                   not self.checkCouponExpired(coupon) and \
                   self.checkCouponEffective(coupon) and \
                   self.checkRequiredItemsInCart(coupon):
                     valid = True
        else:
            message = "Please input a coupon code."
        if not valid:
            return """<div class="portalMessage error">%s</div>""" % (message)
        else:
            return coupon.getObject().absolute_url()
    
    def checkCouponExpired(self, coupon):
        ''' returns True if coupon is expired '''
        now = DateTime()
        expiration_date = coupon.getCouponExpirationDate
        if not expiration_date or now < expiration_date or now.Date() == expiration_date.Date(): 
            return False
        return True
        
    def checkCouponEffective(self, coupon):
        ''' returns False if coupon is not yet effective '''
        now = DateTime()
        effective_date = coupon.getCouponEffectiveDate
        if not effective_date or now > effective_date or now.Date() == effective_date.Date():
            return True
        return False
        
    def checkRequiredItemsInCart(self, coupon):
        ''' returns False is the required items are not in the cart '''
        required_types = set(coupon.getCouponRequiredItemTypes)
        if len(required_types) == 0:
            return True
        cart = getUtility(IShoppingCartUtility).get(self.context) or {}
        cart_items = cart.values()
        for item in cart_items:
            ref_obj = item.resolve()
            if ref_obj:
                ref_type = ref_obj.portal_type
                if ref_type in required_types:
                    required_types.discard(ref_obj.portal_type)
        if len(required_types) == 0:
            return True
        return False

    def couponAlreadyExists(self, couponcode):
        ''' returns True if this coupon already been applied 
            or multiple coupons have already been applied and the
            allowMultipleCoupons property is set to False
        '''
        cart = getUtility(IShoppingCartUtility).get(self.context) or {}
        pprops = getToolByName(self, 'portal_properties')
        cart_items = cart.values()
        for item in cart_items:
            ref_obj = item.resolve()
            if ref_obj and \
               ref_obj.portal_type == "CouponCode":
               if pprops is not None:
                   cc_props = getattr(pprops, 'couponcode_properties', None)
                   if cc_props and \
                      cc_props.hasProperty('allowMultipleCoupons') and \
                      cc_props.getProperty('allowMultipleCoupons') == False:
                       return True
               if ref_obj.getCouponCode().lower() == couponcode.lower():
                    return True
        return False

