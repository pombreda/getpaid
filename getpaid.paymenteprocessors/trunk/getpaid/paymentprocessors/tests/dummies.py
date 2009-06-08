import zope.interface

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

import getpaid.core 

class DummyButton:
    
    index = ViewPageTemplateFile("templates/button.pt")
    
    def render(self):
        return self.index()

class DummyThankYou:
    
    index = ViewPageTemplateFile("templates/thank_you.pt")
    
    def render(self):
        return self.index()
    
    
class DummyProcessor:
    zope.interface.implements(getpaid.core.interfaces.IPaymentProcessor)
    
    