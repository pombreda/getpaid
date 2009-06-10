This is initial code for supporting multiple payment processors on getpaid site.

Purpose
-------

This package provides generic payment processor registration methods. Though the code itself is without Plone dependencies,
payment processor code is documented here.

Installation
------------

Use branch https://getpaid.googlecode.com/svn/Products.PloneGetPaid/branches/multiplepaymentprocessors as Products.PloneGetPaid::

	cd src
	rm -rf Products.PloneGetPaid
	rm -rf getpaid.nullpayment
	svn co https://getpaid.googlecode.com/svn/Products.PloneGetPaid/branches/multiplepaymentprocessors Products.PloneGetPaid
	svn co https://getpaid.googlecode.com/svn/getpaid.nullpayment/branches/multiplepaymentprocessors getpaid.nullpayment

Add ''getpaid.paymentprocessers'' egg to your''buildout.cfg''.

Add ''getpaid.paymentprocessers'' zcml to your''buildout.cfg''.

Architecture
------------

Payment processors are registered using a ZCML directive.

    <paymentprocessors:registerProcessor
       name="dummy"
       processor="getpaid.paymentprocessors.tests.dummies.DummyButton"
       selection_view="getpaid.paymentprocessors.tests.dummies.DummyButton"
       thank_you_view="getpaid.paymentprocessors.tests.dummies.DummyThankYou"
       />

Each view is the view name what is used to render the corresponding part. Those must map to registered <browser:page> objects.

To see available directive attributes, please read directives.py / IRegisterPaymentProcessorDirective.

Payment processor registry is available in getpaid.paymentprocessors.registry.paymentProcessorRegistry. This registry
holds the data of registered payment processor code objects. Active payment processors are determined by Products.PloneGetPaid.

Payment processors are described by Entry objects which simply hold the information provided by IRegisterPaymentProcessorDirective.

To get active payment processors call::

	from Products.PloneGetPaid import payment

	processors = payment.getActivePaymentProcessors(context) # context = any Plone site object

UI drop ins
-----------

selection_view
==============

This is a <tr> element which is rendered on the checkout payment method selection page. It contains three columns:

	- Name/logo, preferably an image <button>

	- Description

	- Plain text <button> "Use this method"

There is context variable "processor" available which referse to registered Entry object of the payment processors.

<button> elements must have name which can be obtained from the context::

other views
===========

Other UI drop ins are normal <browser:page> views.

Checkout
--------

A checkout wizard contains a step "checkout-payment-method" which allows the user to select the wanted payment method.

This

Administration
--------------

GetPaid admin interface has page "" where the site manager can enable payment processors and enter to the payment processor settings pages.

Each payment processor setting page must be uniquely named. This goes against the prior GetPaid best practice to have just one page.

Active payment processor names are stored in portal_properties as LinesField::

	portal_properties.payment_processor_properties.enabled_processors


Testing
-------

Non-plone related functionality is tested in getpaid.paymentprocessors.tests. This mainly involves testing ZCML validy.

Plone related functionality is tested in Products.PloneGetPaid.tests.test_payment_processors.


