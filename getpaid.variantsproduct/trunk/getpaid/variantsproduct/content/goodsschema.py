"""

    Archetypes schematas for shoppaple goods.

"""

__author__ = "Mikko Ohtamaa <mikko.ohtamaa@twinapex.com> http://www.twinapex.com"
__docformat__ = "epytext"
__license__ = "GPL"
__copyright__ = "2009 Twinapex Research"

from Products.Archetypes import public as atapi

from getpaid.variantsproduct import variantsproductMessageFactory as _

from getpaid.core.interfaces import IShippableContent

WEIGHT_VOCABULARY = atapi.DisplayList()
WEIGHT_VOCABULARY.add(u"kq", "Kilograms")
WEIGHT_VOCABULARY.add(u"lbs", "Pounds")

#: Schema for products which have simple price
priceSchema = atapi.Schema((

    atapi.FloatField(
        'price',
        storage=atapi.AnnotationStorage(),
        widget=atapi.DecimalWidget(
            label=_(u"Price"),
            description=_(u"Item price in the shop currency unit"),
        ),
        required=True,
        validators=('isDecimal'),
    ),

))

productDescriptionSchema = atapi.Schema((

    atapi.StringField(
        'product_code',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Product code"),
            description=_(u"Inventory id for this product"),
        ),
    ),

    atapi.TextField(
        'text',
        storage=atapi.AnnotationStorage(),
        widget=atapi.RichWidget(
            label=_(u"Product text"),
            description=_(u"Long text describing the product"),
        ),
    ),

))



# Archetypes schema matching getpaid.core.interfaces.IShippableContent

shippableSchema = atapi.Schema((

    atapi.StringField(
        'dimensions',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Dimensions"),
            description=_(u"Free text description of the dimensions of the packed product"),
        ),
    ),

    atapi.FloatField(
        'weight',
        storage=atapi.AnnotationStorage(),
        widget=atapi.DecimalWidget(
            label=_(u"Weight"),
            description=_(u"Weight of the item for shipping"),
        ),
        default=_(u"0"),
        validators=('isDecimal'),
    ),

    atapi.StringField(
        "weight_unit",
        storage=atapi.AnnotationStorage(),
        vocabulary = WEIGHT_VOCABULARY,
        default=u"kg",
        widget=atapi.SelectionWidget(
            label=_(u"Weight unit"),
            description=_(u"Weight of the item for shipping"),
        ),
    )
))

