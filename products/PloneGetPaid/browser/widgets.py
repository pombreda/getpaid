from zope.app.form.browser import DropdownWidget
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

print 'cargando mis widgets\n\n\n'
class ChoiceWithSubField(DropdownWidget):

    __cal__ = ViewPageTemplateFile('ChoiceWithSubField.pt')

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

