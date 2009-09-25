
Off-site Payment Processors
===========================

By definition, an “off-site payment processor” redirects the user's web
browser off-site at some point during the GetPaid checkout process.
Writing support for an off-site solution can be a bit complicated,
because you have think through every GET and POST that will be involved
along the way as the user is sent off-site and then returns.  But if you
simply tackle the issues one at a time, you should find the process of
writing your payment processor quite manageable.

There are several steps involved in writing an off-site payment
processor, so here they are, in a simple list.  Use this list as an
overview to keep you oriented you as you read through this document, and
also as a checklist to make sure you have covered everything when you
think your payment processor package is nearing completion.

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
   refund the customer instead.  (Some off-site processors might only
   support these actions on their own web site, in which case the store
   owner will have to log in there to manage their orders.)

If any of these steps sound complicated, then, well, there's the chance
that they are — depending, largely, on how complicated the payment
processing site is that you are trying to tie GetPaid into.  But we have
tried to make your GetPaid development experience as easy as possible,
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
tell GetPaid which view to render to replace either the shopping cart
check-out button or the review-and-pay credit-card form.  The result, at
its simplest, looks something like this::

    from getpaid.core.processors import OffsitePaymentProcessor
    from getpaid.chargeit.interfaces import IChargeItOptions

    from zope.i18nmessageid import MessageFactory
    _ = MessageFactory('getpaid.chargeit')

    class ChargeIt(OffsitePaymentProcessor):
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
shopping cart view.  (Specifically, it will be placed at the bottom of
both the cart portlet in the sidebar, and on the main cart web page).
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

The three arguments used to instantiate your class are each simply
stored in an attribute of the same name by the ``__init__()`` method
that you inherit from ``OffsitePaymentProcessor``, so you can access
them easily.  The three values are:

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
by using a property::

    class ChargeIt(OffsitePaymentProcessor):
        ...
        @property
        def payment_form(self):
            if self.options.inEuropeanUnion:
                return 'euro-form'
            else:
                return 'world-form'

The likelihood of needing this flexibility is small.  After all, you can
create a single view whose outer level is a big “if” statement as easily
as you could provide two separate views, like this, with a switch to
decide between them.  But the ability is there if you ever need it.

Writing views
-------------

Since an off-site payment processor diverts the user away from the
natural course of an on-site GetPaid checkout, it is going to have to
render some HTML — you will have to write at least a modest link
pointing off-site, and quite possibly a complete form.  In addition, you
are going to have to prepare landing pages to which the user will return
when they are done checking out, and you might also create URLs through
which the off-site processor can provide updates to GetPaid as the buyer
steps through their checkout process.

The views you create will fall into two genres.  First, you will create
the HTML “snippets”, discussed in the previous two sections, that are
designed to be seen by the user and will be inserted into the theme of
the larger web site of which GetPaid is a part.  Checkout buttons,
review-pay forms, and welcome-back pages all fall into this category.
Second, you may also design complete web pages over which you have full
control — and which will often be in machine formats like XML or JSON —
for consumption by the off-site payment service.

With what technology should you create your views?  There are several
technologies for constructing them in the Zope world today.  We
recommend using Five_, which is advanced enough to be sleek and modern,
but established enough to be fairly widespread and something that other
developers will understand.

There is a nice, compact tutorial on `Creating a minimalistic Zope 3
View`_ at http://plone.org/ that you should consult for details.  But
the basic idea is that your Five-powered view will consist of three
things: a page template file containing HTML; a “view” class that pulls
together the data that the HTML needs; and, finally, a ZCML declaration
telling GetPaid that your class and template go together.  To see how
these three files work together to support a view, see the examples in
the sections that follow.

Sending the customer off-site
-----------------------------

The first view you will probably write is the checkout button or payment
form that sends the user off-site.  Here is a very modest example of
what it might look like:

.. code-block:: html

    <!-- getpaid/chargeit/templates/pay_form.pt -->

    <!-- In a template, "view" is an instance of your
         view class, and "context" is an instance of
         your payment processor class. -->

    <div>
      <a tal:attributes="href view/offsite_url"
         href="http://url.goes.here/">
         Check out using
         <span tal:replace="context/title">
           ChargeIt
         </span>
       </a>
    </div>

::

    # -- getpaid/chargeit/views.py --

    from Products.Five import BrowserView
    class PayForm(BrowserView):
        @property
        def offsite_url(self):
            if self.context.options.for_real is True:
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
        name="pay-form"
        class=".views.PayForm"
        template="pay_form.pt"
        permission="zope2.View"
        />

      ...

    </configure>

The view that sends your user off-site should, as in this example,
declare that it is a view ``for=`` your own payment processor class.
This gives the view an interesting property: it will have no URL!
Because your payment processor itself has no URL in a GetPaid-powered
site, the user cannot add (in this example) ``/pay_form`` to the end of
that URL and activate the view.  This limitation is deliberate: users
should *not* be able to run your view logic unless GetPaid is already
rendering a checkout page that the view belongs on.

The key features that make the above example a fully-working view for
sending the user off-site are simply that:

1. The *name* of the view matches the name that GetPaid will receive
   when it asks your payment processor instance for the value of its
   ``checkout_button`` or ``payment_form``.

2. The *context* for which the view is declared (``for=``) is your
   payment processor class itself.

There are a few other things going on in the above code which we should
note, in case you are new to writing Zope 3 views.

First, note that instead of hard-coding the payment processor name
(“ChargeIt”) in the view, we ask it for its ``title`` instead.  This
gives the store owner the chance to provide a translation suitable to
their locale, since the title in the class's definition is wrapped with
a standard Zope ``_()`` translation wrapper.  You should try to provide
this convenience for every customer-facing phrase that your view
generates.

Also, note that when GetPaid wants one of your views rendered, it
instantiates a copy of your payment processor and provides it with
objects that become the attributes ``options``, ``shopping_cart``, and
``order``.  This means that all three of these things are available
inside of your view class's methods, where you can get to them with
expressions like::

    self.context.options
    self.context.shopping_cart
    self.context.order

They are also available inside the view itself, through TAL expressions
like::

    context/options
    context/shopping_cart
    context/order

The example above makes use of this by accessing the payment processor
``options`` to determine whether users should be sent off-site to the
service's testing “sandbox”, or to the real production service that
actually takes money from real credit cards.

Since order management is an important topic, we will talk more about it
below, in its own section.  But we should at least note here that the
third of the three values above — the ``order`` — will be ``None`` if
your view is a ``checkout_button``, since at that point the checkout
process has not actually started; but for a ``payment_form`` will be an
``Order`` object holding all of the information about the buyer, their
address, and their shipping preferences that was collected through the
preceding steps of the GetPaid checkout process.

The example view given above is overly simple, of course, because it
makes no effort to transmit to the off-site processor the store owner's
merchant ID, the contents of the shopping cart, or even the total
payment that is due to complete the transaction.  That is why your view
will probably be a form with several hidden fields, rather than a simple
link like this.  But, however complex it becomes, your view will work
because it has the same basic features as the small view shown above.

GetPaid URLs
------------

In the next few sections of this document, we are going to talk about
views that have real URLs on the GetPaid-powered web site.  Before
examining them, we should look at how GetPaid URLs are constructed.

At the center of the GetPaid customer experience is a “Store”.  The
store is, from the point of view of the site owner, the module that they
have added to their web site to make GetPaid available for their users.
From the point of view of you, the developer, the store is first and
foremost the base object off of which all GetPaid URLs are hung.

Let's consider an example web site that lives at::

    http://example.com/

Depending on which web framework has been used to build the site, the
store might be located one of two places.  If the site is powered by
Plone or another Zope-based framework that supports adapter-based
views, then the GetPaid installation process will probably mark the site
root itself as the :class:`IStore` and GetPaid URLs will look like::

    http://example.com/cart
    http://example.com/checkout
    http://example.com/chargeit-thank-you
    http://example.com/chargeit-declined

But most other web frameworks do not make it easy to mix in lots of
views down at the site root; indeed, they would consider this a design
flaw, because of the chance that two add-on products would have views of
the same name.  So, under most other frameworks, the GetPaid install
process involves choosing a URL for the store that lives one level (or
more) below the site root, like::

    http://example.com/shop

The store owner is free to choose a name that fits with the logic of
their site design, like ``shop`` or ``store`` or ``buy`` or, if they are
brand-loyal, maybe even ``getpaid``.  In any case, in these other web
frameworks, GetPaid views will appear beneath the store URL instead of
up at the site root, like this::

    http://example.com/shop/cart
    http://example.com/shop/checkout
    http://example.com/shop/chargeit-thank-you
    http://example.com/shop/chargeit-declined

How, when writing view code, can you compute these URLs for yourself?
You might need them, especially if you have to inform the off-site
payment service of one of your view's URL.  The answer is that the store
object is always available as a utility, and can always — regardless of
what web framework you are running under — report its URL if you call
its :meth:`~IStore.absolute_url()` method.  The checkout wizard's URL,
for example, can be computed with::

    import zope.component

    store = zope.component.getUtility(IStore)
    store_url = store.absolute_url()
    checkout_url = store_url.rstrip('/') + '/checkout'

As suggested by the example URLs given above, the URLs available beneath
the GetPaid :class:`IStore` are a mix: some of them are views that come
packaged with GetPaid, while others are provided by your payment
processor and any other payment processors that are installed.

To prevent collisions among these view names, we strongly suggest that
you start all of your view names with the name of your payment processor
module, as we did with the fictitious ``chargeit-`` views shown in the
URL list above.

Setting up the welcome-back views
---------------------------------

The second kind of views you will have to provide (the first, you will
recall, is the HTML that sends the customer off-site) are the screens
that welcome the user back when they are done checking out through the
off-site service.  These views will need an actual URL, so that the
user's web browser can load them.

If the off-site processor provides its own “Authorization successful”
and “Payment declined” screens, and only forwards the user back once the
whole shopping experience is complete, then you will probably provide
only a single landing page for the user's return.  But if the off-site
payment service simply redirects the user back with some sort of a code
indicating whether payment succeeded, then you will need to provide a
view (or several views) that let the user know what happened.


.. code-block:: html

    <!-- getpaid/chargeit/templates/landing.pt -->

    <div>
      <p tal:condition="view/is_success">
        Thank you for your order!<br/>
        <a tal:attributes="href view/store_url">Click here</a>
        to continue shopping.
      </p>
      <p tal:condition="view/is_failure">
        Your attempt to check out was not successful.<br/>
        <a tal:attributes="href view/cart_url">Click here</a>
        to return to your shopping cart.
      </p>
      <p tal:condition="view/is_error">
        Please <a tal:attributes="href view/store_url">return to
        our front page</a>.
      </p>
    </div>

::

    # -- getpaid/chargeit/views.py --

    from Products.Five import BrowserView
    class PayForm(BrowserView):
        @property
        def offsite_url(self):
            if self.context.options.for_real is True:
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
        name="chargeit-landing"
        class=".views.Landing"
        template="landing.pt"
        permission="zope2.View"
        />

      ...

    </configure>

Creating and resolving an Order
-------------------------------

An off-site processor packages must do their best to make sure
that a GetPaid :class:`Order` object is created for every off-site
transaction that takes place, and that the order is moved into the
:const:`CHARGED` or :const:`PAYMENT_DECLINED` state.  This logic can
either be invoked by the “Welcome back” pages already mentioned, or by a
special page that receives a direct POST notification from the payment
processing service.  For more details, see the section on `Creating and
resolving an Order`_ below.

.. _Creating a minimalistic Zope 3 View: http://plone.org/documentation/how-to/creating-a-minimalistic-zope-3-view
.. _Five: http://codespeak.net/z3/five/

