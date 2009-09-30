"""

    Product image management.

"""

__author__ = "Mikko Ohtamaa <mikko.ohtamaa@twinapex.com> http://www.twinapex.com"
__docformat__ = "epytext"
__license__ = "GPL"
__copyright__ = "2009 Twinapex Research"

import zope.interface

from getpaid.variantsproduct.interfaces.multiimageproduct import IProductImageProvider

class FolderishProductImageProvider(object):
    """ Mix-in class which provide product image management functions.

    Assume the content itself is folderish and contained
    image objects are product images.
    """

    zope.interface.implements(IProductImageProvider)


    def __init__(self, context):
        self.context = context

    def getImages(self):
        """ Return sequence of images.

        Perform folder listing and filter image content from it.
        """

        images = self.context.listFolderContents(contentFilter={"portal_type" : "Image"})
        return images

    def getMainImage(self):

        images = self.getImages()
        if len(images) >= 1:
            return self.getImages()[0]
        else:
            return None