from zope.i18nmessageid import MessageFactory

creditpublishMessageFactory = MessageFactory('getpaid.creditpublish')

# One little bit of ugly bootstrapping to get our indexable attributes
from catalog import getWeeksLeftPublished, getRepublishReminderSent 
from Products.CMFPlone.CatalogTool import registerIndexableAttribute 

registerIndexableAttribute('getWeeksLeftPublished', getWeeksLeftPublished)
registerIndexableAttribute('getRepublishReminderSent', getRepublishReminderSent)
