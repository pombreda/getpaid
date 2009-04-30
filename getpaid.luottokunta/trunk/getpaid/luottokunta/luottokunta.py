from zope.interface import implements
from zope.component import adapts
from Products.CMFCore.interfaces import ISiteRoot
from interfaces import ILuottokuntaProcessor, ILuottokuntaOptions


class LuottokuntaProcessor( object ):

    implements(ILuottokuntaProcessor)
    adapts(ISiteRoot)

    options_interface = ILuottokuntaOptions

    def __init__( self, context ):
        self.context = context
