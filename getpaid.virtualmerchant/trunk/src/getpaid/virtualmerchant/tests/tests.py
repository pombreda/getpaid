# Copyright (c) 2007 ifPeople, Kapil Thangavelu, and Contributors
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

import unittest
from Testing import ZopeTestCase
from zope.testing import doctest
from Products.PloneGetPaid.tests.base import PloneGetPaidFunctionalTestCase
#from Products.PloneTestCase import PloneTestCase
from Products.PloneTestCase.layer import onsetup
from Products.Five import fiveconfigure
from Products.Five import zcml


OPTIONFLAGS = (doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE |
               doctest.REPORT_UDIFF)

ZopeTestCase.installProduct('CMFonFive')
ZopeTestCase.installProduct('PloneGetPaid')

@onsetup
def setup_product():
    """Set up the package and its dependencies.

    The @onsetup decorator causes the execution of this body to be
    deferred until the setup of the Plone site testing layer. We could
    have created our own layer, but this is the easiest way for Plone
    integration tests.
    """

    fiveconfigure.debug_mode = True
    import getpaid.virtualmerchant
    import Products.PloneGetPaid
    zcml.load_config('configure.zcml', getpaid.virtualmerchant)
    zcml.load_config('configure.zcml', Products.PloneGetPaid)
    fiveconfigure.debug_mode = False

#ptc.setupPloneSite()

class VirtualMerchantFunctionalTestCase(PloneGetPaidFunctionalTestCase):

    def afterSetUp(self):
        super(VirtualMerchantFunctionalTestCase, self).afterSetUp()
        self.portal.portal_quickinstaller.installProduct('PloneGetPaid')


def test_suite():
    return unittest.TestSuite([
        ZopeTestCase.ZopeDocFileSuite(
            'README.txt',
            package='getpaid.virtualmerchant',
            test_class=VirtualMerchantFunctionalTestCase,
            optionflags=OPTIONFLAGS,
            ),
        #ZopeTestCase.ZopeDocFileSuite(
        #    'virtualmerchant-browser.txt',
        #    package='getpaid.virtualmerchant',
        #    test_class=VirtualMerchantFunctionalTestCase,
        #    optionflags=OPTIONFLAGS,
        #    ),
        ])
