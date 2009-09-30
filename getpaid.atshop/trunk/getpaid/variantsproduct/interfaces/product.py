from zope import schema
from zope.interface import Interface

class IBuyableMarker(Interface):
    """ Marker interface controlling whether variant specific buying portlet is shown next to the content """
