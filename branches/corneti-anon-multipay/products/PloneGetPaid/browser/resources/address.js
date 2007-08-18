function cloneBillingAddress(e)
{
    if (!e) var e = window.event;
    if (e.target) target = e.target;
    else if (e.srcElement) target = e.srcElement;
	if (target.nodeType == 3) target = targ.parentNode;
	changeShippingAddressVisibility(! target.checked);
	/*
	if (target.checked)
	    //NOTE: instead of cloning, hide shipping address (discuss)
	    cloneFields('form.bill_', 'form.ship_');
	    hideShippingAddress();
	else:
	    showShippingAddress();
	*/
}

function changeShippingAddressVisibility(show)
{
    shippingAddressFieldset = document.getElementById('shipping-address-fieldset');
    if (show)
    {
        shippingAddressFieldset.style.display = 'block';
    }
    else
    {
        shippingAddressFieldset.style.display = 'none';
    }
}



function cloneFields(sourcePrefix, targetPrefix)
{
    var fieldLabels = document.getElementsByTagName('label');
    for(var l=0; l<fieldLabels.length; l++)
    {
        var label = fieldLabels[l];
        var sourceWidgetId = label.getAttribute('for');
        var sourceWidget = document.getElementById(sourceWidgetId);
        if (sourceWidget && sourceWidgetId.substr(0, sourcePrefix.length) == sourcePrefix)
        {
            var targetWidgetId = sourceWidgetId.replace(sourcePrefix, targetPrefix);
            var targetWidget = document.getElementById(targetWidgetId);
            if(sourceWidget.tagName == 'SELECT')
            {
                targetWidget.value = sourceWidget.value;
            }
            else
            {
                targetWidget.value = sourceWidget.value;
            }
        }
    }
}