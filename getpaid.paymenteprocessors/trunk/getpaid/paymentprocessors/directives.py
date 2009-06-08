""" Payment processor configuration ZCML directives

"""

__author__ = "Mikko Ohtamaa <mikko.ohtamaa@twinapex.fi>"
__docformat__ = "epytext"

import os
from inspect import ismethod

from zope import component
from zope.interface import Interface
from zope.component.zcml import handler
from zope.component.interface import provideInterface
from zope.configuration.exceptions import ConfigurationError
from zope.publisher.interfaces.browser import IBrowserRequest, \
     IDefaultBrowserLayer

from zope.app.publisher.browser.viewmeta import pages as zope_app_pages
from zope.app.publisher.browser.viewmeta import view as zope_app_view
from zope.app.publisher.browser.viewmeta import providesCallable, \
     _handle_menu, _handle_for

from Globals import InitializeClass as initializeClass

from zope.configuration.fields import GlobalObject, GlobalInterface
from zope.configuration.fields import MessageID
from zope.configuration.fields import Path
from zope.configuration.fields import PythonIdentifier
from zope.interface import Interface

import getpaid.core

import registry

class IRegisterPaymentProcessorDirective(Interface):
    """ Register payment processor with the global registry.
    """

    name = PythonIdentifier(
        title=u'Name',
        description=u"Unique identifier for the payment processor (use package name)",
        required=True)
    
    processor = GlobalObject(
        title=u"Payment processor",
        description=u"Class which implements IPaymentProcessor",
        required=True)
        
    selection_view = GlobalObject(
        title=u'Selection view',
        description=u"BrowserView class full name which is used to render the payment processor checkout button",        
        required=True)
    
    thank_you_view = GlobalObject(
        title=u'Thank you view',
        description=u"BrowserView class full name which is used to render the thank you page when the payment is complete",        
        required=True)

    setup_view = GlobalObject(
        title=u'Setup view',
        description=u"BrowserView class full name which is used to render the payment processor configuration screen",
        default=None,
        required=False)

def registerProcessor(_context, name, processor, selection_view, thank_you_view, setup_view=None):
    """
    Configure a payment processor.    
    """
    entry = registry.ProcessorEntry(name=name, selection_view=selection_view, thank_you_view=thank_you_view, setup_view=setup_view)    
    
    if not getpaid.core.interfaces.IPaymentProcessor.implementedBy(processor):
        raise ConfigurationError("Payment processor directive does not implement IPaymentProcessor interface:" + str(processor))
    
    registry.ProcessorEntry.register(entry)

