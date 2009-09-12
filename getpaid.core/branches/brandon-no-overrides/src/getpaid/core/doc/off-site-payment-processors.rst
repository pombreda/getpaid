
Off-site Payment Processors
===========================

By definition, an off-site payment processor redirects the user's web
browser off-site at some point during the GetPaid checkout process.
There are two reasons why doing so is a bit complicated.

1. There are several points in the checkout process at which payment
   processors might want to redirect users off to their own sites.  For
   example, the Authorize.Net SIM protocol is designed to accept a POST
   from the final payment screen of a checkout process, meaning that it
   would need to take place after GetPaid has already accepted your
   mailing address and offered any pages of shipping options that were
   applicable.  Google Checkout, on the other hand, handles shipping
   options itself, and therefore wants the user redirected the moment
   they finish playing with their shopping cart and hit the “Checkout”
   button.

2. Off-site payment processors need to override the page from which the
   user will be redirected off-site, so that they can craft and insert a
   form which will POST exactly the right information to the payment
   service to get the transaction processed.  Whether they provide an
   entire form or just a simple button, they need the power to render an
   HTML view and return its contents for inclusion on a checkout page.

Of course, there is one task for which every payment processor is
responsible: establishing a web page on the site to which the user can
be redirected when the off-site processing service is done with them.
This not only presents the result of the transaction to the user and
then allows them to navigate back to other parts of the store, but it
also gives GetPaid a chance to mark the transaction as complete and
empty the user's shopping cart so that they can start filling it again.

Fancy off-site payment processing systems often support a callback
mechanism with which they can signal your site when a user finishes
checking out, so that you find out that they did so whether or not their
browser actually makes it back to your site.  GetPaid also lets you
provide a page for this purpose, as we will see below.

So, let's get started!

Your payment processor class
----------------------------

In the :doc:`writing-a-payment-processor` chapter, we started to
construct a sample payment processor class.  Now we will learn how to
finish it.

Your payment processor should specify at which step in the checkout
process it needs to be inserted, and also provide a view that can render
the HTML that needs to be inserted there.

``step_name = 'checkout_button'``
  This indicates ...

``step_name = 'review_pay_form'``
  This says that ...

::

    from getpaid.core.processors import OffSitePaymentProcessor

    from zope.i18nmessageid import MessageFactory
    _ = MessageFactory('getpaid.chargeit')

    class ChargeIt(OffSitePaymentProcessor):
        name = 'charge-it'
        title = _(u'ChargeIt checkout')
        options_schema = IChargeItOptions

        step_name = 'checkout_button'
        view_name = 'getpaid.chargeit.button_view'


Defining your view
------------------

Of course, having named the view that will be rendered to generate your
special check-out button or form, you now need to provide it.  Just as
you normally would in a Zope project, create the named view using ...

..
   def __init__(self, cart, options)


::

    from Products.Five import BrowserView
    class CheckoutButtonView(BrowserView):
        pass  # will automatically use "checkoutbutton.pt"
