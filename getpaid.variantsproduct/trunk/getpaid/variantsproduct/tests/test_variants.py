from base import TestCase

from getpaid.variantsproduct.variation import Variation

from Products.validation.exceptions import ValidatorError

class ParseVariantDataTestCase(TestCase):

    def test_good_input(self):
        line = u"tshirtxl; T-Shirt (XL); 30.00"
        variation = Variation.decode(line)

        self.assertEqual(variation.sku, "tshirtxl")
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

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(ParseVariantDataTestCase))
    return suite
