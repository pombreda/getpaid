"""Definition of the CouponCode content type
"""

from zope.interface import implements, directlyProvides

from Products.Archetypes import atapi
from Products.Archetypes.utils import DisplayList
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from Products.CMFCore.utils import getToolByName
from Products.PloneGetPaid import interfaces

from getpaid.couponcode import couponcodeMessageFactory as _
from getpaid.couponcode.interfaces import ICouponCode
from getpaid.couponcode.config import PROJECTNAME

CouponCodeSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

    atapi.StringField(
        'couponCode',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Coupon Code"),
            description=_(u""),
        ),
        required=True,
    ),


    atapi.FixedPointField(
        'couponAmount',
        storage=atapi.AnnotationStorage(),
        widget=atapi.DecimalWidget(
            label=_(u"Amount to remove from the cart"),
            description=_(u""),
        ),
        required=True,
        validators=('isDecimal'),
    ),


    atapi.DateTimeField(
        'couponEffectiveDate',
        storage=atapi.AnnotationStorage(),
        widget=atapi.CalendarWidget(
            label=_(u"Effective Date"),
            description=_(u"If not entered, the creation date will be used."),
        ),
        validators=('isValidDate'),
        with_time = False,
    ),


    atapi.DateTimeField(
        'couponExpirationDate',
        storage=atapi.AnnotationStorage(),
        widget=atapi.CalendarWidget(
            label=_(u"Expiration Date"),
            description=_(u"If not entered, it will be assumed the coupon never expires."),
        ),
        validators=('isValidDate'),
        with_time = False,
    ),

    atapi.LinesField(
        'couponRequiredItemTypes',
        storage=atapi.AnnotationStorage(),
        vocabulary = 'getBuyableContentTypes',
        widget=atapi.MultiSelectionWidget(
            label=_(u"Required Item Types"),
            description=_(u"What type of item(s) are required to be in the cart for this coupon to be valid? If nothing is selected, it is assumed the discount can apply to anything on the site."),
        ),
    ),


))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

CouponCodeSchema['title'].storage = atapi.AnnotationStorage()
CouponCodeSchema['description'].storage = atapi.AnnotationStorage()
CouponCodeSchema['relatedItems'].widget.visible = False

schemata.finalizeATCTSchema(CouponCodeSchema, moveDiscussion=False)

class CouponCode(base.ATCTContent):
    """CouponCode"""
    implements(ICouponCode)

    meta_type = "CouponCode"
    schema = CouponCodeSchema

    def getBuyableContentTypes(self):
        portal = getToolByName(self, 'portal_url').getPortalObject()
        ptool = getToolByName(portal, 'portal_types')
        options = interfaces.IGetPaidManagementOptions(portal)
        buyable_types = options.buyable_types
        shippable_types = options.shippable_types
        buyable_list = [(i, i) for i in buyable_types] + \
                       [(i, i) for i in shippable_types \
                               if i not in buyable_types]
        return DisplayList(((buyable_list)))

atapi.registerType(CouponCode, PROJECTNAME)
