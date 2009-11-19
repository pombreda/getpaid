def setSelectWidget(browser, name, labels):
    """Selects the given labels from a named SelectWidget control. (A
    functional replacement for the JavaScript used by this widget.)
    """
    control = browser.getControl(name='%s.from' % name).mech_control
    form = control._form
    for label in labels:
        value = str(control.get(label=label))
        form.new_control('text', 'form.buyable_types', {'value': value})

def getAddToCartControlOrLink(browser):
    """Returns the 'Add to Cart' button as on Plone 2.5 it is a link
    but on Plone 3+ it is a control.
    """
    try:
        browser.getControl('Add to Cart')
        return browser.getControl('Add to Cart')
    except LookupError:
        return browser.getLink('Add to Cart')