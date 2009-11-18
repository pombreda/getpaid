GetPaid Virtual Merchant Payment Processor
=======================================


Store Specific Processor Setting Tests
--------------------------------------

Provide the processor with details about the Virtual Merchant merchant
account:

    >>> from getpaid.virtualmerchant.interfaces import IVirtualMerchantOptions
    >>> options = IVirtualMerchantOptions(portal)
    >>> options.merchant_id = '123456'
    >>> options.merchant_pin = 'V6NJ3A'

Create a shopping cart:

    >>> from zope.component import getUtility
    >>> from getpaid.core.interfaces import IShoppingCartUtility
    >>> cart = getUtility(IShoppingCartUtility).get(portal, create=True)

and add a couple of entries to this cart:

    >>> from getpaid.core.item import LineItem
    >>> line = LineItem()
    >>> line.item_id = 'book-9789988647131'
    >>> line.name = 'Not Without Flowers'
    >>> line.description = 'ISBN: 9789988647131'
    >>> line.cost = 19.95
    >>> line.product_code = '9789988647131'
    >>> line.quantity = 2
    >>> cart[line.item_id] = line

    >>> line = LineItem()
    >>> line.item_id = 'book-9789780232412'
    >>> line.name = 'Echoes from the Mountain'
    >>> line.description = 'ISBN: 9789780232412'
    >>> line.product_code = '9789780232412'
    >>> line.cost = 14.95
    >>> line.quantity = 1
    >>> cart[line.item_id] = line

Authorizing an Order
--------------------       

The processor can generate XML to be sent to the Virtual Merchant site.
    
    >>> from zope.component import getAdapter
    >>> from getpaid.core.interfaces import IPaymentProcessor
    >>> processor = getAdapter(portal, IPaymentProcessor, 'Virtual Merchant')
    >>> options = dict(
    ...    ssl_merchant_id = '123456',
    ...    ssl_user_id = 'V6NJ3A',
    ...    ssl_pin = '123456',
    ...    ssl_transaction_type = 'ccsale',         
    ...    ssl_card_number = '1111111111111111',
    ...    ssl_exp_date = '1210',
    ...    ssl_amount = '2.34',
    ...    ssl_sales_tax = '0.00',
    ...    ssl_cvv2cvc2_indicator = '1',
    ...    ssl_cvv2cvc2 = '321',
    ...    ssl_invoice_number = '1234',
    ...    ssl_customer_code = '',
    ...    ssl_first_name = 'Johnny',
    ...    ssl_last_name = 'BGoode',
    ...    ssl_avs_address = '123 My Wonderful Street',
    ...    ssl_city = 'Bluesville',
    ...    ssl_state = 'Tennesee',
    ...    ssl_avs_zip = '1234',
    ...    ssl_phone = '111-1111-1111',
    ...    ssl_email = 'johnny@bgoode.com'
    ...    )
    >>> xml = processor.createXML( options )
    >>> from elementtree.ElementTree import tostring
    >>> tostring(xml)
    '<txn><ssl_invoice_number>1234</ssl_invoice_number><ssl_email>johnny@bgoode.com</ssl_email><ssl_user_id>V6NJ3A</ssl_user_id><ssl_amount>2.34</ssl_amount><ssl_transaction_type>ccsale</ssl_transaction_type><ssl_cvv2cvc2>321</ssl_cvv2cvc2><ssl_sales_tax>0.00</ssl_sales_tax><ssl_last_name>BGoode</ssl_last_name><ssl_merchant_id>123456</ssl_merchant_id><ssl_avs_address>123 My Wonderful Street</ssl_avs_address><ssl_cvv2cvc2_indicator>1</ssl_cvv2cvc2_indicator><ssl_state>Tennesee</ssl_state><ssl_card_number>1111111111111111</ssl_card_number><ssl_first_name>Johnny</ssl_first_name><ssl_avs_zip>1234</ssl_avs_zip><ssl_pin>123456</ssl_pin><ssl_city>Bluesville</ssl_city><ssl_customer_code /><ssl_phone>111-1111-1111</ssl_phone><ssl_exp_date>1210</ssl_exp_date></txn>'    
