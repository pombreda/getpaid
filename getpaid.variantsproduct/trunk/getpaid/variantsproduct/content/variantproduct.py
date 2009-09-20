"""Definition of the VariantProduct content type
"""

from zope.interface import implements, directlyProvides

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata


from getpaid.variantsproduct import variantsproductMessageFactory as _
from getpaid.variantsproduct.interfaces import IVariantProduct
from getpaid.variantsproduct.config import PROJECTNAME

from getpaid.variantsproduct.validators import VariationTextValidator

from getpaid.variantsproduct.content import multiimageproduct
import getpaid.core.interfaces
import Products.PloneGetPaid.interfaces

from getpaid.variantsproduct.variation import Variation

from getpaid.variantsproduct.content import goodsschema

VariantProductSchema = folder.ATFolderSchema.copy()+ goodsschema.shippableSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

    atapi.LinesField(
        'variations',
        storage=atapi.AnnotationStorage(),
        validators = (VariationTextValidator("Sane variations description"),),
        widget=atapi.LinesWidget(
            label=_(u"Variations"),
            description=_(u"Variations, one per, line. Line contains the following data separated by ; character: product_code; title; price"),
        ),
    ),

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
    implements(IVariantProduct)

    meta_type = "VariantProduct"
    schema = VariantProductSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-
    variations = atapi.ATFieldProperty('variations')

    price = atapi.ATFieldProperty('price')

    weight = atapi.ATFieldProperty('weight')

    dimensions = atapi.ATFieldProperty('dimensions')

    def getProductVariations(self):
        """ Convert human input of variations one per line to Variation objects

        @return: Iterable of Variation objects available for this product
        """
        lines = self.getVariations()
        if lines == None:
            return None

        else:
            result = []

            for line in self.getVariations():

                line = line.strip()
                if line == "":
                    # Ignore empty lines
                    continue

                line = line.decode("utf-8")
                result.append(Variation.decode(line))

            return result

    def getProductVariationByProductCode(self, product_code):
        variations = self.getProductVariations()
        for variation in variations:
            if variation.product_code == product_code:
                return variation

        raise RuntimeError("No product variation by product_code:" + product_code)

    def getCartAddFormURL(self):
        return self.absolute_url() + "/@@getpaid-cart-add-variant"


atapi.registerType(VariantProduct, PROJECTNAME)
