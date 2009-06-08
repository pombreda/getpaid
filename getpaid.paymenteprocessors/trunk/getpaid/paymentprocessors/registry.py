"""

    Payment processor registry.

"""

__author__ = "Mikko Ohtamaa <mikko.ohtamaa@twinapex.fi>"
__docformat__ = "epytext"


class ProcessorEntry:
    """ Payment processor configuration data holder.
    
    For possible parameters, see directives.IRegisterPaymentProcessorDirective
    """
    
    # Global dictionary holding processor name -> processor instance mappings
    registry = {}
    
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    
    @classmethod
    def register(cls, processor):
        """ Put a new payment processor to the global registry """
        cls.registry[processor.name] = processor
                
    
        
        

    