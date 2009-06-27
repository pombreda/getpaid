This package adds multiple payment processors support for Plone GetPaid shops.

Purpose
-------

This package provides generic payment processor registration methods. Though the code itself is without Plone dependencies,
this documentation covers Plone also.

Installation
------------

Install https://getpaid.googlecode.com/svn/getpaid.paymentprocessors/trunk

Use branch https://getpaid.googlecode.com/svn/Products.PloneGetPaid/branches/multiplepaymentprocessors as Products.PloneGetPaid::

	cd src
	rm -rf Products.PloneGetPaid
	rm -rf getpaid.nullpayment
	svn co https://getpaid.googlecode.com/svn/Products.PloneGetPaid/branches/multiplepaymentprocessors Products.PloneGetPaid
	svn co https://getpaid.googlecode.com/svn/getpaid.nullpayment/branches/multiplepaymentprocessors getpaid.nullpayment

Add ''getpaid.paymentprocessers'' egg to your''buildout.cfg''.

Add ''getpaid.paymentprocessers'' zcml to your''buildout.cfg''.

Administration
--------------

Checkout wizard's payment method selection step is rendered only if the site has two or more active payment processors. 
Payment processors must be manually actived from the site setup after installation.

Creating your own payment processor
-----------------------------------

Payment processor directive
===========================

Payment processors are registered using a ZCML directive::

    <!-- Register logic class dealing with the actual payment -->

  	<adapter
     for="getpaid.core.interfaces.IStore"
     provides="getpaid.core.interfaces.IPaymentProcessor"
     factory=".null.NullPaymentAdapter"
     name="Testing Processor"
     />
     
    <!-- Register payment processor specific user interface parts -->

    <paymentprocessors:registerProcessor
       name="Testing Processor"
	   i18n_name="Test Payment"
       selection_view="null_payment_button"
       review_pay_view="null_payment_pay_page"
       thank_you_view="null_payment_thank_you_page"
       settings_view="null_payment_settings_page"
       />
       
              
It is recommended best practice to put paymentprocessor directive into a separate ZCML file in your getpaid extension module 
to maintain backwards compatibility. You can do it using zcml condition::

  <include zcml:condition="installed getpaid.paymentprocessors" file="paymentprocessors.zcml" />
  
  
paymentprocessors:registerProcessor attributes
++++++++++++++++++++++++++++++++++++++++++++++

Below is explanation for ''registerProcessor'' attributes.

'''name''': This must match getpaid.core.interfaces.IPaymentProcessor adapter name

'''i18_name''': This is the user visible name of the payment processor. It might appear in the summaries and listing. 
  Term "payment method" is recommended here for more end user friendly language.
  
'''selection_view''': This is a <browser:page> registration name which renders the payment method selection button on payment
method selection checkout wizard step. The browser view class should be subclasses from Products.GetPaid.browser.checkout.BasePaymentMethodButton.

selection_view template should render a <tr> element which is rendered on the checkout payment method selection page. It contains three columns:

	- <td> having <input type="radio"> button with accessibility <label>

	- <td> with payment method name/logo image

	- <td> with description. You can override this template to have clauses like "Using PayPal will cost 2$ extra"
	
For example, see getpaid.nullpayment/templates/button.pt

'''review_pay_view'''': This view renders payment processor specific "review and pay" view in the checkout wizard. The attribute
holds the registered <browser:page> name. This view should be subclass of Products.PloneGetPaid.browser.checkout.CheckoutReviewAndPay.
To change the review and pay page template, override template attribute of the class.

Usually review and pay page has two purposes::
	
	- Render a <form> which is submitted to the payment authorization server with a callback back to the shop server
	
	- Do a HTTP redirect or Javascript redirect and take the user to the payment authorization server for an external review payment page

'''settings_view''': This is currently unused. It is reserved to override the default payment processor options screen in site setup.

'''thank_you_view''': This should point to the <browser:page> which is rendered after the payment processor is complete. It is unused currently.
Payment processor review_pay_view is itself responsible to point the user back to the shop site after the payment has been authorized.

See https://getpaid.googlecode.com/svn/getpaid.nullpayment/branches/multiplepaymentprocessors/src/getpaid/nullpayment/paymentprocessors.zcml
for more info.

Checkout
--------

A checkout wizard contains a step "checkout-payment-method" which allows the user to select the wanted payment method.


Testing
-------

Tests required Plone are in Products.PloneGetPaid.tests.test_payment_processors. It is recommended to take a look on 
Products.PloneGetPaid.tests.test_payment_processors.test_payment how to programmatically play around with the checkout wizard.

Non-plone related functionality is tested in getpaid.paymentprocessors.tests. This mainly involves testing ZCML validy.

Developer snippets
-------------------

Payment processors are described by Entry objects which simply hold the information provided by IRegisterPaymentProcessorDirective.

To get active payment processors call::

	from Products.PloneGetPaid import payment

	processors = payment.getActivePaymentProcessors(context) # context = any Plone site object

In checkout wizard, you can get the user chosen payment method using the following snippet. You can do this *after* the user
has passed payment method selection step::

	payment_method_name = wizard.getActivePaymentMethod()

Payment processor registry is available in getpaid.paymentprocessors.registry.paymentProcessorRegistry. This registry
holds the data of registered payment processor code objects. 

Activated payment processor names are stored in portal_properties as LinesField::

	portal_properties.payment_processor_properties.enabled_processors
