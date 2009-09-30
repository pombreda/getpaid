"""Definition of the MultiImageProduct content type
"""

from zope.interface import implements, directlyProvides

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from getpaid.variantsproduct import variantsproductMessageFactory as _
from getpaid.variantsproduct.interfaces import IMultiImageProduct
from getpaid.variantsproduct.config import PROJECTNAME

from getpaid.variantsproduct.content import goodsschema

import getpaid.core.interfaces
import Products.PloneGetPaid.interfaces

MultiImageProductSchema = folder.ATFolderSchema.copy() + \
                          goodsschema.priceSchema.copy() + \
                          goodsschema.productDescriptionSchema.copy() + \
                          goodsschema.shippableSchema.copy()

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

MultiImageProductSchema['title'].storage = atapi.AnnotationStorage()
MultiImageProductSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(
    MultiImageProductSchema,
    folderish=True,
    moveDiscussion=False
)


class MultiImageProduct(folder.ATFolder):
    """Buyable product with multiple images"""
    implements(IMultiImageProduct)

    meta_type = "MultiImageProduct"
    schema = MultiImageProductSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # getpaid.core.interfaces.IShippableContent compatible accessors

    price = atapi.ATFieldProperty('price')

    weight = atapi.ATFieldProperty('weight')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-
    text = atapi.ATFieldProperty('text')

    product_code = atapi.ATFieldProperty('product_code')

    def getCartAddFormURL(self):
         return self.absolute_url() + "/@@getpaid-cart-add-simple"


atapi.registerType(MultiImageProduct, PROJECTNAME)
