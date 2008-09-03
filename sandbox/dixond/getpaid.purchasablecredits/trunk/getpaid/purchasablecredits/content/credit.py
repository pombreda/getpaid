__author__  = 'Darryl Dixon <darryl.dixon@winterhouseconsulting.com>'
__docformat__ = 'plaintext'

from zope.interface import implements
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from Products.Archetypes.public import BaseContent, StringField, TextField, AnnotationStorage, StringWidget, TextAreaWidget, registerType, Schema, FixedPointField, DecimalWidget

from getpaid.purchasablecredits import purchasablecreditsMessageFactory as _
from getpaid.purchasablecredits.config import PROJECTNAME
from getpaid.purchasablecredits.interfaces import IPurchasableCredit

PurchasableCreditSchema = BaseContent.schema.copy() + Schema((

    StringField('title',
        accessor = 'Title',
        required = True,
        schemata = _(u"required"),
        searchable = True,
        storage = AnnotationStorage(),
        widget = StringWidget(
            description = _(u"Please enter the name of this type of credit"),
            label = _(u"Credit Name"),
        ),
    ),

    TextField('description',
        accessor = 'Description',
        allowable_content_types=('text/plain',),
        required = True,
        schemata = _(u"required"),
        searchable = True,
        storage = AnnotationStorage(),
        widget = TextAreaWidget(
            rows = 10,
            description = _(u"Please enter a description of this type of credit"),
            label = _(u"Credit Description"),
        ),
    ),

    FixedPointField('price',
        accessor = 'getPrice',
        required = True,
        widget = DecimalWidget(
            description = _(u"Enter the cost of this credit (format 00.00, omit the $ sign)"),
            label = _(u"Price of Credit"),
            thousands_commas = True,
            dollars_and_cents = True,
            size = 10,
        ),
    ),
))

class PurchasableCredit(BrowserDefaultMixin, BaseContent):
    implements(IPurchasableCredit)

    portal_type = 'PurchasableCredit'
    _at_rename_after_creation = True
    schema = PurchasableCreditSchema

registerType(PurchasableCredit, PROJECTNAME)
