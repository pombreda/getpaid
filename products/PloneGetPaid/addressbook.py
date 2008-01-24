
from persistent import Persistent
from zope.app.container.sample import SampleContainer

class AddressBookUtility( Persistent ):

    interface.implements( interfaces.IAddressBookUtility )
    
    def __init__( self ):
        self._addresses = OOBTree()

    def get( self, uid, create=True ):
        if not self._addresses.has_key( uid ):
            if not create:
                return
            self._addresses[ uid ] = book = AddressBook()
            book.__name__ = uid
        return self._addresses[ uid ]
        
    def destroy( self, uid ):
        if not self._addresses.has_key( uid ):
            return
        del self._addresses[ uid ]
        
    def manage_fixOwnershipAfterAdd( self ): pass
    
def AddressBook( SampleContainer ):
    
    interface.implements( interfaces.IAddressBook )