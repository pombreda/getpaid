"""

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

from Products.Five.browser import BrowserView

class CheckoutWizard( BrowserView ):
    """
    review cart
    
    collect address billing info
    create order
    
    payment processor ( order, customer ) viewlet
    
    payment processor
      sets order status

    callback url for followup after processor ( return to url )
    
    """
    pass


