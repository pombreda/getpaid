from zope.interface import implements
from zope.component import adapts

from archetypes.schemaextender.interfaces import ISchemaExtender
from archetypes.schemaextender.field import ExtensionField

from Products.Archetypes import atapi

from interfaces import IOneWeekCreditPublishedContent
from getpaid.creditpublish import creditpublishMessageFactory as _

class WeeksField(ExtensionField, atapi.IntegerField):
    """Just a default IntegerField used for holding the number of weeks requested"""

class ReminderField(ExtensionField, atapi.BooleanField):
    """Just a default BooleanField used for toggling whether an email has been sent"""


class OneWeekCreditPublishedSchemaExtender(object):
    """Basic extender to allow us to store our credit publishing metadata on this object"""

    implements(ISchemaExtender)
    adapts(IOneWeekCreditPublishedContent)

    _fields = [
               WeeksField('weeksLeftPublished',
                          schemata='metadata',
                          widget=atapi.DecimalWidget(
                                                     label = _(u"Weeks Left Published"),
                                                     description = _(u"Weeks remaining with this item published"),
                                                     visible = {'edit' : 'invisible',
                                                                'view' : 'invisible',
                                                               },
                                                    ),
                         ),
               ReminderField('republishReminderSent',
                             schemata='metadata',
                             widget=atapi.BooleanWidget(
                                                        label = _(u"Reminder Email Sent"),
                                                        description = _(u"Has a reminder email been sent when this item is about to expire?"),
                                                        visible = {'edit' : 'invisible',
                                                                   'view' : 'invisible',
                                                                  },
                                                       ),
                            ),
              ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self._fields
