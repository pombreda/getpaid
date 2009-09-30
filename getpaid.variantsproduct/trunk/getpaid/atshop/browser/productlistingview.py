"""

    Product listing view for folders and collections.

"""

__author__ = "Mikko Ohtamaa <mikko.ohtamaa@twinapex.com> http://www.twinapex.com"
__docformat__ = "epytext"
__license__ = "GPL"
__copyright__ = "2009 Twinapex Research"


from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from Products.ATContentTypes.interface import IATTopic

from getpaid.atshop import atshopMessageFactory as _

from getpaid.atshop.interfaces import IProductImageProvider

class IProductListingView(Interface):
    """
    View methods exposed to the template.
    """


class ProductListingView(BrowserView):
    """
    Summary view of the products in the current folder.
    """
    implements(IProductListingView)

    def __init__(self, context, request):
        self.context = context
        self.request = request


    def has_image(self, catalog_brain):
        """ Check whether the iterated item is product like and supports multiple images

        @return: True or False
        """

        # TODO: I don't think metadata supports interface checks...
        if catalog_brain["portal_type"] in ["MultiImageProduct", "VariantProduct"]:
            return True

        return False

    def get_image_tag(self, item):

        object = item.getObject()

        if IProductImageProvider.providedBy(object):
            image = object.getMainImage()
            return image.tag()

        return None


    def query(self, start, limit, contentFilter):
        """ Make catalog query for the folder listing.

        @param start: First index to query

        @param limit: maximum number of items in the batch

        @param contentFilter: portal_catalog filtering dictionary with index -> value pairs.

        @return: Products.CMFPlone.PloneBatch.Batch object
        """

        # Batch size
        b_size = limit

        # Batch start index, zero based
        b_start = start

        # We use different query method, depending on
        # whether we do listing for topic or folder
        if IATTopic.providedBy(self.context):
            # ATTopic like content
            # Call Products.ATContentTypes.content.topic.ATTopic.queryCatalog() method
            # This method handles b_start internally and
            # grabs it from HTTPRequest object
            return self.context.queryCatalog(contentFilter, batch=True, b_size=b_size)
        else:
            # Folder or Large Folder like content
            # Call CMFPlone(/skins/plone_scripts/getFolderContents Python script
            # This method handles b_start parametr internally and grabs it from the request object
            return self.context.getFolderContents(contentFilter, batch=True, b_size=b_size)

    def __call__(self):
        """ Render the content item listing.
        """

        # How many items is one one page
        limit = 3

        # Read the first index of the selected batch parameter as HTTP GET request query parameter
        start = self.request.get("b_start", 0)

        filter = {}

        # Perform portal_catalog query
        self.contents = self.query(start, limit, filter)

        # Return the rendered template (productcardsummaryview.pt), with content listing information filled in
        return self.index()


