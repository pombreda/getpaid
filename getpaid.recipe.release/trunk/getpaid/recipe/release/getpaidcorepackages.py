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

GETPAID_CORE_PACKAGES = [
    PyModule('ore.viewlet', CHEESE_SOURCE + 'o/ore.viewlet/ore.viewlet-0.2.tar.gz', version="0.2"),
    PyModule('getpaid.paymentech', CHEESE_SOURCE + 'g/getpaid.paymentech/getpaid.paymentech-0.2.tar.gz', version="0.2"),
    PyModule('getpaid.discount', CHEESE_SOURCE + 'g/getpaid.discount/getpaid.discount-0.4.tar.gz', version="0.4"),
]
