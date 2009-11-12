from zope import schema
from zope.interface import Interface
from getpaid.discount import discountMessageFactory as _
class IDiscountable(Interface):
    """
    Marker interface for the Discountable items
    """
    discount_title = schema.TextLine(title=_(u'Discount Title'),
                           required=True)
    
    discount_type = schema.Choice(title=_(u'Type of Discount'),
                                  values=[_(u'Dollars Off'), _(u'Percentage Off')],
                                  required=True)
    
    discount_value = schema.Float(title=_(u'Value of the discount'),
                                  required=True,)

class IDiscountableMarker(Interface):
    """
    Discount Interface
    """

class IBuyXGetXFreeable(Interface):
    """
    Marker interface for the BuyXGetXFreeable items
    """
    discount_title = schema.TextLine(title=_(u'Discount Title'),
                           required=True)
    
    number_to_buy = schema.Int(title=_(u'Number of items to buy'),
                                  required=True)
    
    number_free = schema.Int(title=_(u'Number of free items'),
                                  required=True)

class IBuyXGetXFreeableMarker(Interface):
    """
    Discount Interface
    """

class ICodeDiscountable(Interface):
    """
    Marker interface for the CodeDiscountable items
    """
    discount_title = schema.TextLine(title=_(u'Discount Title'),
                           required=True)

    discount_code = schema.TextLine(title=_(u'Discount Code'),
                           required=True)
    
    discounted_price = schema.Float(title=_(u'Price after Discount'),
                                  required=True,)


class ICodeDiscountableMarker(Interface):
    """
    Discount Interface
    """
