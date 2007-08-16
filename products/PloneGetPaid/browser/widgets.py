from zope.app.form.browser import FloatWidget
from zope.app.form.browser.widget import SimpleInputWidget
from zope.app.form.browser.itemswidgets import OrderedMultiSelectWidget as BaseSelection
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile


#from Acquisition import Explicit

class ChoiceWithSubField(SimpleInputWidget):

    template = ViewPageTemplateFile('templates/ChoiceWithSubField.pt')
    
    def test( self ):
        """Test"""
        return "test"
    
    def __call__( self ):
        #return self.render()
        return self.template()

    def getVocabulary(self):
        return self.context.vocabulary

    #def render(self):
        #result = """<div xmls:tal="http://xml.zpope.org/namespaces/tal">
#<select>"""
        #for i in self.getVocabulary():
            #result += '<option value="%s">%s</option>' % (i.title,i.title)
        #result += '</select> </div>'
        #return result

    #def __init__(self,**kw):
        #print 'asi como vine, me voy'
        #super(ChoiceWithSubField,self).__init__(**kw)

    #def renderValue(self, value):
        #rendered_items = self.renderItems(value)
        #contents = "\n%s\n" %"\n".join(rendered_items)
        #print '*'*80
        #print 'yes'
        #print '*'*80
        #return renderElement('select',
                             #name=self.name+'jota',
                             #id=self.name,
                             #contents=contents,
                             #size=self.size,
                             #extra=self.extra,
                             #onchange="javascript:alert('alarma!');")

    #def __call__(self):
        #"""See IBrowserWidget."""
        #print '*'*80
        #print 'mi __call__'
        #print '*'*80
        #value = self._getFormValue()
        #contents = []
        #have_results = False

        #contents.append(self._div('value', self.renderValue(value)))
        #contents.append(self._emptyMarker())
        #return self._div(self.cssClass, "\n".join(contents))


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
