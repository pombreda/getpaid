
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

On-site and off-site processing
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
user interface.  While running an on-site payment processor will place a
high security burden on your web servers, they are relatively easy to
write: you just have to write three functions, :func:`authorize()`,
:func:`capture()`, and :func:`refund()`, with which GetPaid can create
and finalize a charge against a customer's credit card.  Off-site
payment processors, on the other hand, have to step into the normal
GetPaid checkout process at some point and subvert it so that the user's
browser is sent elsewhere.  This makes them more complicated than their
on-site brethren, but, as you will see from the instructions below, we
have tried to make them, too, as easy for you to write as possible.
