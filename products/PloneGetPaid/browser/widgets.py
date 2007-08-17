from zope.app.form.browser import FloatWidget
from zope.app.form.browser.widget import SimpleInputWidget
from zope.app.form.browser.itemswidgets import OrderedMultiSelectWidget as BaseSelection
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from zope.i18n.interfaces import IUserPreferredCharsets

from Products.Five.browser.decode import setPageEncoding

class CountrySelectionWidget(SimpleInputWidget):

    template = ViewPageTemplateFile('templates/country-selection-widget.pt')

    def __call__( self ):
        # XXX dirty hack to make the values coming out of here encoded properly
        # please fix me.
        envadapter = IUserPreferredCharsets( self.request)
        charsets = envadapter.getPreferredCharsets() or ['utf-8']
        value = unicode( self.template(), charsets[0] )
        # we reset the page encoding thg thats get set by our template
        setPageEncoding( self.request )
        return value

    def getVocabulary(self):
        return self.context.vocabulary

class StateSelectionWidget(SimpleInputWidget):

    def __call__( self ):
        value = ''
        if self.hasInput():
            value = self.getInputValue()
        return """<div id="%s_container">
                  <select name="%s" id="%s">
                    <option value="%s" selected="selected">Selected</option>
                  </select>
                  </div>""" % (self.name, self.name, self.name, value)


class PriceWidget(FloatWidget):
    """ This is a widget for rendering the price.
    """
    def _toFormValue(self, value):
        """Converts a field value to a string used as an HTML form value.

        This method is used in the default rendering of widgets that can
        represent their values in a single HTML form value. Widgets whose
        fields have more complex data structures should disregard this
        method and override the default rendering method (__call__).
        """
        if value == self.context.missing_value:
            return self._missing
        else:
            #import pdb; pdb.set_trace()
            return '%.2f' % value



def SelectWidgetFactory( field, request ):
    vocabulary = field.value_type.vocabulary
    return OrderedMultiSelectionWidget( field, vocabulary, request ) 

class OrderedMultiSelectionWidget(BaseSelection):
    template = ViewPageTemplateFile('templates/ordered-selection.pt')

    def __call__( self ):

	value = super( OrderedMultiSelectionWidget, self).__call__()
        setPageEncoding( self.request )
	return value

    def selected(self):
        """Return a list of tuples (text, value) that are selected."""
        # Get form values
        values = self._getFormValue()
        # Not all content objects must necessarily support the attributes
        if hasattr(self.context.context, self.context.__name__):
            # merge in values from content 
            for value in self.context.get(self.context.context):
                if value not in values:
                    values.append(value)
        terms = [self.vocabulary.getTerm(value)
                 for value in values if value in self.vocabulary ]
        return [{'text': self.textForValue(term), 'value': term.token}
                for term in terms]
