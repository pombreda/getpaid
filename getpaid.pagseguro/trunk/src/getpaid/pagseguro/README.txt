To install the product, besides adding getpaid.pagseguro at eggs and zcml sections you also need to add 
zcml =   getpaid.pagseguro-overrides
and make sure there is not other getpaid override (such as getpaid.paypal, foprexample)

You will need to set this as your payment processor in the getpaid admin
interface (Payment Options)

Last step is to enter your pagseguro email info in Payment Processor
Settings. You may also want to add your generated TOKEN if return functionality is desired

Enjoy!
