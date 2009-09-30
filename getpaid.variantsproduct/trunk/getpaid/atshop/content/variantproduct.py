"""Definition of the VariantProduct content type
"""

from zope.interface import implements, directlyProvides

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata


from getpaid.atshop import atshopMessageFactory as _
from getpaid.atshop.interfaces import IVariantProduct
from getpaid.atshop.config import PROJECTNAME

from getpaid.atshop.validators import VariationTextValidator

from getpaid.atshop.content import multiimageproduct
import getpaid.core.interfaces
import Products.PloneGetPaid.interfaces

from getpaid.atshop.variation import Variation

from getpaid.atshop.content import goodsschema

VariantProductSchema = folder.ATFolderSchema.copy()+ goodsschema.shippableSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-
    atapi.TextField(
        'text',
        storage=atapi.AnnotationStorage(),
        default="",
        widget=atapi.RichWidget(
            label=_(u"Product text"),
            description=_(u"Long text describing the product"),
        ),
    ),

    atapi.LinesField(
        'variations',
        storage=atapi.AnnotationStorage(),
        validators = (VariationTextValidator("Sane variations description"),),
        default = ["myitemcode; My Item; 0.00"],
        widget=atapi.LinesWidget(
            label=_(u"Variations"),
            description=_(u"Variations, one per, line. Line contains the following data separated by ; character: product_code; title; price. Use dot as decimal separator."),
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

    text = atapi.ATFieldProperty('text')

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

    def getCheapestPrice(self):
        variations = self.getProductVariations()

        if len(variations) == 0:
            return None

        prices = [ var.price for var in variations ]
        return min(prices)

atapi.registerType(VariantProduct, PROJECTNAME)
