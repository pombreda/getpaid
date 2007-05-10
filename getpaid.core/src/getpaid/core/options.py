from zope.app.annotation import IAnnotations
from persistent.dict import PersistentDict
from zope import schema
from zope.interface import classImplements, implements
import interfaces


class PersistentOptions( object ):

    implements( interfaces.IPersistentOptions )
    
    _storage = None
    
    def __init__( self, context ):
        self.context = context

    def storage( self, name=None ):
        """ name if given is the key of a persistent dictionary off of
        the annotation.
        """ 
        if self._storage is None:
            annotations = IAnnotations( self.context )
            self._storage = annotations.get( self.annotation_key, None )
            if self._storage is None:
                annotations[ self.annotation_key ] = self._storage = PersistentDict()

        if name is None:
            return self._storage
        if name in self._storage:
            return self._storage[name]
        
        self._storage[ name ] = PersistentDict()
        return self._storage[name]

    def getProperty( self, property_name ):
        return self.storage().get( property_name )
    
    def setProperty( self, property_name, property_value ):
        self.storage()[ property_name ] = property_value

    def nullProperty( self, *args):
        return None

    def wire( cls, name, key, *interfaces, **options ):
        fields = {}
        bases = (cls, ) + options.get('bases', ())
        
        for iface in interfaces:
            for field in schema.getFields( iface ).values():
                fields[ field.__name__ ] = property( lambda self, field_name=field.__name__: self.getProperty( field_name ),
                lambda self, value, field_name=field.__name__: self.setProperty( field_name, value ) )
        new_class = type( name, bases, fields)
        cls.annotation_key = key
        classImplements( new_class, interfaces )
        return new_class

    wire = classmethod( wire )
    
