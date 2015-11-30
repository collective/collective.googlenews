# -*- coding: utf-8 -*-
from collective.googlenews.config import PROJECTNAME
from collective.googlenews.interfaces import GoogleNewsSettings
from collective.googlenews.testing import INTEGRATION_TESTING
from plone import api
from plone.app.testing import logout
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

import unittest


class ControlPanelTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.controlpanel = self.portal['portal_controlpanel']

    def test_controlpanel_view(self):
        view = api.content.get_view(
            name='googlenews-controlpanel',
            context=self.portal,
            request=self.layer['request'],
        )
        view = view.__of__(self.portal)
        self.assertTrue(view())

    def test_controlpanel_view_protected(self):
        from AccessControl import Unauthorized
        logout()
        with self.assertRaises(Unauthorized):
            self.portal.restrictedTraverse('googlenews-controlpanel')

    def test_controlpanel_installed(self):
        actions = [a.getAction(self)['id']
                   for a in self.controlpanel.listActions()]
        self.assertIn('collective.googlenews.settings', actions)

    def test_controlpanel_removed_on_uninstall(self):
        qi = self.portal['portal_quickinstaller']
        with api.env.adopt_roles(['Manager']):
            qi.uninstallProducts(products=[PROJECTNAME])
        actions = [a.getAction(self)['id']
                   for a in self.controlpanel.listActions()]
        self.assertNotIn('collective.googlenews.settings', actions)


class RegistryTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.registry = getUtility(IRegistry)
        self.settings = self.registry.forInterface(GoogleNewsSettings)

    def test_record_portal_types(self):
        self.assertTrue(hasattr(self.settings, 'portal_types'))
        self.assertListEqual(self.settings.portal_types, ['News Item'])

    def test_logo_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'logo'))
        self.assertIsNone(self.settings.logo)

    def test_records_removed_on_uninstall(self):
        qi = self.portal['portal_quickinstaller']
        with api.env.adopt_roles(['Manager']):
            qi.uninstallProducts(products=[PROJECTNAME])

        BASE_REGISTRY = 'collective.googlenews.interfaces.GoogleNewsSettings.'
        records = [
            BASE_REGISTRY + 'portal_types',
            BASE_REGISTRY + 'logo',
        ]

        for r in records:
            self.assertNotIn(r, self.registry)
