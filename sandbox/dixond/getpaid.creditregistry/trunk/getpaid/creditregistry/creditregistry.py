from decimal import Decimal
from persistent import Persistent

from BTrees.OOBTree import OOBTree, OOTreeSet
from BTrees.OIBTree import OIBTree

from zope.interface import implements
from zope.component import getUtility

from interfaces import ICreditRegistryCredit, ICreditRegistry, ICreditRegistryItemDecimalCash

class InvalidCreditType(Exception):
    """Wasn't provided with a credit registry credit"""


class CreditRegistryItemDecimalCash(object):
    """All cash is stored internally in cents, and only converted to dollars+cents for display purposes"""

    implements(ICreditRegistryItemDecimalCash)

    credit = 0
    credit_name = ''
    credit_user = ''

    def __init__(self, credit=0, credit_name='', credit_user=''):
        self.credit = Decimal('%0.2f' % credit)
        self.credit_name = credit_name
        self.credit_user = credit_user

    def __add__(self, other):
        if isinstance(other, CreditRegistryItemDecimalCash):
            self.addCredit(other.queryCredit())
        else:
            self.addCredit(other)
        return self

    def __sub__(self, other):
        if isinstance(other, CreditRegistryItemDecimalCash):
            self.useCredit(other.queryCredit())
        else:
            self.useCredit(other)
        return self

    def currentCredit(self):
        """Print-friendly dollars+cents version"""
        return '$%0.2f' % (self.queryCredit())

    def queryCredit(self):
        return self.credit

    def addCredit(self, credit):
        self.credit += Decimal('%0.2f' % credit)

    def useCredit(self, amount):
        """Use the requested amount and return the value of remaining credit"""
        if amount > self.queryCredit():
            raise InsufficientCreditException("The amount requested to be used is greater than available credit")
        else:
            self.credit = self.credit - amount
        return self.queryCredit()


class CreditRegistry(Persistent):
    """The concrete class implementing the persistent utility for ICreditRegistry.
       The data structure looks like:
       # The default value for the credit when registering a new user:
       # Now initialise a user:
       _usercredit_map = OIBTree()
       _inverted_usermap = OOBTree()
       _inverted_usermap['username'] = OOTreeSet()
       _inverted_usermap['username'].insert('creditname')
       _inverted_creditmap = OOBTree()
       _inverted_creditmap['creditname'] = OOTreeSet()
       _inverted_creditmap['creditname'].insert('username')
    """

    implements(ICreditRegistry)

    #TODO: wire this up a better way that doesn't involve hardcoding at this level
    default_types = {'cash' : CreditRegistryItemDecimalCash}
    _usercredit_map = None
    _inverted_creditmap = None
    _inverted_usermap = None

    def __init__(self):
        self._usercredit_map = OOBTree()
        self._inverted_creditmap = OOBTree()
        self._inverted_usermap = OOBTree()

    #def defineCredit(self, creditinterface, default_value=0):
    #    """Define a new type of credit to track against.
    #    """
    #    if not ICreditRegistryCredit.providedBy(creditinterface):
    #        raise InvalidCreditType("The provided interface does not define a credit registry credit type")
    #    creditname = creditinterface.__identifier__
    #    if not self._inverted_creditmap.has_key(creditname):
    #        self._inverted_creditmap[creditname] = OOTreeSet()
    #    return True

    def initialiseUserCredit(self, username, creditname, initialcredit):
        """Initialises a credit record for username against creditname.
           If the credit is already initialised, just return True.
        """
        if not ICreditRegistryCredit.providedBy(initialcredit):
            raise InvalidCreditType("The provided credit  does not define a credit registry credit type")
        elif (username, creditname) in self._usercredit_map:
            # Policy - set existing credit to initialcredit?
            #        - add existing credit to initialcredit?
            #        - do nothing?
            return True
        else:
            if not self._inverted_creditmap.has_key(creditname):
                # This is the first time this credit has been allocated
                self._inverted_creditmap[creditname] = OOTreeSet()
            self._usercredit_map[(username, creditname)] = initialcredit
            self._inverted_creditmap.setdefault(creditname, OOTreeSet()).insert(username)
            self._inverted_usermap.setdefault(username, OOTreeSet()).insert(creditname)
            return True

    def addCredit(self, username, creditname, amount, credit_type='cash', define=False):
        """Increment the count of a particular credit against a particular user
           raises KeyError if this creditname has not been initialised for this user.
        """
        if define:
            self.initialiseUserCredit(username, creditname, self.default_types[credit_type]())
        self._usercredit_map[(username, creditname)] = self._usercredit_map[(username, creditname)] + amount

    def useCredit(self, username, creditname, amount):
        """Decrement the count of a particular credit against a particular user
           raises KeyError if initiliaseUserCredit() has not ever been called for this username/creditname combo
           raises ValueError if amount is greater than the credit currently available
           returns the amount of credit currently remaining if the transaction is successful
        """
        if self._usercredit_map[(username, creditname)].queryCredit() >= amount:
            self._usercredit_map[(username, creditname)] = self._usercredit_map[(username, creditname)] - amount
            return self._usercredit_map[(username, creditname)]
        else:
            raise ValueError("The amount requested (%d) is greater than the amount available (%d)" % (amount, self._usercredit_map[(username, creditname)]))
        
    def queryCredit(self, username, creditname):
        """Query for the amount of credit currently allocated for creditname to username
           returns integer value (0 if either username or creditname have never been seen
           before). Errors should be transparent to the caller - should *not* raise any exceptions!
        """
        cred = self._usercredit_map.get((username, creditname), None)
        if cred is not None:
            return cred.queryCredit()
        else:
            return 0
