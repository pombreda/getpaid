# Copyright (c) 2007 ifPeople, Kapil Thangavelu, and Contributors
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

"""

workflow event driven payment processor integration and property bags needed for
an order.
"""

from getpaid.core import interfaces, options 
from zope import component, interface

class Address( options.PersistentBag ): pass
Address.initclass( interfaces.IAddress  )    
    
class ShippingAddress( options.PersistentBag ): pass
ShippingAddress.initclass( interfaces.IShippingAddress )    
 
class BillingAddress( options.PersistentBag ): pass
BillingAddress.initclass( interfaces.IBillingAddress )    
    
class ContactInformation( options.PersistentBag ): pass
ContactInformation.initclass( interfaces.IUserContactInformation )    
    
def fireAutomaticTransitions( order, event ):    
    """ fire automatic transitions for a new state """ 
    order.finance_workflow.fireAutomatic()


def processorWorkflowSubscriber( order, event ):
    """
    fire off transition from charging to charged or declined based on
    payment processor interaction.
    """

    # check for a payment processor associated with the 
    # there is a default notion here that the workflows for finance / fulfillment can't share state names
    # 
    if order.finance_state == event.destination:
        adapter = component.queryMultiAdapter( (order, order.finance_workflow.workflow() ),
                                               interfaces.IWorkflowPaymentProcessorIntegration )
                                               
    elif order.fulfillment_state == event.destination:
        adapter = component.queryMultiAdapter( (order, order.fulfillment_workflow.workflow() ),
                                               interfaces.IWorkflowPaymentProcessorIntegration )
    else:
        return
                                              
    if adapter is None:
        return

    return adapter( event )

class DefaultFinanceProcessorIntegration( object ):
    
    interface.implements( interfaces.IWorkflowPaymentProcessorIntegration )
    
    def __init__( self, order, workflow):
        self.order = order
        self.workflow = workflow
        
    def __call__( self, event ):
        if event.destination != interfaces.workflow_states.order.finance.CHARGING:
            return

        # ick.. get a hold of the store
        # this is a little gross, we need some access to context, so we fetch line items
        # till we find something that resolves to an object, and try to get the store from that
        # 
        context = component.queryUtility( interfaces.IStore )
        if context is None:
            from Products.CMFCore.utils import getToolByName
            ob = None
            for i in self.order.shopping_cart.values():
                if interfaces.IPayableLineItem.providedBy( i ):
                    ob = i.resolve()
            if ob is None:
                raise AttributeError("can't get store, TODO - please switch processors settings to utility adapters")
            context = getToolByName( ob, 'portal_url').getPortalObject()

        processor = component.getAdapter( context,
                                          interfaces.IPaymentProcessor,
                                          self.order.processor_id )

        result = processor.capture( self.order, self.order.getTotalPrice() )
    
        if result == interfaces.keys.results_async:
            return
        elif result == interfaces.keys.results_success:
            self.order.finance_workflow.fireTransition('charge-charging')
        else:
            self.order.finance_workflow.fireTransition('decline-charging', comment=result)


CREDIT_CARD_TYPES = ( u"Visa", u"MasterCard", u"Discover", u"American Express" )

class CreditCardTypeEnumerator(object):
    interface.implements(interfaces.ICreditCardTypeEnumerator)

    def __init__(self, context):
        self.context = context

    def acceptedCreditCardTypes(self):
        return CREDIT_CARD_TYPES

    def allCreditCardTypes(self):
        return CREDIT_CARD_TYPES
