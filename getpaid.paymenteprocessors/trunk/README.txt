This is initial code for supporting multiple payment processors on getpaid site.

This code is unfinished - do not touch until ask permission, ok? :)

Installation
------------

As the last GetPaid plug in, add ''getpaid.paymentprocessers'' egg to your ''zcml'' direction in ''buildout.cfg''.


Architecture
------------

Payment processor logic code is registered as usual.

To enable multiple payment processor support in the user interface,
payment processors register several views::

    <paymentprocessors:registerProcessor
       name="dummy"
       processor="getpaid.paymentprocessors.tests.dummies.DummyButton"
       selection_view="getpaid.paymentprocessors.tests.dummies.DummyButton"
       thank_you_view="getpaid.paymentprocessors.tests.dummies.DummyThankYou"
       />
       
To see available registration options, please read directives.py / IRegisterPaymentProcessorDirective.



