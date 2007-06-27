"""Integration tests for donations.
"""
from base import PloneGetPaidTestCase

class TestCreateDonation(PloneGetPaidTestCase):

    def testDonationProcess(self):
        from Products.Five.utilities.marker import mark
        from Products.PloneGetPaid.interfaces import IDonatableMarker
        from getpaid.core.interfaces import IDonationContent
        from zope.publisher.browser import TestRequest

        self.setRoles(('Manager',))
        id = self.portal.invokeFactory('Document', 'page-to-donate')
        donation = self.portal.restrictedTraverse('page-to-donate')
        
        mark( donation, IDonatableMarker)
        
        #XXX needs lots of tests - held up debugging the IDonationContent adapter:
        
        #request = TestRequest()
        #d = IDonationContent(donation, request)
        #import pdb; pdb.set_trace()
        #print d.values()
        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestCreateDonation))
    return suite
