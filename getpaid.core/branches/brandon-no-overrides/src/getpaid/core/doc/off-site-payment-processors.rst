
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
        payment_form = 'pay_form'

Here, the views names (in the next section we will start discussing the
actual creation of the views themselves) have been specified using
simple class attributes, and in many cases this is all you will need.

The ``checkout_button`` attribute, if not ``None``, should name the view
that will replace the GetPaid checkout button at the bottom of each
shopping cart view (both the cart portlet, and the main cart page).
Similarly, the ``payment_form`` attribute names the view that should be
rendered to supply the bottom pane of the last page of GetPaid's
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

Because GetPaid asks for the ``checkout_button`` and ``payment_form``
attributes of an instance of your class, and not simply of the class
object itself, you have the option of generating the answer dynamically
through code like this::

    class ChargeIt(OffSitePaymentProcessor):
        ...
        @property
        def payment_form(self):
            if self.options.inEuropeanUnion:
                return 'euro-form'
            else:
                return 'world-form'

The likelihood of needing this flexibility is small.  After all, you
could just supply one view whose outer level was a big “if” statement as
easily as you could provide two separate views like this with a switch
to decide between them.  But the ability is there if you ever need it.

Writing views
-------------

Since an off-site payment processor diverts the user away from the
natural course of an on-site GetPaid checkout, it is going to have to
render some HTML — you will have to write at least a modest link
pointing off-site, and quite possibly a complete form.  In addition, you
are going to have to prepare landing pages to which the user will return
when they are done checking out, and may also create URLs with which the
off-site processor can provide updates to GetPaid as the buyer process
through their checkout process.

The views you create will fall into two genres.  First, you will create
HTML “snippets” that are designed to be seen by the user, and that will
be inserted into the theme of the larger web site of which GetPaid is a
part.  Checkout buttons, review-pay forms, and welcome-back pages all
fall into this category.  Second, you may also design complete web pages
over which you have full control — and which will often be in machine
formats like XML or JSON — for the consumption of the off-site payment
service.

Customer-facing views
---------------------

If you have done much programming in Plone, you might be surprised by
some of the properties of the view that you write to provide the HTML
“snippets” that will lead the user off-site and to your payment
processing service.  For one thing, they will typically be declared as
views of a class — your payment processor class — instead of being
“generic” views designed to render every object of a given interface.

Since your payment processor does not have a URL in a GetPaid-powered
site, there is no URL that a user can construct that will force your
views to display.  This is deliberate; users have no business attempting
to run your view code outside of a context in which GetPaid has taken
deliberate steps to display it.

How should you create your views?  There are several technologies for
constructing them in the Zope world today.  We recommend using Five_,
which is advanced enough to be sleek and modern, but established enough
to be fairly widespread and something that other developers will
understand.

There is a nice, compact tutorial on `Creating a minimalistic Zope 3
View`_ at http://plone.org/ that you should consult for details.  Here,
we will mention that your Five-powered view will consist of three
pieces: a page template file with the HTML, a “view” class that puts
together the data that the HTML needs, and, finally, a ZCML declaration
telling GetPaid everything about it.  We should go ahead and give an
example ZCML declaration here, since that is what pulls everything
together where GetPaid can find it:

.. code-block:: html

    <!-- getpaid/chargeit/templates/pay_form.pt -->

    <div>
      <a tal:attributes="href offsite_url"
         href="http://express.chargeit.com/"
         >Check out</a>
    </div>

::

    # -- getpaid/chargeit/views.py --

    from Products.Five import BrowserView
    class PayForm(BrowserView):
        @property
        def offsite_url(self):
            if self.context.options.production is True:
                return 'http://express.chargeit.com/'
            else:
                return 'http://sandbox.chargeit.com/'

.. code-block:: xml

    <!-- getpaid/chargeit/configure.zcml -->

    <configure
      xmlns="http://namespaces.zope.org/zope"
      xmlns:browser="http://namespaces.zope.org/browser">

      ...

      <browser:page
        for="ChargeIt"
        name="pay_form"
        class=".views.PayForm"
        template="pay_form.pt"
        permission="zope2.View"
        />

      ...

    </configure>

The browser page, as usual, links a page template together with a view
class.  But, do you see the key features?  They are what will make this
view work with GetPaid:

1. The *name* of the view matches the same name that GetPaid will
   receive when it asks your class instance for the value of its
   ``checkout_button`` or ``payment_form`` attribute.

2. The *context* for which the view is declared (``for=``) is your
   payment processor class itself.

Remember that when GetPaid wants one of your views rendered, and
instantiates a copy of your payment processor, it provides it with
objects that become the attributes ``options``, ``shopping_cart``, and
``order``.  This means that all three of these are available inside of
your view class's methods, where you can get to them with expressions
like::

    self.context.options
    self.context.shopping_cart
    self.context.order

They are also available inside the view itself, through TAL expressions
like::

    context/options
    context/shopping_cart
    context/order

The example above makes use of this by accessing the payment processor
options to determine whether users should be sent off-site to the
service's testing “sandbox”, or to the real production service that
actually takes money from real credit cards.

The above example is silly, of course, because it makes no effort to
transmit either your store owner's identity as a merchant, nor the
contents of the shopping cart, nor even the total payment that is due to
complete the transaction.  That is why your view will probably be a form
with several hidden fields rather than a simple link like this.  But,
however complex it becomes, your view will be found by GetPaid and will
work because it has the same links to the payment processor as in the
example given above.

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

``payment_form = 'view_name'``
  This says that ...



How are GetPaid URLs constructed?  Every GetPaid installation involves
the creation of a “store”, which has a URL beneath which all of the
GetPaid web pages will live.  For example, consider a Plone site whose
root has been marked as an :class:`IStore`.  If the site has the URL::

    http://store.example.com/

then its GetPaid views will live URLs like::

    http://store.example.com/checkout
    http://store.example.com/thank-you
    http://store.example.com/declined

If, on the other hand, the web site owner has chosen to install the
GetPaid :class:`IStore` a bit deeper in their site, then it would be at
the level beneath that URL that the GetPaid views were available.




store will live at some URL
store_views?
no, normal views registered to IStore




what is your URL?
store = zope.component.getUtility(IStore)
store_url = store.absolute_url()


Welcoming the user back
-----------------------

drat, when does order get created?

 — as best they can;
off-site processors will

establishing a URL on the site to which the
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


Creating and resolving an Order
-------------------------------

.. _Creating a minimalistic Zope 3 View: http://plone.org/documentation/how-to/creating-a-minimalistic-zope-3-view
.. _Five: http://codespeak.net/z3/five/

