"""

    Zope vocabularies used by payment processors.


    E.g. used in the checkout schema.

"""


__author__ = "Mikko Ohtamaa <mikko.ohtamaa@twinapex.fi>"
__docformat__ = "epytext"

from zope import component
from zope.interface import implements
from zope.schema import vocabulary
import interfaces

from registry import paymentProcessorRegistry

def PaymentProcessors(context):
    """ List all registered payment processors.

    Mostly useful for validating form input.

    Vocabulary contains all payment processors, not just active ones.
    """
    return vocabulary.SimpleVocabulary.fromValues(paymentProcessorRegistry.getProcessors())


