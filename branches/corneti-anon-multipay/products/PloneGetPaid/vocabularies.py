"""
$Id$

vocabularies for getpaid
"""

from zope import component
from zope.interface import implements
from zope.app import zapi
from os import path

from zope.schema import vocabulary
from getpaid.core import interfaces

from Products.PloneGetPaid.CountriesStatesParser import CountriesStatesParser
from Products.PloneGetPaid.interfaces import ICountriesStates

from Products.CMFCore.utils import getToolByName

def PaymentMethods( context ):
    # context is the portal config options, whose context is the portal
    adapters = component.getAdapters( (context.context,), interfaces.IPaymentProcessor )
    payment_names = set( map(unicode, [ n for n,a in adapters]) )
    return vocabulary.SimpleVocabulary.fromValues( payment_names )    

def ContentTypes( context ):
    # context is actually a preferences object, dig another level to get to the adapted context
    # which is acq wrapped.
    portal_types = getToolByName( context.context, 'portal_types' )
    terms = []
    # hmmm..
    types = filter( lambda x: x.global_allow, portal_types.objectValues() )

    properties = getToolByName( context.context, 'portal_properties')
    types_not_searched = set( properties.site_properties.types_not_searched )

    for type in portal_types.objectValues():
        if type.getId() in types_not_searched:
            continue
        terms.append(
            vocabulary.SimpleTerm( unicode(type.getId()), title=unicode(type.title_or_id()) )
            )

    terms.sort( lambda x,y: cmp( x.title, y.title ) )

    return vocabulary.SimpleVocabulary( terms )

def TaxMethods( context ):
    return vocabulary.SimpleVocabulary.fromValues( (u"None",) )

def ShippingMethods( context ):
    return vocabulary.SimpleVocabulary.fromValues( (u"None", u"Flat Rate Shipping") )

def CreditCards( context ):
    return vocabulary.SimpleVocabulary.fromValues( (u"Visa", u"Mastercard", u"Discover", u"American Express") )

def WeightUnits( context ):
    return vocabulary.SimpleVocabulary.fromValues( (u"Pounds",) )

def Currencies( context ):
    return vocabulary.SimpleVocabulary.fromValues( (u"US Dollars",) )

def MerchantNotificationChoices( context ):
    return vocabulary.SimpleVocabulary.fromItems(
        [
        (u"Do not send merchant email notification of a completed transaction" ,u"no_notification"),
        (u"Send merchant email notification when a transaction happens", u"notification"),
        #("Send merchant encrypted email notification when a transaction happens", u"encrypted_notification")]
        ]
        )

def CustomerNotificationChoices( context ):
    return vocabulary.SimpleVocabulary.fromItems(
        [
        (u"Do not send customer email notification of a completed transaction", u"no_notification"), 
        (u"Send customer email notification of a completed transaction", u"notification")    
        ]
        )                                                

class TitledVocabulary(vocabulary.SimpleVocabulary):
    def fromTitles(cls, items, *interfaces):
        """Construct a vocabulary from a list of (value,title) pairs.

        The order of the items is preserved as the order of the terms
        in the vocabulary.  Terms are created by calling the class
        method createTerm() with the pair (value, title).

        One or more interfaces may also be provided so that alternate
        widgets may be bound without subclassing.
        """
        terms = [cls.createTerm(value,value,title) for (value,title) in items]
        return cls(terms, *interfaces)
    fromTitles = classmethod(fromTitles)

class CountriesStatesFromFile(object):
    """Countries utility that reads data from a file
    """
    implements(ICountriesStates)

    _noValues = [(u'(no values)',u'(no values)')]

    def __init__(self):
        iso3166_path = path.join(path.dirname(__file__), 'iso3166')
        self.csparser = CountriesStatesParser(iso3166_path)
        self.csparser.parse()

    def countries(self):
        return self.csparser.getCountriesNameOrdered()
    countries = property(countries)

    def states(self, country=None):
        if country is None:
            return self.allStates()
        states = self.csparser.getStatesOf(country)
        if len(states) == 0:
            return self._noValues
        return states

    def allStates(self):
        return self.csparser.getStatesOfAllCountries() + self._noValues

def Countries( context ):
    utility = zapi.getUtility(ICountriesStates)
    return TitledVocabulary.fromTitles(utility.countries)

def States( context ):
    utility = zapi.getUtility(ICountriesStates)
    return TitledVocabulary.fromTitles(utility.states())

