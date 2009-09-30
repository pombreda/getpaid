"""

    AT validators specific to this product.

"""

__author__ = "Mikko Ohtamaa <mikko.ohtamaa@twinapex.com> http://www.twinapex.com"
__docformat__ = "epytext"
__license__ = "GPL"
__copyright__ = "2009 Twinapex Research"

import zope.interface

from Products.validation.interfaces.IValidator import IValidator
from Products.validation.exceptions import ValidatorError

from getpaid.atshop.variation import Variation


class VariationTextValidator(object):
    """ Validate that human input for variation text is correct """

    #zope.interface.implements(IValidator)
    __implements__ = IValidator

    def __init__(self, name, *args, **kw):
        self.name = name
        self.title = kw.get('title', name)
        self.description = kw.get('description', '')


    def __call__(self, value, *args, **kwargs):


        for line in value:

            line = line.strip()

            #print "Validating line:" + line
            if line == "":
                continue

            line = line.decode("utf-8")

            try:
                Variation.decode(line)
            except ValidatorError, e:
                return unicode(e) + u" Line is:" + line
        #print "All ok"
        return True