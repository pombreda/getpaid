from base import FunctionalTestCase, VARIANTS_TEXT

from getpaid.variantsproduct.variation import Variation

class BuyPortletFunctionalTestCase(FunctionalTestCase):
    """ Test variant product shopping functionality """

    def test_buy_normal(self):

        self.loginAsPortalOwner()
        self.portal.invokeFactory("MultiImageProduct", "product")

        browser = self.browser
        browser.open(self.portal.product.absolute_url() )

        # Check that shippable portlet is visible
        browser.getLink('Add to Cart').click()

    def test_buy_variant(self):

        self.loginAsPortalOwner()
        self.portal.invokeFactory("VariantProduct", "product")

        self.portal.product.setVariations(VARIANTS_TEXT)

        browser = self.browser
        self.browser.open(self.portal.product.absolute_url() )

        # Check that shippable portlet is visible
        browser.getControl("sku").value = "t-shirt-s"
        browser.getLink('Add to Cart').click()



def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(BuyPortletFunctionalTestCase))
    return suite
