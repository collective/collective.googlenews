# -*- coding: utf-8 -*-
import unittest

from zope import interface

from plone.app import testing

from collective.googlenews.testing import FUNCTIONAL_TESTING
from collective.googlenews.testing import INTEGRATION_TESTING
from collective.googlenews.tests import utils


class UnitTestCase(unittest.TestCase):

    def setUp(self):
        from ZPublisher.tests.testPublish import Request
        from zope.annotation.interfaces import IAttributeAnnotatable
        from collective.googlenews.interfaces import IGoogleNewsLayer
        super(UnitTestCase, self).setUp()
        self.context = utils.FakeContext()
        self.request = Request()
        interface.alsoProvides(self.request,
                               (IAttributeAnnotatable, IGoogleNewsLayer))
        self.requestNoLayer = Request()
        interface.alsoProvides(self.request, (IAttributeAnnotatable,))


class TestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        from zope.annotation.interfaces import IAttributeAnnotatable
        from collective.googlenews.interfaces import IGoogleNewsLayer
        interface.alsoProvides(self.layer['request'],
                               (IAttributeAnnotatable, IGoogleNewsLayer))
        super(TestCase, self).setUp()
        self.portal = self.layer['portal']
        testing.setRoles(self.portal, testing.TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        testing.setRoles(self.portal, testing.TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']


class FunctionalTestCase(unittest.TestCase):

    layer = FUNCTIONAL_TESTING

    def setUp(self):
        from zope.annotation.interfaces import IAttributeAnnotatable
        from collective.googlenews.interfaces import IGoogleNewsLayer
        interface.alsoProvides(self.layer['request'],
                               (IAttributeAnnotatable, IGoogleNewsLayer))
        self.portal = self.layer['portal']
        testing.setRoles(self.portal, testing.TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        testing.setRoles(self.portal, testing.TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']


def build_test_suite(test_classes):
    suite = unittest.TestSuite()
    for klass in test_classes:
        suite.addTest(unittest.makeSuite(klass))
    return suite
