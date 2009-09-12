
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

    class GoogleCheckout(object):
        implements(IOnSitePaymentProcessor)
        name = u'Google Checkout'
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

Third and finally, each payment processor needs to provide a ``name``
for use in the GetPaid admin interface.  When a store owner is setting
up GetPaid, they are given a menu of available payment processors to
choose from.  The string you provide as ``name`` will be the choice by
which the store owner can choose your payment processor.


