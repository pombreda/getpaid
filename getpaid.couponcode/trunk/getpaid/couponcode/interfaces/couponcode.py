from zope.interface import Interface

from getpaid.couponcode import couponcodeMessageFactory as _


class ICouponCode(Interface):
    """CouponCode"""


class IValidateCouponCode(Interface):
    """ Validate CouponCode """


class ICouponCodeUtils(Interface):
    """ Coupon Code Utils"""

