from base import TestCase, VARIANTS_TEXT

from getpaid.atshop.variation import Variation

from Products.validation.exceptions import ValidatorError

class ParseVariantDataTestCase(TestCase):
    """ Test parsing of variant input text """

    def test_good_input(self):
        line = u"tshirtxl; T-Shirt (XL); 30.00"
        variation = Variation.decode(line)

        self.assertEqual(variation.product_code, "tshirtxl")
        self.assertEqual(variation.title, "T-Shirt (XL)")
        self.assertEqual(variation.price, 30.00)

    def test_only_one_colum(self):

        line = u"tshirtxl; T-Shirt (XL)"

        try:
            variation = Variation.decode(line)
            raise AssertionError("Should be never reached")
        except ValidatorError:
            pass

    def test_bad_price(self):

        line = u"tshirtxl; T-Shirt (XL); 1+00"

        try:
            variation = Variation.decode(line)
            raise AssertionError("Should be never reached")
        except ValidatorError:
            pass

class GetProductVariantsTestCase(TestCase):
    """ Test getting variant data out of AT object """

    def test_get_variants(self):

        self.loginAsPortalOwner()

        self.portal.invokeFactory("VariantProduct", "product")

        self.portal.product.setVariations(VARIANTS_TEXT)
        variants = self.portal.product.getProductVariations()
        self.assertEqual(len(variants), 3)

    def test_get_variants_not_set(self):
        """ Check that we don't get error if variants field has not yet been set """

        self.loginAsPortalOwner()

        self.portal.invokeFactory("VariantProduct", "product")

        # By default we have 1 sample variation
        variants = self.portal.product.getProductVariations()
        self.assertEqual(len(variants), 1)

        self.portal.product.setVariations([])
        variants = self.portal.product.getProductVariations()
        self.assertEqual(len(variants), 0)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(ParseVariantDataTestCase))
    suite.addTest(makeSuite(GetProductVariantsTestCase))
    return suite
