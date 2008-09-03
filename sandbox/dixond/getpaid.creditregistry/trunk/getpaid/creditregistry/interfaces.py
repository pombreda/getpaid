from getpaid.creditregistry import creditregistryMessageFactory as _
from zope.interface import Interface

from zope import schema

class ICreditRegistryItem(Interface):
    """An interface for any item that is purchased to gain 'credits'
    """

    credit_name = schema.ASCIILine(title = _(u"Credit Name"),
                                   description = _(u"The name of the type of credit being represented"),
                                   required = True)

    user_name = schema.ASCIILine(title = _(u"User Name"),
                                 description = _(u"The name of the user that this credit should be applied to"),
                                 required = True)

    credit_amount = schema.Int(title = _(u"Credit Amount"),
                               description = _(u"The amount to increment this credit by"),
                               required = True)



class ICreditRegistry(Interface):
    """A registry for storing and revoking integer 'credits' and associating them with a given user.
    """

    def defineCredit(creditname, default_value=0):
        """Define a new type of credit to track against.
           Raises KeyError if creditname already exists, and ValueError if default_value is not int-ish
        """

    def initialiseUserCredit(username, creditname):
        """Initialises a credit record for username against creditname.
           If the credit is already initialised, just return True.
           Raises KeyError if defineCredit() has not ever been called for this creditname.
        """

    def addCredit(username, creditname, amount):
        """Increment the count of a particular credit against a particular user
           raises KeyError if creditname has not already been defined
        """

    def useCredit(username, creditname, amount):
        """Decrement the count of a particular credit against a particular user
           raises KeyError if initiliaseUserCredit() has not ever been called for this username/creditname combo
           raises ValueError if amount is greater than the credit currently available
           returns the amount of credit currently remaining if the transaction is successful
        """

    def queryCredit(username, creditname):
        """Query for the amount of credit currently allocated for creditname to username
           returns integer value (0 if either username or creditname have never been seen
           before). Errors should be transparent to the caller - should *not* raise any exceptions!
        """
