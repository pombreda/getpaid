from Products.CMFCore.utils import getToolByName
from getpaid.core.options import PersistentOptions
from getpaid.core.interfaces import IOrderManager, IShoppingCartUtility
from getpaid.ogone.interfaces import IOgoneStandardProcessor, IOgoneStandardOptions
from zope.i18n.interfaces import IUserPreferredLanguages
from zope.interface import implements
from zope.component import getUtility
from getpaid.core.interfaces import keys
import interfaces
import urllib
import sha

OgoneStandardOptions = PersistentOptions.wire("OgoneStandardOptions",
                                              "getpaid.ogone",
                                              interfaces.IOgoneStandardOptions)


class OgoneStandardProcessor(object):
    """
    Ogone Standard Processor
    """
    implements(IOgoneStandardProcessor)

    options_interface = IOgoneStandardOptions

    def __init__(self, context):
        self.context = context

    def cart_post_button(self, cart):
        options = IOgoneStandardOptions(self.context)

    def getLanguage(self):
        """
        Ogone requires en_EN or en_US language id
        We are parsing the request to get the right
        """
        languages = IUserPreferredLanguages(self.context.REQUEST)
        langs = languages.getPreferredLanguages()
        if langs:
            language = langs[0]
        else:
            plone_props = getToolByName(self.context, 'portal_properties')
            language = plone_props.site_properties.default_language
        language = language.split('-')
        if len(language) == 1:
            language.append(language[0])
        language = language[:2]
        return "_".join(language)

    def createSHASignature(self, args):
        """
        Create the basic SHA signature
        See the Ogone Advanced e-commerce documentation SHA-IN for more informations
        """
        options = IOgoneStandardOptions(self.context)
        shaPassword = options.shain
        shaObject = sha.new()
        keys = args.keys()
        for key in ['RL']: # Whitelist would be cleaner but MUUCH longer
            keys.remove(key)
        keys.sort()
        for key in keys:
            shaObject.update("%s=%s%s" % (key, args[key], shaPassword))
        hexString = shaObject.hexdigest()
        return hexString.upper()

    def getColors(self):
        props = self.context.base_properties
        layoutDict = {}
        layoutDict['BGCOLOR'] = props.getProperty('backgroundColor')
        layoutDict['TXTCOLOR'] = props.getProperty('fontColor')
        return layoutDict

    def authorize(self, order, payment_information):
        """
        authorize an order, using payment information.
        """
        price = order.getTotalPrice()
        ogone_price = int(price * 100)
        orderId = order.order_id
        options = IOgoneStandardOptions(self.context)
        server_url = options.server_url
        urlArgs = dict(PSPID=options.pspid,
                       ORDERID=orderId,
                       RL='ncol-2.0',
                       CURRENCY=options.currency,
                       AMOUNT=ogone_price)
        if options.use_portal_css:
            urlArgs.update(self.getColors())
        urlArgs['LANGUAGE'] = self.getLanguage()
        if options.cancel_url:
            urlArgs['CANCELURL'] = options.cancel_url
        if options.accept_url:
            urlArgs['ACCEPTURL'] = options.accept_url
        if options.decline_url:
            urlArgs['DECLINEURL'] = options.decline_url
        if options.error_url:
            urlArgs['EXCEPTIONURL'] = options.error_url
        if order.billing_address.bill_name:
            urlArgs['CN'] = order.billing_address.bill_name[:35]
        if order.contact_information.email:
            urlArgs['EMAIL'] = order.contact_information.email[:50]
        if order.billing_address.bill_first_line:
            urlArgs['owneraddress'] = order.billing_address.bill_first_line[:35]
        if order.billing_address.bill_postal_code:
            urlArgs['ownerZIP'] = order.billing_address.bill_postal_code[:10]
        if order.billing_address.bill_city:
            urlArgs['ownertown']= order.billing_address.bill_city[:40]
        if order.billing_address.bill_country:
            urlArgs['ownercty'] = order.billing_address.bill_country[:2]
        if order.contact_information.phone_number:
            urlArgs['ownertelno'] = order.contact_information.phone_number[:30]
        urlArgs['SHASIGN'] = self.createSHASignature(urlArgs)
        arguments = urllib.urlencode(urlArgs)
        url = "%s?%s" % (server_url, arguments)
        order_manager = getUtility(IOrderManager)
        order_manager.store(order)
        order.finance_workflow.fireTransition("authorize")
        getUtility(IShoppingCartUtility).destroy(self.context)
        self.context.REQUEST.RESPONSE.redirect(url)
        return keys.results_async

    def capture(self, order, amount):
        """
        capture amount from order.
        """
        return keys.results_async

    def refund(self, order, amount):
        """
        reset
        """
