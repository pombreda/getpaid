from Products.Five.utilities.marker import mark
from Products.PloneGetPaid.interfaces import IBuyableMarker
from getpaid.core.interfaces import IBuyableContent

def makeCouponCodeBuyable(couponcode_obj, event):
    """ Ensure the coupon code item is buyable
    """
    if not IBuyableMarker.providedBy(couponcode_obj):
        mark(couponcode_obj, IBuyableMarker)
    adapted = IBuyableContent(couponcode_obj)
    price = float('-' + couponcode_obj.getCouponAmount())
    adapted.setProperty('price', price)

