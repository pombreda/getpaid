"""Definition of the CouponCode content type
"""

from zope.interface import implements, directlyProvides

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from getpaid.couponcode import couponcodeMessageFactory as _
from getpaid.couponcode.interfaces import ICouponCode
from getpaid.couponcode.config import PROJECTNAME

CouponCodeSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

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

    #jessilfp title = atapi.ATFieldProperty('title')
    #jessilfp description = atapi.ATFieldProperty('description')
    
    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(CouponCode, PROJECTNAME)
