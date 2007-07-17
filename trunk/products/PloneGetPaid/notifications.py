"""
email notifications for store admins and customers.
"""

from zope import component

def sendNotification( order, event ):
    site = component.getSiteManager()
    mail_host = site.context.MailHost
    


