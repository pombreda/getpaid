"""
Plugin Manager Base

See: getpaid.core.interfaces.IPluginManager
"""

__version__ = "$Revision$"
# $Id$
# $URL$

from zope import component, interface

from getpaid.core.interfaces import IPluginManager


class PluginManagerBase(object):
    """ A getpaid plugin manager """

    interface.implements(IPluginManager)

    factory = None # <class ... >
    marker = None # <class 'zope.interface.interface.InterfaceClass>

    def __init__(self, context):
        self.context = context
        assert self.marker != None, "Incomplete PluginManager: add plugin (marker) interface."
        assert self.factory != None, "Incomplete PluginManager: add plugin factory class."

    def install(self):
        """ Create and register payment processor as local persistent utility """
        sm = self.context.getSiteManager()
        util = sm.queryUtility(self.marker, name=self.factory.name)
        if util is None:
            payment_processor = self.factory()
            sm.registerUtility(component=payment_processor, provided=self.marker,
                               name=self.factory.name, info=self.factory.description)

    def uninstall(self, remove_data=True):
        """ Delete and unregister payment processor local persistent utility """
        # This base implementation doesn't care about remove_data attribute.
        # Although, there are a few options to implement this:
        # a) if processor could saved its data e.g. on plone.registry, its plugin
        #    manager may implement uninstall() to remove plone.registry data only
        #    on remove_data=True (and otherwise remove persisten utility as usual)
        # b) if processor saved its data on itself, it could implement and support
        #    custom enabled/disabled property and customize install() and uninstall()
        #    to only alter that property when utility already exists on install() or
        #    remove_data=False on uninstall().
        sm = self.context.getSiteManager()
        util = sm.queryUtility(self.marker, name=self.factory.name)
        if util is not None:
            sm.unregisterUtility(util, self.marker, name=self.factory.name)
            del util # Requires successful transaction to be effective

    def status(self):
        """ Return payment processor utility registration status """
        sm = self.context.getSiteManager()
        return sm.queryUtility(self.marker, name=self.factory.name) is not None


## Subscribe your plugin to be installed on IStoreInstalleEvent
#
#  <subscriber
#     for="getpaid.core.interfaces.IStore
#          getpaid.core.interfaces.IStoreInstalledEvent"
#     handler=".myplugin.storeInstalled"
#     />
#
#
# def storeInstalled(object, event):
#     """ Install on IStore Installation (e.g. when PloneGetPaid is installed) """
#     return MyPluginManager(object).install()
