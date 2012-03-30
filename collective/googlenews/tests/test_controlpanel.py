# -*- coding: utf-8 -*-

import unittest2 as unittest

from zope.component import getMultiAdapter
from zope.component import getUtility

from plone.app.testing import TEST_USER_ID
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.registry.interfaces import IRegistry

from collective.googlenews.interfaces import GoogleNewsSettings
from collective.googlenews.testing import INTEGRATION_TESTING


class ControlPanelTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.controlpanel = self.portal['portal_controlpanel']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_controlpanel_view(self):
        view = getMultiAdapter((self.portal, self.portal.REQUEST),
                               name='googlenews-controlpanel')
        view = view.__of__(self.portal)
        self.assertTrue(view())

    def test_controlpanel_view_protected(self):
        from AccessControl import Unauthorized
        logout()
        self.assertRaises(Unauthorized, self.portal.restrictedTraverse,
                          'googlenews-controlpanel')

    def test_controlpanel_installed(self):
        actions = [a.getAction(self)['id']
                   for a in self.controlpanel.listActions()]
        self.assertTrue('collective.googlenews.settings' in actions)

    def test_controlpanel_removed_on_uninstall(self):
        qi = self.portal['portal_quickinstaller']
        qi.uninstallProducts(products=['collective.googlenews'])
        actions = [a.getAction(self)['id']
                   for a in self.controlpanel.listActions()]
        self.assertTrue('collective.googlenews.settings' not in actions)


class RegistryTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        registry = getUtility(IRegistry)
        self.settings = registry.forInterface(GoogleNewsSettings)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_record_portal_types(self):
        self.assertTrue(hasattr(self.settings, 'portal_types'))
        self.assertListEqual(self.settings.portal_types, ['News Item'])

    def test_records_removed(self):
        qi = self.portal['portal_quickinstaller']
        qi.uninstallProducts(products=['collective.googlenews'])
        self.assertFalse(hasattr(self.settings, 'portal_types'))


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
