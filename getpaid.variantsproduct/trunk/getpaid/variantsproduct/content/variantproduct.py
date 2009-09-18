"""Definition of the VariantProduct content type
"""

from zope.interface import implements, directlyProvides

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from getpaid.variantsproduct import variantsproductMessageFactory as _
from getpaid.variantsproduct.interfaces import IVariantProduct
from getpaid.variantsproduct.config import PROJECTNAME

import getpaid.core.interfaces
import Products.PloneGetPaid.interfaces

VariantProductSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

VariantProductSchema['title'].storage = atapi.AnnotationStorage()
VariantProductSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(
    VariantProductSchema,
    folderish=True,
    moveDiscussion=False
)

class VariantProduct(folder.ATFolder):
    """ Buyable physical good with variants of title and price and multiple images """
    implements(IVariantProduct,
              Products.PloneGetPaid.interfaces.IShippableMarker)

    meta_type = "VariantProduct"
    schema = VariantProductSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(VariantProduct, PROJECTNAME)
