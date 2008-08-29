import os, subprocess

class Software:
    """ general software """
    type = 'Software'

    name = None
    download_url = None
    archive_rename = None
    productdir_rename = None
    filename = None
    parent = None
    version = None

    destination = 'downloads'

    def __init__(self, name, download_url, productdir=None, archive_rename=None, version=None):
        self.name = name
        self.download_url = download_url
        self.productdir_rename = productdir
        self.archive_rename = archive_rename
        self.version = version

class PyModule(Software):
    """ python module """

    type = 'PyModule'
    destination = 'lib/python'

    def post_extract(self, destination, me):
        cwd=os.getcwd()
        me=me.split('/')[0]
        os.chdir(os.path.join(destination, me))
        res=subprocess.call(["python2.4", "setup.py", "install_lib",
            "--install-dir=%s" % destination])
        if res!=0:
            raise RuntimeError, "Failed to setup package"

        os.chdir(destination)
        subprocess.call(["rm", "-rf", me])
        os.chdir(cwd)

CHEESE_SOURCE = 'http://pypi.python.org/packages/source/'

GETPAID_BASE_PACKAGES = [
    PyModule('ore.viewlet', CHEESE_SOURCE + 'o/ore.viewlet/ore.viewlet-0.2.tar.gz', version="0.2"),
    PyModule('getpaid.core', CHEESE_SOURCE + 'g/getpaid.core/getpaid.core-0.7.tar.gz', version="0.7"),
    PyModule('Products.PloneGetPaid', CHEESE_SOURCE + 'P/Products.PloneGetPaid/Products.PloneGetPaid-0.7.tar.gz', version="0.7"),
    PyModule('getpaid.wizard', CHEESE_SOURCE + 'g/getpaid.wizard/getpaid.wizard-0.3.tar.gz', version="0.3"),
    PyModule('getpaid.nullpayment', CHEESE_SOURCE + 'g/getpaid.nullpayment/getpaid.nullpayment-0.3.tar.gz', version="0.3"),
]

GETPAID_PAYMENT_PROCESSORS = [
    PyModule('getpaid.authorizedotnet', CHEESE_SOURCE + 'g/getpaid.authorizedotnet/getpaid.authorizedotnet-0.3.tar.gz', version="0.3"),
    PyModule('getpaid.paymentech', CHEESE_SOURCE + 'g/getpaid.paymentech/getpaid.paymentech-0.3.tar.gz', version="0.3"),
    PyModule('getpaid.googlecheckout', CHEESE_SOURCE + 'g/getpaid.googlecheckout/getpaid.googlecheckout-0.2.tar.gz', version="0.2"),
    #PyModule('getpaid.pxpay', CHEESE_SOURCE + 'g/getpaid.pxpay/getpaid.pxpay-0.2.tar.gz', version="0.2"),
]

GETPAID_SHIPPING = [
    PyModule('getpaid.flatrateshipping', CHEESE_SOURCE + 'g/getpaid.flatrateshipping/getpaid.flatrateshipping-0.2.tar.gz', version="0.2"),
    PyModule('getpaid.ups', CHEESE_SOURCE + 'g/getpaid.ups/getpaid.ups-0.3.tar.gz', version="0.3"),
]

GETPAID_EXTRA_PACKAGES = [
    PyModule('getpaid.discount', CHEESE_SOURCE + 'g/getpaid.discount/getpaid.discount-0.5.tar.gz', version="0.5"),
]

GETPAID_CORE_PACKAGES = GETPAID_BASE_PACKAGES + GETPAID_SHIPPING + GETPAID_PAYMENT_PROCESSORS + GETPAID_EXTRA_PACKAGES
