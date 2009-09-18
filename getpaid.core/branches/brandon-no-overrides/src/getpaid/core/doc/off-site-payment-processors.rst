
Off-site Payment Processors
===========================

By definition, an off-site payment processor redirects the user's web
browser off-site at some point during the GetPaid checkout process.
Writing support for an off-site solution can be a bit complicated,
because you have think through every GET and POST that will be involved
along the way as the user is sent off-site and then returns.  But if you
simply tackle the issues one at a time, you should find the process of
writing your payment processor quite manageable.

There are several steps involved in writing an off-site payment
processor, so here they are, in a simple list.  Use this list as an
overview to help orient you as you read through this document, and also
as a checklist to make sure you have covered everything when you think
your payment processor package is nearing completion.

1. Provide a view that, through means of an HTML form, will direct the
   user off-site.  This view will either be an alternative to the normal
   GetPaid “Checkout” button, and thus skip the entire GetPaid checkout
   experience, or it will be a form that sits on the last of the GetPaid
   checkout screens in place of GetPaid's normal credit-card form.
   Either way, your view will determine exactly how the user's browser
   is directed away from GetPaid at the crucial moment.

2. Provide a “Welcome back” experience for users returning when they
   have completed their order using the off-site processor.  This might
   be a single page that says either “Welcome back” or “Sorry you were
   declined” depending upon information encoded in the URL or form when
   the user returns from off-site, or it might be two pages with
   different URLs.

3. Make sure that a GetPaid :class:`Order` object gets created and
   marked as successfully "authorized" if the user completes the
   off-site process and their credit card is authorized for payment.

4. If the off-site payment processor supports it, you should provide
   methods with which the GetPaid store owner can either capture the
   authorized funds once they are ready to send the buyer goods, or can
   refund the customer instead.

If any of these steps sound complicated, then, well, there's the chance
that they are — depending, largely, on how complicated the payment
processing site is that you are trying to tie GetPaid into.  But we have
tried to make your GetPaid development experience as happy as possible,
as you will see in the following sections, where we will tackle each of
the above goals and show you how to implement their solutions.

.. neither shopping card nor order will be available, will they?
   can we give off-site service a different URL for each order?

Your payment processor class
----------------------------

As discussed in the :doc:`writing-a-payment-processor` introduction, the
core of your payment processor code will be a class that inherits from
the base class for off-site payment processors.  The only strict
requirement beyond the basics we have already covered is that it must
tell GetPaid which views to render to replace either the shopping cart
check-out button or the review-and-pay credit-card form.  The result, at
its simplest, looks something like this::

    from getpaid.core.processors import OffSitePaymentProcessor
    from getpaid.chargeit.interfaces import IChargeItOptions

    from zope.i18nmessageid import MessageFactory
    _ = MessageFactory('getpaid.chargeit')

    class ChargeIt(OffSitePaymentProcessor):
        name = 'charge-it'
        title = _(u'ChargeIt checkout')
        options_schema = IChargeItOptions

        checkout_button = None
        review_pay_form = 'getpaid.chargeit.review_pay'

Here, the views names (in the next section we will start discussing the
actual creation of the views themselves) have been specified using
simple class attributes, and in many cases this is all you will need.

The ``checkout_button`` attribute, if not ``None``, should name the view
that will replace the GetPaid checkout button at the bottom of each
shopping cart view (both the cart portlet, and the main cart page).
Similarly, the ``review_pay_form`` attribute names the view that should
be rendered to supply the bottom pane of the last page of GetPaid's
checkout process.  Typically, you will only supply a name for one of
these attributes, and leave the other ``None``.

Of course, just because this bare minimum is sufficient does not mean
that your particular processor class needs to be this simple.  You will,
in particular, find that the class is an excellent place to put logic
that you want shared conveniently among your views.  But before we
explore this idea, we should look at exactly how your payment processor
class is used in GetPaid.

How your processor class is used
--------------------------------

You should be aware of the fact that GetPaid always asks questions of a
fully-fledged *instance* of your class, and never of the bare class
itself.  In other words, if faced with the class shown in the previous
section, GetPaid would determine the name of the checkout view by doing
something roughly equivalent to this::

    payment_processor = ChargeIt(options, shopping_cart, order)
    checkout_view = payment_processor.checkout_button

The three arguments used to instantiate your class are simply stored in
attributes of the same name by the initialize method that you inherit
from ``OffSitePaymentProcessor``, so you can access them easily.  The
three values are:

``options``
  An object that implements the ``options_schema`` that your class
  names, whose attributes are the values that the store owner has set
  through the GetPaid admin interface.

``shopping_cart`` ``order``
  (These two objects will be documented elsewhere, and links to those
  sections of the documentation added here in a while.)

Because GetPaid asks for the ``checkout_button`` and ``review_pay_form``
attributes of an instance of your class, and not simply of the class
object itself, you have the option of generating the answer dynamically
through code like this::

    class ChargeIt(OffSitePaymentProcessor):
        ...
        @property
        def review_pay_form(self):
            if self.options.inEuropeanUnion:
                return 'getpaid.chargeit.euro-review-pay'
            else:
                return 'getpaid.chargeit.world-review-pay'

The likelihood of needing this flexibility is small.  After all, you
could just supply one view whose outer level was a big “if” statement as
easily as you could provide two separate views like this with a switch
to decide between them.  But the ability is there if you ever need it.

Writing views
-------------


store will live at some URL
store_views?
no, normal views registered to IStore




what is your URL?
store = zope.component.getUtility(IStore)
store_url = store.absolute_url()

Setting up your checkout view
-----------------------------

As its first step toward supporting an off-site payment processor, your
package must arrange to interrupt the normal GetPaid checkout wizard and
send the user off-site to finish checking out instead.

There are two places where GetPaid is currently configured to be
interrupted; your payment processor can use either.

1. If your off-site processor wants to be in charge of the entire
   check-out process, then you will want to override the checkout button
   itself that normally carries the user from the GetPaid shopping cart
   to the first page of the checkout wizard.

2. If the off-site processor is more modest, and wants GetPaid to do the
   work of collecting the user's address and shipping data so that only
   the actual credit-card verification step is left, then you will just
   want to take control of the bottom half of the “review-and-pay”
   screen.  Instead of letting GetPaid put its normal credit-card form
   there, you will want to either display a form of your own that POSTs
   directly to the off-site processor, or a button that sends the user,
   along with all of the shipping and address information that has
   already been collected, to the off-site processor's web site.

In order to discover

1 needs to name view
2 needs to get its URL in other views
3 the view needs to get called when its URL is called

/Plone
/Plone/store
/Plone/checkout/callback
/Plone/

``checkout_button = 'view_name'``
  This indicates ...

``review_pay_form = 'view_name'``
  This says that ...


First, it is complicated because there are several points in the
checkout process at which payment processors might want to redirect
users off to their own sites.  For example, the Authorize.Net SIM
protocol is designed to accept a POST from the final payment screen of a
checkout process, meaning that it would need to take place after GetPaid
has already accepted your mailing address and offered any pages of
shipping options that were applicable.  Google Checkout, on the other
hand, handles shipping options itself, and therefore wants the user
redirected the moment they finish playing with their shopping cart and
hit the “Checkout” button.

Off-site payment processors need to override the page from which the
user will be redirected off-site, so that they can craft and insert a
form which will POST exactly the right information to the payment
service to get the transaction processed.  Whether they provide an
entire form or just a simple button, they need the power to render an
HTML view and return its contents for inclusion on a checkout page.

There are two other tasks for which every off-site payment processor is
responsible.


Welcoming the user back
-----------------------

drat, when does order get created?

 — as best they can;
off-site processors will

  : establishing a URL on the site to which the
user can be redirected when the off-site processing service is done with
them.  This not only presents the result of the transaction to the user
and then allows them to navigate back to other parts of the store, but
it also gives GetPaid a chance to mark the transaction as complete and
empty the user's shopping cart so that they can start filling it again.

Fancy off-site payment processing systems often support a callback
mechanism with which they can signal your site when a user finishes
checking out, so that you find out that they did so whether or not their
browser actually makes it back to your site.  GetPaid also lets you
provide a page for this purpose, as we will see below.

So, let's get started!

And, second, off-site processor packages must do their best to make sure
that a GetPaid :class:`Order` object is created for every off-site
transaction that takes place, and that the order is moved into the
:const:`CHARGED` or :const:`PAYMENT_DECLINED` state.  This logic can
either be invoked by the “Welcome back” pages already mentioned, or by a
special page that receives a direct POST notification from the payment
processing service.  For more details, see the section on `Creating and
resolving an Order`_ below.

Your payment processor class
----------------------------

In the :doc:`writing-a-payment-processor` chapter, we started to
construct a sample payment processor class.  Now we will learn how to
finish it.



Your payment processor should specify at which step in the checkout
process it needs to be inserted, and also provide a view that can render
the HTML that needs to be inserted there.


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



Creating and resolving an Order
-------------------------------
