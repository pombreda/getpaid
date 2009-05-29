from getpaid.vcs import _
from zope.schema import vocabulary

def serverUrlsChoices( context ):
    return vocabulary.SimpleVocabulary.fromItems(
        [(_("Production Server"), u"https://www.vcs.co.za/vvonline/ccform.asp"),])

def currencyChoices( context ):
    return vocabulary.SimpleVocabulary.fromItems(
        [(_(u"SOUTH AFRICAN RAND"), u"zar")])
