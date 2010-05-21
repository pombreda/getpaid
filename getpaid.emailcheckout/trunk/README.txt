Why do I want to use this package?
==================================


In our shop shipping to different countries is possible but shipping costs vary for different items and destination countries.
(and the ups plugin is bound to ups service which is not that common and quite expensive in our region)

Writing a custom sippment plugin that handles all these cases seemed to be too much work for the start.

We have a small website with shop functionality (no dedicated webshop) and expect few orders (about 0-10 per week).

That's why we decided to let our staff calculate shipping costs and handle the payment and fulfillment part
of the shopping process offline.


What this package does
======================

`getpaid.emailcheckout` customize the CheckoutReviewAndPay step so users need not supply
credit card information.


currently orders stay in CHARGING state. getpaid's order interface does not
offer the possibility to set the state to charged atm.



Requirements
============

This package has been developed for and tested with

* Plone 4.0b3 (older plone versions should work though)

* Products.PloneGetPaid >= 0.10.1dev (XXX next release)

