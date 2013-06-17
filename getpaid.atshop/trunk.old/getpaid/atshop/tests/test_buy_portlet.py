from base import FunctionalTestCase, VARIANTS_TEXT

from getpaid.atshop.variation import Variation

class BuyPortletFunctionalTestCase(FunctionalTestCase):
    """ Test variant product shopping functionality.

    TODO: Finish this test implementation
    """


    def setupProduct(self):
        product = self.portal.product

        product.setTitle("Foobar")

        product.setWeight(0)
        product.setWeight_unit("kg")

        if product.portal_type == "MultiImageProduct":
            product.setPrice(0)
            product.setProduct_code("foobar")


    def xxx_test_buy_normal(self):

        browser = self.browser
        browser.open(self.portal.absolute_url() )

        # Check that shippable portlet is visible
        browser.getLink('Add to Cart').click()

    def xxx_test_buy_variant(self):

        self.loginAsPortalOwner()
        self.portal.invokeFactory("VariantProduct", "product")
        self.setupProduct()
        self.portal.product.setVariations(VARIANTS_TEXT)

        browser = self.browser
        self.browser.open(self.portal.product.absolute_url())

        # Check that shippable portlet is visible
        browser.getControl("product_code").value = "t-shirt-s"
        browser.getLink('Add to Cart').click()



def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(BuyPortletFunctionalTestCase))
    return suite
