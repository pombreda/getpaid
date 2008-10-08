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
GETPAID_SOURCE = 'http://getpaid.googlecode.com/files/'

# XXX Missing
# gchecky is installed by default
# ore.viewlet need to update browser.py
# getpaid.paypal => personal info in it
# zc.table svn://svn.zope.org/repos/main/zc.table/tags/zc.table-0.5.1 (double check)
# zc.resourcelibrary svn://svn.zope.org/repos/main/zc.resourcelibrary/tags/zc.resourcelibrary-0.5 (double check)

GETPAID_BASE_PACKAGES = [
    PyModule('ore.viewlet', CHEESE_SOURCE + 'o/ore.viewlet/ore.viewlet-0.2.tar.gz', version="0.2"),
    PyModule('getpaid.core', CHEESE_SOURCE + 'g/getpaid.core/getpaid.core-0.7.tar.gz', version="0.7"),
    PyModule('Products.PloneGetPaid', CHEESE_SOURCE + 'P/Products.PloneGetPaid/Products.PloneGetPaid-0.7.tar.gz', version="0.7"),
    PyModule('getpaid.wizard', CHEESE_SOURCE + 'g/getpaid.wizard/getpaid.wizard-0.3.tar.gz', version="0.3"),
    PyModule('getpaid.nullpayment', CHEESE_SOURCE + 'g/getpaid.nullpayment/getpaid.nullpayment-0.3.tar.gz', version="0.3"),
]

GETPAID_DEPENDENCIES = [
    PyModule('five.intid', CHEESE_SOURCE + 'f/five.intid/five.intid-0.2.0.tar.gz', version="0.2.0"),
    #PyModule('hurry.workflow', GETPAID_SOURCE + 'hurry.workflow-0.9.1-getpaid.tar.gz', version="0.9.1-getpaid"),
    #PyModule('yoma.batching', 'http://getpaid.googlecode.com/files/yoma.batching-0.2.1.tar.gz', version="0.2.1"),
    PyModule('zc.authorizedotnet', CHEESE_SOURCE + 'z/zc.authorizedotnet/zc.authorizedotnet-1.3.tar.gz', version="1.3"),
    PyModule('zc.resourcelibrary', CHEESE_SOURCE + 'z/zc.resourcelibrary/zc.resourcelibrary-1.0.1.tar.gz', version="1.0.1"),
    PyModule('zc.table', CHEESE_SOURCE + 'z/zc.table/zc.table-0.7.0.tar.gz', version="0.7.0"),
]

GETPAID_PAYMENT_PROCESSORS = [
    PyModule('getpaid.authorizedotnet', CHEESE_SOURCE + 'g/getpaid.authorizedotnet/getpaid.authorizedotnet-0.3.tar.gz', version="0.3"),
    PyModule('getpaid.googlecheckout', CHEESE_SOURCE + 'g/getpaid.googlecheckout/getpaid.googlecheckout-0.2.tar.gz', version="0.2"),
    PyModule('getpaid.paymentech', CHEESE_SOURCE + 'g/getpaid.paymentech/getpaid.paymentech-0.3.tar.gz', version="0.3"),
    PyModule('getpaid.paypal', CHEESE_SOURCE + 'g/getpaid.paypal/getpaid.paypal-0.4.tar.gz', version="0.4"),
    PyModule('getpaid.pxpay', CHEESE_SOURCE + 'g/getpaid.pxpay/getpaid.pxpay-0.2.tar.gz', version="0.2"),
]

GETPAID_SHIPPING = [
    PyModule('getpaid.flatrateshipping', CHEESE_SOURCE + 'g/getpaid.flatrateshipping/getpaid.flatrateshipping-0.2.tar.gz', version="0.2"),
    PyModule('getpaid.ups', CHEESE_SOURCE + 'g/getpaid.ups/getpaid.ups-0.3.tar.gz', version="0.3"),
]

GETPAID_EXTRA_PACKAGES = [
    PyModule('getpaid.discount', CHEESE_SOURCE + 'g/getpaid.discount/getpaid.discount-0.5.tar.gz', version="0.5"),
]

GETPAID_PACKAGES = GETPAID_BASE_PACKAGES + GETPAID_DEPENDENCIES + \
                        GETPAID_SHIPPING + GETPAID_PAYMENT_PROCESSORS + \
                        GETPAID_EXTRA_PACKAGES
