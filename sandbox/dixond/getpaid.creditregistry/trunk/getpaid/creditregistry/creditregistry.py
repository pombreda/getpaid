from persistent import Persistent

from BTrees.OOBTree import OOBTree, OOTreeSet
from BTrees.OIBTree import OIBTree

from zope.interface import implements
from zope.component import getUtility

from interfaces import ICreditRegistry

class CreditRegistry(Persistent):
    """The concrete class implementing the persistent utility for ICreditRegistry.
       The data structure looks like:
       # The default value for the credit when registering a new user:
       _default_values = OIBTree()
       _default_values['creditname'] = int
       # Now initialise a user:
       _usercredit_map = OIBTree()
       _usercredit_map[('username', 'creditname')] = _default_values['creditname']
       _inverted_usermap = OOBTree()
       _inverted_usermap['username'] = OOTreeSet()
       _inverted_usermap['username'].insert('creditname')
       _inverted_creditmap = OOBTree()
       _inverted_creditmap['creditname'] = OOTreeSet()
       _inverted_creditmap['creditname'].insert('username')
    """

    implements(ICreditRegistry)

    _usercredit_map = None
    _inverted_creditmap = None
    _inverted_usermap = None
    _default_values = None

    def __init__(self):
        self._usercredit_map = OIBTree()
        self._inverted_creditmap = OOBTree()
        self._inverted_usermap = OOBTree()
        self._default_values = OIBTree()

    def defineCredit(self, creditname, default_value=0):
        """Define a new type of credit to track against.
           Raises ValueError if default_value is not int-ish
        """
        if not self._inverted_creditmap.has_key(creditname):
            try:
                self._default_values[creditname] = int(default_value)
            except ValueError, e:
                raise ValueError("%s is an invalid value for default_value" % str(default_value))
            else:
                self._inverted_creditmap[creditname] = OOTreeSet()
        return True

    def initialiseUserCredit(self, username, creditname):
        """Initialises a credit record for username against creditname.
           If the credit is already initialised, just return True.
           Raises KeyError if defineCredit() has not ever been called for this creditname.
        """
        self._usercredit_map.setdefault((username, creditname), self._default_values[creditname])
        self._inverted_creditmap[creditname].insert(username)
        self._inverted_usermap.setdefault(username, OOTreeSet()).insert(creditname)
        return True

    def addCredit(self, username, creditname, amount, define=False):
        """Increment the count of a particular credit against a particular user
           raises KeyError if creditname has not already been defined and define is False
        """
        # Harmless if already initialised, raises KeyError if creditname is not known
        if define:
            self.defineCredit(creditname)
        self.initialiseUserCredit(username, creditname)
        self._usercredit_map[(username, creditname)] = self._usercredit_map[(username, creditname)] + amount

    def useCredit(self, username, creditname, amount):
        """Decrement the count of a particular credit against a particular user
           raises KeyError if initiliaseUserCredit() has not ever been called for this username/creditname combo
           raises ValueError if amount is greater than the credit currently available
           returns the amount of credit currently remaining if the transaction is successful
        """
        if self._usercredit_map[(username, creditname)] >= amount:
            self._usercredit_map[(username, creditname)] = self._usercredit_map[(username, creditname)] - amount
            return self._usercredit_map[(username, creditname)]
        else:
            raise ValueError("The amount requested (%d) is greater than the amount available (%d)" % (amount, self._usercredit_map[(username, creditname)]))
        
    def queryCredit(self, username, creditname):
        """Query for the amount of credit currently allocated for creditname to username
           returns integer value (0 if either username or creditname have never been seen
           before). Errors should be transparent to the caller - should *not* raise any exceptions!
        """
        return self._usercredit_map.get((username, creditname), 0)
