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

from getpaid.variantsproduct.variation import Variation


class VariationTextValidator(object):
    """ Validate that human input for variation text is correct """

    #zope.interface.implements(IValidator)
    __implements__ = IValidator

    def __call__(self, value):

        lines = value.split("\n")

        for line in lines:

            if line == "":
                continue

            line = line.decode("utf-8")

            try:
                Variation.decode(line)
            except ValidatorError, e:
                return e.message + " " + " Line is:" + line

        return True