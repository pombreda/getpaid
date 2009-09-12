
Writing a Payment Processor for GetPaid
=======================================

Welcome, developers!

This document is intended to be a comprehensive guide to writing payment
processors for the GetPaid e-commerce framework.  At the moment, it is a
mere draft. Actually, it is worse than a mere draft: it is actually
simply a proposal, describing interfaces which are not yet even written.

Why do I write about fictions?  Because I, Brandon Rhodes, am looking to
clean up and improve how payment processors are written in GetPaid, and
this guide to a fictitious development process is the best way I know to
get everyone to think through my ideas about how payment processor
integration should work.

So, sit down, grab a cup of coffee, and imagine with me what it might
soon be like to write a GetPaid payment processor.

On-site and Off-site Processing
-------------------------------

The first thing we need to establish is the difference between the two
kinds of payment processor that GetPaid can use.

The essential distinction is whether the user's web browser ever gets
redirected away from your GetPaid-powered web site and to the web site
of the payment company you are using.

* If the user never leaves your web site, and their web browser never
  sends a GET or POST to the payment processing system you are using,
  then you are doing “on-site” payment processing: GetPaid is powering
  the entire user experience.  The form that contains the user's credit
  cart number will POST to GetPaid's checkout form, and the actual
  process of contacting the merchant processing system to charge their
  card happens behind the scenes from the user's point of view.

* If the user *does* leave your site, such that the user's browser POSTs
  a form to the payment processor's web site, or is redirected there to
  finish entering their credit card information, then you are doing
  “off-site” payment processing.  This is true even if the user does not
  know that they were sent off-site because their POST was immediately
  followed by a redirect back to your own site: as long as the credit
  card number POSTs to some other web site, you are dealing with an
  “off-site” solution.

This distinction is crucial, because there are many restrictions these
days placed upon web sites that are going to handle credit card data.
An off-site payment processing system that receives the credit card
number for you without ever letting your site see it, like PayPal or
Google Checkout, is a very popular way for site administrators to wipe
their hands of the whole affair and put somebody else on the hook for
handling sensitive financial data.

The distinction is also crucial for you, the GetPaid developer, because
it determines whether you are going to have to interact with the GetPaid
user interface — all of those forms and buttons that are presented to
the user.  While running an on-site payment processor places a high
security burden on your web servers, they are at least relatively easy
payment processors to write: you just have to make three functions,
:func:`authorize()`, :func:`capture()`, and :func:`refund()`, with which
GetPaid can create and finalize a charge against a customer's credit
card.  Off-site payment processors, on the other hand, have to step into
the GetPaid checkout process at some point and subvert it so that the
user's browser is sent elsewhere.

Payment Processor Basics
------------------------

Whether you are writing an on-site or off-site payment processor, you
will need to create a Python class that tells GetPaid everything about
interfacing with your payment processor.  The first information that
GetPaid will need is what kind of payment processor you are writing, and
what the processor should be called in the menu from which the store
owner selects which payment processor to use.  The top of your payment
processor class definition will look something like this::

    from zope.interface import implements
    from getpaid.core.interfaces import IOnSitePaymentProcessor

    class ChargeIt(object):
        implements(IOnSitePaymentProcessor)
        name = 'charge-it'
        title = _(u'ChargeIt checkout')
        ...

First, notice that the payment processor is not burdened with the need
to inherit from any particular class; here, in fact, we see a payment
processor inheriting from the completely generic ``object`` class.  Of
course, if another class has functionality that you want to inherit and
specialize, then by all means inherit from it.  But GetPaid cares only
about how your class behaves, not how it is implemented, so just inherit
from ``object`` unless you know you need a more specific parent class.

Second, every payment processor needs to implement one of the two basic
GetPaid payment processor interfaces:

* :class:`IOnSitePaymentProcessor` for on-site payment.
* :class:`IOffSitePaymentProcessor` for off-site payment.

Third, a payment processor needs to declare a ``name`` that can be used
in URLs and in other places where a brief string is needed to identify a
given payment processor.  The ``name`` should consist only of lower-case
letters and dashes.

Fourth and finally, each payment processor needs to provide a ``title``
for use in the GetPaid admin interface.  When a store owner is setting
up GetPaid, they are given a menu of available payment processors to
choose from.  The string you provide as ``title`` will be the name of
the choice that the store owner can click to select your payment
processor.

Payment Processor Options
-------------------------

Next, each payment processor needs to define the configuration options
that the store owner will need to provide for the payment processor to
operate.  The resulting form might look something like this::

             Charge-It Options

    Merchant account:  __________________
    Merchant password: __________________

    Processing mode:  ☑ Sandbox
                      ☐ Production

Be sure, by the way, to include an option that lets the store owner
choose between “sandbox mode” and “production mode”.  When the former is
selected, your package should still make real API calls to the payment
service, but credit card processing should not actually take place; this
lets store owners test and develop their site but without making actual
purchases.  Look through the payment service's documentation for how
this feature can be selected with their particular API, and then make
sure you give the option to store owners.

To define your processor options, simply create a Zope schema.  For the
sample form shown above, you might write::

    from getpaid.core.interfaces import IPaymentProcessorOptions

    class IChargeItOptions(IPaymentProcessorOptions):
        """Charge-It checkout configuration options."""

        account = schema.ASCIILine(title=_(u"Merchant account"))
        password = schema.ASCIILine(title=_(u"Merchant password"))
        mode = schema.Choice(
            title = _(u"Processing mode"),
            values = (_(u"Sandbox"), _(u"Production")),
            )

To designate this interface as your configuration schema, simply
reference it from your payment processor with a class variable named
``options_schema``.  This expands the sample payment processor
definition cited above so that it reads::

    class ChargeIt(object):
        implements(IOnSitePaymentProcessor)
        name = 'charge-it'
        title = u'ChargeIt checkout'
        options_schema = IChargeItOptions
        ...

Once you have created your options schema and referenced it from your
payment processor class, you are done!  GetPaid will automatically
provide the store owner with a form for configuring your payment
processor, and save the values they enter.  Later, when a customer is
checking out, any of your routines that get called will be passed a
``config`` object, already adapted to your schema, whose attributes
contain the values specified by the site owner.


