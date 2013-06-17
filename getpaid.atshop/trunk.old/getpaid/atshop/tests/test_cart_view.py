# -*- coding: utf-8 -*-

from base import TestCase, VARIANTS_TEXT
from zope import component

from getpaid.atshop.variation import Variation

from Products.validation.exceptions import ValidatorError

from getpaid.atshop.price import get_price_text

from getpaid.atshop.variation import Variation
from getpaid.atshop.interfaces import IVariationItemFactory

import getpaid.core.interfaces

class CartStatusViewTestCase(TestCase):
    """ Test cart view rendering (not visible in the default setup) """
    
    def render(self):
        view = self.portal.restrictedTraverse("@@cart-status")
        view = view.__of__(self.portal)
        view()
        return view
    
    def buy(self):
        self.loginAsPortalOwner()

        self.portal.invokeFactory("VariantProduct", "product")

        self.portal.product.setVariations(VARIANTS_TEXT)

        # create a line item and add it to the car
        cart = self.create_cart()
        item_factory = component.getMultiAdapter((cart, self.portal.product), IVariationItemFactory )

        item = item_factory.create("t-shirt-s")
        

    def test_no_items(self):
        self.render()
    
    def test_has_items(self):
        self.buy()
        view = self.render()
        
        self.assertEqual(view.summary_text(), u"You have 1 items worth of 20.00 €")


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(CartStatusViewTestCase))
    return suite
