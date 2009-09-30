"""

    Make our custom AT objects shippable.

    By default GetPaid buy portlet assumes payable, shippable, etc.
    information is held in magic storage.

    Our "designed-for-buying" content implements shippable data directly.

"""

__author__ = "Mikko Ohtamaa <mikko.ohtamaa@twinapex.com> http://www.twinapex.com"
__docformat__ = "epytext"
__license__ = "GPL"
__copyright__ = "2009 Twinapex Research"

def shippableAdapter(object ):
    """
    Shippable content adapter which reads price, value, etc. directly from AT object.

    Archetypes object itself should satisfy IShippableItem interface.
    """
    return object