"""Definition of the ProductImage content type
"""

from zope.interface import implements, directlyProvides

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from Products.ATContentTypes.content import image

from getpaid.atshop import atshopMessageFactory as _
from getpaid.atshop.interfaces import IProductImage
from getpaid.atshop.config import PROJECTNAME


ProductImageSchema = image.ATImageSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

ProductImageSchema['title'].storage = atapi.AnnotationStorage()
ProductImageSchema['description'].storage = atapi.AnnotationStorage()


schemata.finalizeATCTSchema(ProductImageSchema, moveDiscussion=False)

class ProductImage(image.ATImage):
    """Image associated withthe product.

    By default this is excluded from the navigation.
    """
    implements(IProductImage)

    meta_type = "ProductImage"
    schema = ProductImageSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(ProductImage, PROJECTNAME)
