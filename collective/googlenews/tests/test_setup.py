# -*- coding: utf-8 -*-
from collective.googlenews.config import PROJECTNAME
from collective.googlenews.interfaces import IGoogleNewsLayer
from collective.googlenews.testing import INTEGRATION_TESTING
from collective.googlenews.utils import get_workflows_with_publish_transition
from plone import api
from plone.browserlayer.utils import registered_layers

import unittest


class InstallTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_installed(self):
        qi = self.portal['portal_quickinstaller']
        self.assertTrue(qi.isProductInstalled(PROJECTNAME))

    def test_browserlayer_installed(self):
        self.assertIn(IGoogleNewsLayer, registered_layers())

    def test_workflow_guards_installed(self):
        from collective.googlenews.config import GUARD_EXPRESSION
        for wf in get_workflows_with_publish_transition():
            guard = wf.transitions['publish'].guard
            self.assertEqual(guard.getExprText(), GUARD_EXPRESSION)


class UninstallTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']
        with api.env.adopt_roles(['Manager']):
            self.qi.uninstallProducts(products=[PROJECTNAME])

    def test_uninstalled(self):
        self.assertFalse(self.qi.isProductInstalled(PROJECTNAME))

    def test_browserlayer_removed(self):
        self.assertNotIn(IGoogleNewsLayer, registered_layers())

    def test_workflow_guards_removed(self):
        for wf in get_workflows_with_publish_transition():
            guard = wf.transitions['publish'].guard
            self.assertEqual(guard.getExprText(), '')
