from base import TestCase, VARIANTS_TEXT

from zope import component

from getpaid.variantsproduct.variation import Variation
from getpaid.variantsproduct.interfaces import IVariationItemFactory

class VariantBuyTestCase(TestCase):
    """ Test variant product shopping functionality """

    def test_buy_variant(self):

        self.loginAsPortalOwner()

        self.portal.invokeFactory("VariantProduct", "product")

        self.portal.product.setVariations(VARIANTS_TEXT)

        # create a line item and add it to the car
        cart = self.create_cart()
        item_factory = component.getMultiAdapter((cart, self.portal.product), IVariationItemFactory )

        item = item_factory.create("t-shirt-s")

        self.assertEqual(item.cost, 20.00)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(VariantBuyTestCase))
    return suite
