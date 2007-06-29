"""Doc test runner
"""

__docformat__ = "reStructuredText"

import doctest
import unittest
from zope.testing.doctestunit import DocFileSuite
from zope.app.testing import placelesssetup, ztapi
from zope.app.annotation import interfaces as annotation_interfaces
from zope.app.annotation import attribute

from hurry.workflow import interfaces
from getpaid.core.interfaces import IOrder
from getpaid.core import order_workflow as oworkflow
def setUp(test):
    return
    
def tearDown(test):
    return
    
def workflowSetUp(doctest):
    placelesssetup.setUp()


    ztapi.provideAdapter( IOrder,
                          interfaces.IWorkflowState,
                          oworkflow.FinanceState,
                         'getpaid.finance.state')

    ztapi.provideAdapter( IOrder,
                       interfaces.IWorkflowState,
                       oworkflow.FulfillmentState,
                      'getpaid.fulfillment.state')

    ztapi.provideAdapter( IOrder,
                     interfaces.IWorkflowInfo,
                     oworkflow.FinanceInfo,
                    'getpaid.finance.info')

    ztapi.provideAdapter( IOrder,
                     interfaces.IWorkflowInfo,
                     oworkflow.FulfillmentInfo,
                    'getpaid.fulfillment.info')
                    
    ztapi.provideAdapter(annotation_interfaces.IAttributeAnnotatable,
                         annotation_interfaces.IAnnotations,
                         attribute.AttributeAnnotations)

    ztapi.provideUtility(interfaces.IWorkflow,
                         oworkflow.FulfillmentWorkflow(),
                        'getpaid.fulfillment.workflow')
                        
    ztapi.provideUtility(interfaces.IWorkflow,
                        oworkflow.FinanceWorkflow(),
                        'getpaid.finance.workflow')                        
   
    ztapi.provideUtility(interfaces.IWorkflowVersions,
                         oworkflow.OrderVersions())

def test_suite():
    return unittest.TestSuite((
        DocFileSuite('order_api.txt',
                     setUp=workflowSetUp,
                     tearDown=tearDown,
                     optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
                     ),
        ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
