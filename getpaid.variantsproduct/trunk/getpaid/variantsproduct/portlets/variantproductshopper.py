from zope.interface import Interface
from zope.interface import implements

from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider

from zope import schema
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from getpaid.variantsproduct import variantsproductMessageFactory as _
from getpaid.variantsproduct.interfaces import IBuyableMarker, IVariantProduct

from getpaid.variantsproduct.currency import format_currency

from Products.PloneGetPaid.browser.portlets import base as getpaidbase



class IVariantProductShopper(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    cart_add_form_url = schema.TextLine()




class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IVariantProductShopper)

    def __init__(self):
        pass

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return u"Buy portlet"


class Renderer(getpaidbase.GetPaidRenderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    marker = IBuyableMarker

    render = ViewPageTemplateFile('variantproductshopper.pt')

    def variations(self):
        return self.context.getProductVariations()

    def has_variations(self):
        """
        @return: Does this product support varations
        """
        return IVariantProduct.providedBy(self.context)

    def cart_add_form_url(self):
        """
        @return: URL for form posts addindg this item to cart
        """
        return self.context.getCartAddFormURL()

    def price(self):
        return self.format_price(self.context.price)

    def format_price(self, value):
        return format_currency(value)

    def is_visible(self):
        """ Is the context object marked to be buyable using this portlet
        """
        return IBuyableMarker.providedBy(self.cotext)

# NOTE: If this portlet does not have any configurable parameters, you can
# inherit from NullAddForm and remove the form_fields variable.

class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(IVariantProductShopper)

    def create(self, data):
        return Assignment(**data)


# NOTE: IF this portlet does not have any configurable parameters, you can
# remove this class definition and delete the editview attribute from the
# <plone:portlet /> registration in configure.zcml

class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(IVariantProductShopper)
