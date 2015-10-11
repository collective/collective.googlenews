# -*- coding: utf-8 -*-

# import unittest2 as unittest
import unittest

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from plone.browserlayer.utils import registered_layers

from collective.googlenews.config import PROJECTNAME
from collective.googlenews.testing import INTEGRATION_TESTING


class InstallTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_installed(self):
        qi = self.portal['portal_quickinstaller']
        self.assertTrue(qi.isProductInstalled(PROJECTNAME),
                        'package not installed')

    def test_browserlayer_installed(self):
        layers = [l.getName() for l in registered_layers()]
        self.assertTrue('IGoogleNewsLayer' in layers,
                        'browser layer not installed')


class UninstallTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.qi.uninstallProducts(products=[PROJECTNAME])

    def test_uninstalled(self):
        self.assertFalse(self.qi.isProductInstalled(PROJECTNAME),
                         'package not uninstalled')

    def test_browserlayer_removed(self):
        layers = [l.getName() for l in registered_layers()]
        self.assertTrue('IGoogleNewsLayer' not in layers,
                        'browser layer not removed')


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
