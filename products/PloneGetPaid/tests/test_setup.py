from base import PloneGetPaidTestCase

#from Products.membrane.interfaces import ICategoryMapper
#from Products.membrane.config import ACTIVE_STATUS_CATEGORY
#from Products.membrane.utils import generateCategorySetIdForType

#from Products.borg.config import LOCALROLES_PLUGIN_NAME, PLACEFUL_WORKFLOW_POLICY

class TestProductInstall(PloneGetPaidTestCase):

    # XXX MOVED THIS TO THE BASE 'PloneGetPaidTestCase' to simplify things
    #def afterSetUp(self):
    #    # XXX monkey patch -- see tests/base.py for more details
    #    super( TestProductInstall, self).afterSetUp()
    #    self.portal.portal_quickinstaller.installProduct('PloneGetPaid')

    def testTypesInstalled(self):
        self.types = ('Donation',)
        for t in self.types:
            self.failUnless(t in self.portal.portal_types.objectIds(),
                            '%s content type not installed' % t)
    
    #def testTypesRegisteredWithMembrane(self):
    #    for t in self.types:
    #        self.failUnless(t in self.portal.membrane_tool.listMembraneTypes(),
    #                        '%s content type not added to membrane' % t)
    #    
    #def testMembraneActiveWorkflowMappingForEmployee(self):
    #    states = { 'Department' : ['active',],
    #               'Employee'   : ['active',],
    #               'Project'    : ['private', 'published',],
    #               }
    #    categoryMap = ICategoryMapper(self.portal.membrane_tool)
    #    for t, s in states.items():
    #        categorySet = generateCategorySetIdForType(t)
    #        self.assertEquals(s, categoryMap.listCategoryValues(categorySet, ACTIVE_STATUS_CATEGORY))
    #    
    #def testPortalFactoryEnabled(self):
    #    for t in self.types:
    #        self.failUnless(t in self.portal.portal_factory.getFactoryTypes().keys(),
    #                        '%s content type not installed' % t)
    #
    #def testPASPluginInstalled(self):
    #    self.failUnless(LOCALROLES_PLUGIN_NAME, self.portal.acl_users.objectIds())
    #    
    #def testPASPluginActivated(self):
    #    self.fail('Test missing: Need to test PAS plugin activated')
    #    
    #def testWorkflowsInstalled(self):
    #    workflowIds = self.portal.portal_workflow.objectIds()
    #    self.failUnless('borg_department_workflow' in workflowIds)
    #    self.failUnless('borg_employee_workflow' in workflowIds)
    #    self.failUnless('borg_project_workflow' in workflowIds)
    #    
    #def testWorkflowsMapped(self):
    #    wf = self.portal.portal_workflow
    #    self.assertEquals(('borg_department_workflow',), wf.getChainForPortalType('Department'))
    #    self.assertEquals(('borg_employee_workflow',), wf.getChainForPortalType('Employee'))
    #    self.assertEquals(('borg_project_workflow',), wf.getChainForPortalType('Project'))
    #
    #def testLocalWorkflowPolicyInstalled(self):
    #    self.failUnless(PLACEFUL_WORKFLOW_POLICY in self.portal.portal_placeful_workflow.objectIds())
    #    policy = self.portal.portal_placeful_workflow.getWorkflowPolicyById(PLACEFUL_WORKFLOW_POLICY)
    #    self.assertEqual(('borg_project_default_workflow',), policy.getDefaultChain(None))
    #    self.assertEqual(('borg_project_default_workflow',), policy.getChainFor('Folder'))
    #    self.assertEqual(('borg_project_default_workflow',), policy.getChainFor('Large Plone Folder'))

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestProductInstall))
    return suite
