# -*- coding: utf-8 -*-

import unittest2 as unittest

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from plone.browserlayer.utils import registered_layers

from collective.googlenews.testing import INTEGRATION_TESTING


class TestInstall(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']

    def test_installed(self):
        self.assertTrue(self.qi.isProductInstalled('collective.googlenews'),
                        'package not installed')

    def test_dependencies_installed(self):
        packages = ['plone.app.registry']
        for p in packages:
            self.assertTrue(self.qi.isProductInstalled(p),
                            '%s not installed' % p)

    def test_browserlayer_installed(self):
        layers = [l.getName() for l in registered_layers()]
        self.assertTrue('IGoogleNewsLayer' in layers,
                        'browser layer not installed')


class TestUninstall(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.qi.uninstallProducts(products=['collective.googlenews'])

    def test_uninstalled(self):
        self.assertFalse(self.qi.isProductInstalled('collective.googlenews'),
                         'package not uninstalled')

    def test_browserlayer_removed(self):
        layers = [l.getName() for l in registered_layers()]
        self.assertFalse('IGoogleNewsLayer' in layers,
                         'browser layer not removed')


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
