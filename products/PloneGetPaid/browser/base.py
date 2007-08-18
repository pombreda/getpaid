"""
$Id$
"""


from zope.i18n.interfaces import IUserPreferredLanguages, IUserPreferredCharsets
from zope.i18n.locales import locales, LoadLocaleError

from ZTUtils import make_hidden_input

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.app import pagetemplate
from Products.Five.browser import decode
from Products.Five.formlib import formbase
from Products.Five.viewlet import viewlet

from yoma.layout import layout

class LayoutTemplate( object ): pass

class WidgetRenderer( layout.WidgetRenderer ):
    
    template = pagetemplate.ViewPageTemplateFile('templates/grid-widget-render.pt')
    
    def render( self ):
        self.visible = self.widget.visible
        self.error = self.widget.error()
        self.required = self.widget.required
        
        print 'visible', self.widget.visible, 'required', self.widget.required, 'error', self.widget.error()
        value =  self.template( widget=self.widget)
        charsets = IUserPreferredCharsets( self.request ).getPreferredCharsets() or ['utf-8']
        # reset since our z3 template kills it.
        decode.setPageEncoding( self.request )
        return decode._decode( value, charsets )

## class TextCell( layout.TextCell ):

##     def render( self, form ):
##         value = self()
##         if isinstance( value, messageid ):
##             return XXX translate
##         return value

class WidgetCell( layout.WidgetCell ):

    def render( self, form ):
        name, label, hint = self()
        renderer = WidgetRenderer( form.context, form.request, form.widgets[ name ] )

        return unicode( renderer.render() )

class GridLayout( layout.GridLayout ):

    def addWidget(self,
        name, row, col, rowspan=1, colspan=1, label=layout._marker, hint=layout._marker,
        ):
        widgetcell = WidgetCell(name, label, hint, rowspan, colspan)
        if label is None:
            # hide label - swallow up the label column
            widgetcell.width += 1
            self.grid.set(row, col, widgetcell)
        else:
            self.grid.set(row, col, layout.LabelCell(widgetcell))
            self.grid.set(row, col+1, widgetcell)
        return self

    def setDesign( self, row, col, **kw ):
        for n in ('id', 'class', 'style'):
            if not n in kw:
                continue
            setattr( self.grid.get( row, col ), n, kw[n] )
            
    def setId( self, row, col, id ):
        setattr( self.grid.get( row, col), 'id', id )

    def setCSS( self, row, col, css_class ):
        setattr( self.grid.get( row, col), 'class', css_class )

    def setStyle( self, row, col, style ):
        setattr( self.grid.get( row, col), 'style', style )
        
    def render( self, form ):
        formatter = LayoutTableFormatter( self.grid, form )
        return formatter()

class LayoutTableFormatter( layout.TableFormatter ):
    
    def renderCell( self, cell ):
        attr = u''
        for n in ('style', 'class', 'id'):
            value = getattr( cell, n, '' )
            if value:
                attr += u' %s="%s"'%(n, value )
        if cell.width > 1:
            attr += (u' colspan="%s"' % cell.width)
        if cell.height > 1:
            attr += (u' rowspan="%s"' % cell.height)
        print>>self.out, u'<td%s>%s</td>' % (attr, cell.render(self.form))        
        

class FormViewlet( viewlet.SimpleAttributeViewlet, formbase.SubPageForm ):
    """ a viewlet which utilize formlib
    """
    form_template = formbase.FormBase.template    
    renderForm = formbase.FormBase.render
    
    __page_attribute__ = "template"
    
    def update( self ):
        super( viewlet.SimpleAttributeViewlet, self).update()
        super( formbase.SubPageForm, self).update()

class BaseView( object ):
    # so this mixin fixes some issues with doing zope3 in zope2 for views
    # specifically it puts a debug attribute on the request which some view machinery checks for
    # secondly it lookups the user locale, and attaches it as an attribute on the request
    # where the i10n widget machinery expects to find it.

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

    template = ViewPageTemplateFile('templates/form.pt')

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
        
