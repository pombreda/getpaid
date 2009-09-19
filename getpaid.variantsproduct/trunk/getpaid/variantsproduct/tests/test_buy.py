from base import TestCase

from getpaid.variantsproduct.variation import Variation

class BuyTestCase(TestCase):

    def test_buy_variant(self):
        line = "tshirtxl; T-Shirt (XL); 30.00"
        variation = Variation.decode(line)

        self.assertEqual(variation.id, "tshirtxl")
        self.assertEqual(variation.title, "T-Shirt (XL)")
        self.assertEqual(variation.price, 30.00)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(ParseVariantDataTestCase))
    return suite
