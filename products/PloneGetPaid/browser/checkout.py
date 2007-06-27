"""

cart-review checkout

$Id$
"""

"""
random notes

get order

 - create order [ entry points ]
 - dispatch on workflow state
 
Order Workflow

  - created
     - system invariant - make sure we don't create multiple orders from the same cart, need to create cart_id, retrieve order by user_id, cart_id
     - automatic ready
     
  - ready
     - user submit
     
  - pending
     - automatic declined     
     - automatic accepted
     
  - declined
     - user submit pending

  - accepted
     - admin submit processed
     
  - processed

  - re
  
  - status
  
allow linear progression

carry hidden to force transition to required, allow linear links to be used though

"""

from zope.formlib import form
from zope import component
from getpaid.core import interfaces
from getpaid.core.order import Order

from base import BaseFormView
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from zope.schema import getFieldsInOrder
import random, sys
from cPickle import loads, dumps
from ore.member.browser import MemberContextEdit

class PropertyBag(object):

    schema = interfaces.IUserPaymentInformation
    title = "Payment Details"
    description = ""
    
    def initclass( cls ):
        for field_name, field in getFieldsInOrder( interfaces.IUserPaymentInformation ):
            setattr( cls, field_name, field.default )
    
    initclass = classmethod( initclass )

PropertyBag.initclass()

class ImmutableBag( object ):

    def initfrom( self, other, iface ):
        for field_name, field in getFieldsInOrder( iface ):
            setattr( self, field_name, field.get( other ) )
        return self
            

    
class CheckoutBillingCollection( MemberContextEdit ):

    form_fields = None
    template = ZopeTwoPageTemplateFile("templates/checkout-billing-info.pt")

    @form.action("Make Payment")
    def makePayment( self, action, data ):
        order_manager = component.getUtility( interfaces.IOrderManager )
        order = Order()

        shopping_cart = component.getUtility( interfaces.IShoppingCartUtility ).get( self.context )
        # shopping cart is attached to the session, but we want to switch the storage to the persistent
        # zodb, we pickle to get a clean copy to store.
        order.shopping_cart = loads( dumps( shopping_cart ) )
        order.shipping_address = ImmutableBag().initfrom( self.adapters[ interfaces.IShippingAddress ],
                                                          interfaces.IShippingAddress ) 
        order.billing_address = ImmutableBag().initfrom( self.adapters[ interfaces.IBillingAddress ],
                                                         interfaces.IBillingAddress )
        while 1:
            order_id =  str( random.randint( 0, sys.maxint ) )
            if order_manager.get( order_id ) is None:
                break
        order.order_id = order_id
        order_manager.store( order )

    def getFormFields( self, user ):
        form_fields = super( CheckoutBillingCollection, self).getFormFields(user)
        self.adapters[ interfaces.IUserPaymentInformation ] = self.billing_info
        return form_fields + form.Fields( interfaces.IUserPaymentInformation )

    def __call__( self ):
        self.billing_info = PropertyBag()        
        return super( CheckoutBillingCollection, self).__call__()

    def setUpWidgets( self, ignore_request=False ):
        self.adapters = self.adapters is not None and self.adapters or {}
        self.widgets = form.setUpEditWidgets(
            self.form_fields, self.prefix, self.context, self.request,
            adapters=self.adapters, ignore_request=ignore_request
            )
    


    
