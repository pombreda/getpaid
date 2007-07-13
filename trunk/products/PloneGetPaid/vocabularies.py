"""
$Id$

vocabularies for getpaid
"""

from zope import component

from zope.schema import vocabulary
from getpaid.core import interfaces, cart

from Products.CMFCore.utils import getToolByName

def PaymentMethods( context ):
    # context is the portal config options, whose context is the portal
    adapters = component.getAdapters( (context.context,), interfaces.IPaymentProcessor )
    payment_names = set( [ n for n,a in adapters] )
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
            vocabulary.SimpleTerm( type.getId(), title=type.title_or_id() )
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
    return vocabulary.SimpleVocabulary.fromItems( [("Do not send merchant email notification of a completed transaction" ,u"no_notification"),
                                                   ("Send merchant email notification when a transaction happens", u"notification"),
                                                   ("Send merchant encrypted email notification when a transaction happens", u"encrypted_notification")]
                                                )

def CustomerNotificationChoices( context ):
    return vocabulary.SimpleVocabulary.fromItems( [(u"Do not send customer email notification of a completed transaction", u"no_notification"), 
                                                   (u"Send customer email notification of a completed transaction", u"notification")    
                                                  ]
                                                )                                                
