from base import FunctionalTestCase, VARIANTS_TEXT

from getpaid.atshop.variation import Variation

class ListingTestCase(FunctionalTestCase):
    """ Test rendering the product page.
    """


    def setupProducts(self, count):

        self.loginAsPortalOwner()

        self.portal.invokeFactory("Folder", "folder")

        for i in range(0, count):

            id = "product" + str(i)

            # Test different type products
            if i == 2:
                self.portal.folder.invokeFactory("VariantProduct", id)
            else:
                self.portal.folder.invokeFactory("MultiImageProduct", id)

            product = self.portal.folder[id]

            product.setTitle("Foobar")

            product.setWeight(0)
            product.setWeight_unit("kg")

            if product.portal_type == "MultiImageProduct":
                product.setPrice(10.00)
                product.setProduct_code("foobar")

    def render(self, product):
        """ Check that page renders without exceptions """

        browser = self.browser
        browser.open(product.absolute_url())

        self.assertTrue("Foobar" in browser.contents)

    def test_without_image(self):
        """ Render product listing with one image on an item """
        self.setupProducts(1)
        self.render(self.portal.folder.product0)

    def test_with_image(self):
        """ Render product listing with one image on an item """
        self.setupProducts(1)
        self.portal.folder.product0.invokeFactory("Image", "testimage")
        self.render(self.portal.folder.product0)

    def test_variant(self):
        self.setupProducts(3)
        self.render(self.portal.folder.product2)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(ListingTestCase))
    return suite
