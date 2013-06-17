# -*- coding: utf-8 -*-
"""

    Render product image browser.


"""

__author__ = "Mikko Ohtamaa <mikko.ohtamaa@twinapex.com> http://www.twinapex.com"
__docformat__ = "epytext"
__license__ = "GPL"
__copyright__ = "2009 Twinapex Research"


from AccessControl import getSecurityManager
from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.CMFCore import permissions


from getpaid.atshop import atshopMessageFactory as _

from getpaid.atshop.interfaces import IProductImageProvider

class IProductImagePreviewsView(Interface):
    """
    ProductImagePreviews view interface
    """

    def images():
        """ @return: List of product images as tuples:

                * Name

                * Image SRC URL

                * Link target URL

        """

    def canEditImage(image):
        """ Checks whether render edit link for an image.

        @return: True or False
        """

class ProductImagePreviewsView(BrowserView):
    """ Render all images associated with a buyable product.

    """
    implements(IProductImagePreviewsView)

    def images(self):
        return self._images

    def canEditImage(self, image):
        return getSecurityManager().checkPermission(permissions.ModifyPortalContent, image)

    def __call__(self):
        self.image_provider = IProductImageProvider(self.context)
        self._images = self.image_provider.getImages()

        return self.index()