"""
$Id$

vocabularies for getpaid
"""

from zope import component

from zope.schema import vocabulary
from getpaid.core import interfaces, cart

from Products.CMFCore.utils import getToolByName


def PaymentMethods( context ):
    adapters = component.getAdapters( (context,), interfaces.IPaymentProcessor )
    payment_names = set( [ n for n,a in adapters] )
    return vocabulary.SimpleVocabulary.fromValues( payment_names )    

def ContentTypes( context ):
    # context is actually a preferences object, dig another level to get to the adapted context
    # which is acq wrapped.
    portal_types = getToolByName( context.context, 'portal_types' )
    terms = []
    # hmmm..
    types = filter( lambda x: x.global_allow, portal_types.objectValues() )

    for type in portal_types.objectValues():
        terms.append(
            vocabulary.SimpleTerm( type.getId(), title=type.title_or_id() )
            )
    terms.sort( lambda x,y: cmp( x.title, y.title ) )

    return vocabulary.SimpleVocabulary( terms )

def TaxMethods( context ):
    return vocabulary.SimpleVocabulary.fromValues( ("None",) )

def ShippingMethods( context ):
    return vocabulary.SimpleVocabulary.fromValues( ("None",) )


    

    
