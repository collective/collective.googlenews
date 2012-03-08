# -*- coding: utf-8 -*-

import unittest2 as unittest

from zope.component import getMultiAdapter
from zope.component import getUtility

from plone.app.testing import TEST_USER_ID
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.registry import Registry
from plone.registry.interfaces import IRegistry

from Products.CMFCore.utils import getToolByName

from collective.googlenews.interfaces import GoogleNewsSettings
from collective.googlenews.testing import INTEGRATION_TESTING

BASE_RECORD_NAME = 'collective.googlenews.interfaces.GoogleNewsSettings.%s'


class RegistryTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.registry = Registry()
        self.registry.registerInterface(GoogleNewsSettings)

    def test_controlpanel_view(self):
        view = getMultiAdapter((self.portal, self.portal.REQUEST),
                               name='googlenews-controlpanel')
        view = view.__of__(self.portal)
        self.assertTrue(view())

    def test_controlpanel_view_protected(self):
        from AccessControl import Unauthorized
        logout()
        self.assertRaises(Unauthorized, self.portal.restrictedTraverse,
                          '@@googlenews-controlpanel')

    def test_entry_in_controlpanel(self):
        self.controlpanel = getToolByName(self.portal, 'portal_controlpanel')
        actions = [a.getAction(self)['id']
                   for a in self.controlpanel.listActions()]
        self.assertTrue('collective.googlenews.settings' in actions)

    def test_record_portal_types(self):
        record_portal_types = self.registry.records[
            BASE_RECORD_NAME % 'portal_types']
        self.assertTrue('portal_types' in GoogleNewsSettings)
        self.assertEquals(record_portal_types.value, ['News Item'])


class RegistryUninstallTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.registry = getUtility(IRegistry)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        qi = self.portal['portal_quickinstaller']
        qi.uninstallProducts(products=['collective.googlenews'])

    def test_records_removed(self):
        records = [
            BASE_RECORD_NAME % 'portal_types',
            ]
        for r in records:
            self.assertFalse(r in self.registry)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
