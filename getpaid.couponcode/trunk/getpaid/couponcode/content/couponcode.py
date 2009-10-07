"""Definition of the CouponCode content type
"""

from zope.interface import implements, directlyProvides

from Products.Archetypes import atapi
from Products.Archetypes.utils import DisplayList
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from Products.CMFCore.utils import getToolByName

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
        vocabulary = 'getPloneContentTypes',
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

schemata.finalizeATCTSchema(CouponCodeSchema, moveDiscussion=False)

class CouponCode(base.ATCTContent):
    """CouponCode"""
    implements(ICouponCode)

    meta_type = "CouponCode"
    schema = CouponCodeSchema

    def getPloneContentTypes(self):
        ptool = getToolByName(self, 'portal_types')
        types = ptool.listTypeInfo()
        types_list = []
        properties = getToolByName(self, 'portal_properties')
        types_not_searched = set( properties.site_properties.types_not_searched )
        for item in types:
            if item.id in types_not_searched:
                continue
            title = item.title
            if title:
                types_list.append((item.id, title))
        types_list.sort(lambda x, y: cmp(x[1].lower(), y[1].lower()))  
        return DisplayList(((types_list)))

atapi.registerType(CouponCode, PROJECTNAME)
