from base import FunctionalTestCase, VARIANTS_TEXT

from getpaid.atshop.variation import Variation

class ListingTestCase(FunctionalTestCase):
    """ Test listing of the products.
    """


    def setupProducts(self, count):

        self.loginAsPortalOwner()

        self.portal.invokeFactory("Folder", "folder")

        self.portal.folder.setLayout("product_listing")

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

    def render(self):
        """ Check that listing page renders without exceptions """

        browser = self.browser
        browser.open(self.portal.folder.absolute_url() )

        self.assertTrue("Foobar" in browser.contents)
        self.assertTrue("10.00" in broser.contents)

    def test_folder_has_product_listing_layout(self):
        """ Check that product_listing layout is available for folders

        """
        self.loginAsPortalOwner()
        self.portal.invokeFactory("Folder", "folder")

        layouts = self.portal.folder.getAvailableLayouts()
        # Rip ids from tuples
        ids = [ layout[0] for layout in layouts ]

        self.assertTrue("product_listing" in ids)

    def test_zero(self):
        """ Test list rendering with 0 items """
        self.setupProducts(0)
        self.render()

    def test_one(self):
        """ Test list rendering with 1 items """
        self.setupProducts(1)
        self.render()

    def test_many(self):
        """ Test list rendering with 2 items """
        self.setupProducts(2)
        self.render()

    def test_with_image(self):
        """ Render product listing with one image on an item """
        self.setupProducts(1)
        self.portal.folder.product0.invokeFactory("Image", "testimage")
        self.render()


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(ListingTestCase))
    return suite
