import unittest2 as unittest
from collective.googlenews.testing import INTEGRATION_TESTING
from plone.registry.interfaces import IRegistry
from plone.browserlayer.interfaces import ILocalBrowserLayerType
from zope import component

from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login

class IntegrationTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def test_setup(self):
        portal = self.layer['portal']

        #check browsler layer is setup
        layers = component.getAllUtilitiesRegisteredFor(ILocalBrowserLayerType)
        layer = [layer for layer in layers if layer.__name__=="IGoogleNewsLayer"]
        self.failUnless(len(layer)==1)

        #check registry
        self.failUnless('portal_registry' in portal.objectIds())
        registry = component.getUtility(IRegistry)
        portal_types = registry['collective.googlenews.interfaces.GoogleNewsSettings.portal_types']
        self.failUnless(portal_types==['News Item'])
        #check controlpanel
        ctool = portal.portal_controlpanel
        actions = ctool.listActions() #not in the api
        action = [action for action in actions if action.category=='Products'][0]
        self.failUnless(action.id=='collective.googlenews.settings')

    def test_digitid(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        portal.invokeFactory('News Item', 'newsid', title=u"Page 1")
        news = portal.newsid
        newid = news.generateNewId()
        self.failUnless(len(newid)>len('newsid'))
        self.failUnless(newid[-5:]=='.html')
        self.failUnless(newid[5:-5].isdigit())

    def test_sitemap(self):
        portal = self.layer['portal']
