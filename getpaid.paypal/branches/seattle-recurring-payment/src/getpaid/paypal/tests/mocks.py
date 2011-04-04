from zope.interface import implements
from getpaid.core import order, item, cart
from getpaid.core import interfaces as coreinterfaces

class MockContactInfo(object):
    name = ''
    email = ''

class MockBillingAddress(object):
    bill_first_line = ''
    bill_city = ''
    bill_state = ''
    bill_postal_code = ''
    bill_country = ''

class MockShippingAddress(object):
    ship_same_billing = True  

class MockPayPalOptions(object):
    server_url = 'Sandbox'
    merchant_id = 'fti_1260762824_per@wesleyan.edu'
    currency = 'USD'
    
class MockGetpaidOptions(object):
    store_name = 'Some Merchant Name'




class MockOrderManager(object):
    implements(coreinterfaces.IOrderManager)
    
    def __init__(self):
        self.order = order.Order()
        self.order.contact_information = MockContactInfo()
        self.order.billing_address = MockBillingAddress()
        self.order.shipping_address = MockShippingAddress()
        self.order.shopping_cart = cart.ShoppingCart()
        
        line = item.ShippableLineItem()
        line.product_code = '01uT0000000vbZyIAI'
        line.quantity = 1
        
        self.order.shopping_cart['01uT0000000vbZyIAI'] = line
        self.storage = {'729492128' : self.order}
    
    def __contains__( self, order_id ):
        return order_id in self.storage
    
    def get(self, id):
        return self.storage[id]



def CART_IPN_MOCK():
    """ An IPN response for a cart with a single item
    """
    return {'address_city': 'San Jose',
            'address_country': 'United States',
            'address_country_code': 'US',
            'address_name': 'Test User',
            'address_state': 'CA',
            'address_status': 'confirmed',
            'address_street': '1 Main St',
            'address_zip': '95131',
            'business': 'seller@sale.com',
            'charset': 'windows-1252',
            'custom': '',
            'discount': '0.0',
            'first_name': 'Test',
            'insurance_amount': '0.00',
            'invoice': '729492128',
            'item_name1': 'A Very Nice Item for Sale',
            'item_number1': '123456789',
            'last_name': 'User',
            'mc_currency': 'USD',
            'mc_fee': '6.06',
            'mc_gross': '198.63',
            'mc_gross_1': '159.00',
            'mc_handling': '0.00',
            'mc_handling1': '0.00',
            'mc_shipping': '25.00',
            'mc_shipping1': '0.00',
            'notify_version': '2.8',
            'num_cart_items': '1',
            'payer_email': 'buyer@buy.com',
            'payer_id': 'S62GN7KJQMLD4',
            'payer_status': 'verified',
            'payment_date': '14:48:19 Jan 05, 2010 PST',
            'payment_fee': '6.06',
            'payment_gross': '198.63',
            'payment_status': 'Completed',
            'payment_type': 'instant',
            'protection_eligibility': 'Eligible',
            'quantity1': '1',
            'receiver_email': 'seller@sales.com',
            'receiver_id': 'KADNEBA3EW5C8',
            'residence_country': 'US',
            'shipping_discount': '0.00',
            'shipping_method': 'Standard Domestic',
            'tax': '14.63',
            'tax1': '0.00',
            'test_ipn': '1',
            'transaction_subject': 'Shopping Cart',
            'txn_id': '0LD62055GR024251B',
            'txn_type': 'cart',
            'verify_sign': 'AwogoH8napMBdR80EfC1QAyg-i9SA5vkBJQeaLJ9ymuWLRv8WOvcj8vx'}

def NON_CART_MOCK_IPN():
    """ Mock IPN response for single item (not a cart)
    """
    return {'business': 'seller@sales.com',
            'charset': 'windows-1252',
            'custom': '',
            'first_name': 'Test',
            'handling_amount': '0.00',
            'invoice': '1266956620P83',
            'item_name': 'A Nice Item',
            'item_number': '701T0000000E80vIAC',
            'last_name': 'User',
            'mc_currency': 'USD',
            'mc_fee': '0.34',
            'mc_gross': '1.29',
            'notify_version': '2.9',
            'payer_email': 'buyer@buy.com',
            'payer_id': 'S62GN7KJQMLD4',
            'payer_status': 'verified',
            'payment_date': '12:25:05 Feb 23, 2010 PST',
            'payment_fee': '0.34',
            'payment_gross': '1.29',
            'payment_status': 'Completed',
            'payment_type': 'instant',
            'protection_eligibility': 'Ineligible',
            'quantity': '1',
            'receiver_email': 'seller@sales.com',
            'receiver_id': 'KADNEBA3EW5C8',
            'residence_country': 'US',
            'shipping': '0.00',
            'tax': '0.00',
            'test_ipn': '1',
            'transaction_subject': 'A Nice Item Subject',
            'txn_id': '8NY65075JW799325G',
            'txn_type': 'web_accept',
            'verify_sign': 'AwpTgBWvew.S7XKiFBHeNH-yulHIAJA7afUpwoz5Fud7erFjA3kahIWn'}

