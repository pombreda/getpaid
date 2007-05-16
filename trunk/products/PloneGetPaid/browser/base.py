"""
$Id$
"""

from zope.i18n.interfaces import IUserPreferredLanguages
from zope.i18n.locales import locales
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.Five.formlib import formbase

class BaseView( object ):
    
    def setupEnvironment( self, request ):
        if not hasattr( request, 'debug'): request.debug = False
        
    def setupLocale( self, request ):
        # slightly adapted from zope.publisher.http.HTTPRequest.setupLocale
        if getattr( request, 'locale', None) is not None:
            return
        
        envadapter = IUserPreferredLanguages(request, None)
        if envadapter is None:
            request.locale = locales.getLocale(None, None, None)            
            return

        langs = envadapter.getPreferredLanguages()
        for httplang in langs:
            parts = (httplang.split('-') + [None, None])[:3]
            try:
                request.locale = locales.getLocale(*parts)
                return
            except LoadLocaleError:
                # Just try the next combination
                pass
        else:
            # No combination gave us an existing locale, so use the default,
            # which is guaranteed to exist
            request.locale = locales.getLocale(None, None, None)


class BaseFormView( formbase.EditForm, BaseView ):

    template = ZopeTwoPageTemplateFile('templates/form.pt')

    action_url = "" # NEEDED
    hidden_form_vars = None # mapping of hidden variables to pass through on the form

    def hidden_inputs( self ):
        if not self.hidden_form_vars: return ''
        return make_hidden_input( **self.hidden_form_vars )

    hidden_inputs = property( hidden_inputs )
    
    def __init__( self, context, request ):
        # setup some compatiblity
        self.setupLocale( request )
        self.setupEnvironment( request )
        super( BaseFormView, self).__init__( context, request )
        
