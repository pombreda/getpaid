"""
email notifications for store admins and customers.
"""

from zope import component
from getpaid.core.interfaces import workflow_states

import interfaces

from DocumentTemplate.DT_HTML import HTML

customer_new_order_template = HTML('''\
To: <dtml-var to_email>
From: "<dtml-var store_name>" <dtml-var from_email>
Subject: New Order Notification

Thank you for you order.

Total Amount to be Charged : <dtml-var "order.getTotalPrice()">

You can view the status of your order here

<dtml-var store_url>/@@getpaid-order-history

''')

merchant_new_order_template = HTML('''\
To: <dtml-var to_email>
From: "<dtml-var store_name>" <dtml-var from_email>
Subject: New Order Notification

A New Order has been created

Total Cost: <dtml-var "order.getTotalPrice()">

The url to continue processing the order is here
<dtml-var store_url>/@@admin-manage-order/<dtml-var "order.order_id">

''')
                                   

def sendNotification( order, event ):
    """ sends out email notifications to merchants and clients based on settings.

    for now we only send out notifications when an order initially becomes chargeable
    """
    
    site = component.getSiteManager()
    portal = site.context
    mailer = portal.MailHost
    
    if event.destination != workflow_states.order.finance.CHARGING:
        return
    
    if not event.source in ( workflow_states.order.finance.REVIEWING,
                             workflow_states.order.finance.PAYMENT_DECLINED ):
        return 
    
    settings = interfaces.IGetPaidManagementOptions( portal )

    store_url = portal.absolute_url()
    
    if settings.merchant_email_notification == 'notification' \
       and settings.contact_email:

        message = merchant_new_order_template( to_email = settings.contact_email,
                                               from_email = settings.contact_email,
                                               store_url = store_url,
                                               order = order)
        mailer.send( message )

    if settings.customer_email_notification == 'notification' \
       and order.user_id:
        
        member = site.portal_membership.getMemberById( order.user_id )
        message = customer_new_order_template( to_email = member.getProperty('email'),
                                               from_email = settings.contact_email,
                                               store_url = store_url,
                                               order = order )
        mailer.send( message )

    
    


