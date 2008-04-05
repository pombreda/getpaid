"""

sync options,

 - sync synchronously

 - sync async
 
we want to do several kinds of reports

$Id: $
"""

from getpaid.core import interfaces
from getpaid.warehouse.interfaces import IProductInventory
from zope import component, schema
from sqlalchemy import create_engine
from sqlalchemy.orm import session

import domain

def copyAddress( source_addr, target_addr, prefix=None):
    field_names = schema.getFields( interfaces.IAddress ).keys()
    for f in field_names:
        fn = prefix and "%s_%s"%(prefix, f) or f
        value = getattr( source_addr, fn, None)
        setattr( target_addr, f, value )

def copyItem( source, target ):
    
    i = interfaces.IShippableLineItem.providedBy( source ) \
        and interfaces.IShippableLineItem \
        or interfaces.IPayableLineItem
    
    field_names = set( schema.getFields( i ).keys() )
    field_names.remove('item_id')
    
    for f in field_names:
        value = getattr( source, f, None)
        setattr( target, f, value )

    target.item_zid = source.uid

def copyCustomer( source, target ):
    for f in schema.getFields( interfaces.IUserContactInformation ).keys():
        value = getattr( source, f )
        setattr( target, f, value )

def copyProduct( item, source, target ):

    payable = interfaces.IPayable( source )

    target.content_uid = item.uid
    target.supplier_uid = payable.made_payable_by
    target.product_code = payable.product_code
    target.type = "payable"
    target.price = payable.price

    # copy inventory information if available
    inventory = component.queryAdapter( source, IProductInventory )
    if inventory:
        target.pick_bin = inventory.pickbin
        target.stock = inventory.stock
        target.store_stock= inventory.store_stock

def copyOrder( _session, source, target ):

    # identity info
    target.order_zid = source.order_id
    target.creation_date = source.creation_date
    
    # handle workflow states
    target.finance_status = source.finance_state
    target.fulfillment_status = source.fulfillment_state
    
    # handle addresses
    billing_address = domain.Address()
    copyAddress( source.billing_address, billing_address, 'bill' )
    target.billing_address = billing_address
    
    shipping_address = domain.Address()
    if source.shipping_address.ship_same_billing:
        target.shipping_address = billing_address
    else:
        copyAddress( source.shipping_address, shipping_address, 'ship')
        target.shipping_address = shipping_address

    # handle customer/contact info
    customer = domain.Customer()
    copyCustomer( source.contact_information, customer )
    target.contact_information = customer
    
    # handle line items
    for _item in source.shopping_cart.values():
        item = domain.LineItem()
        copyItem( _item, item )
        target.items.append( item )

        # serialize products if we haven't seen them.
        if not interfaces.IPayableLineItem.providedBy( _item ):
            continue
        
        if _session.query( domain.Product ).filter(
            domain.Product.content_uid == _item.uid ).count():
            continue
        
        payable = _item.resolve()
        if payable is None:
            continue
        
        product = domain.Product()
        copyProduct( _item, payable, product )
        
    
def handleOrderTransition( _order, event ):
    """
    """

def handleNewOrder( _order, event ):
    """
    """
    s = session.Session()
    s.begin()

    try:
        order = domain.Order()
        copyOrder( s, _order, order )
    except:
        s.rollback()
        raise
    else:
        s.save( order )        
        s.commit()


def sync( ):
    
    manager = component.getUtility( interfaces.IOrderManager )
    session = session.Session()

    s = session.Session()
    s.begin()
    #s.save( order )
    s.commit()
    
    
