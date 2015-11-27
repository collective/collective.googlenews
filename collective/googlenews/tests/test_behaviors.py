# -*- coding: utf-8 -*-
from collective.googlenews.testing import INTEGRATION_TESTING
from plone import api

import unittest


class BehaviorsTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

        with api.env.adopt_roles(['Manager']):
            self.folder = api.content.create(self.portal, 'Folder', 'folder')

        self.dummy1 = api.content.create(self.folder, 'Dexterity Item', 'd1')

    def test_googlenews_behavior(self):
        from collective.googlenews.behaviors.interfaces import IGoogleNews
        self.assertTrue(IGoogleNews.providedBy(self.dummy1))

    def test_fields(self):
        self.assertFalse(self.dummy1.standout_journalism)
        self.assertIsNone(self.dummy1.news_keywords)

        self.dummy1.standout_journalism = True
        self.dummy1.news_keywords = (
            u'World Cup', u'Brazil 2014', u'Spain vs Netherlands')

        self.assertTrue(self.dummy1.standout_journalism)
        self.assertEqual(len(self.dummy1.news_keywords), 3)

    def test_validator(self):
        from collective.googlenews.utils import _valid_as_standout_journalism
        self.assertTrue(_valid_as_standout_journalism())

        for i in range(0, 7):
            api.content.create(
                self.folder, 'Dexterity Item', str(i), standout_journalism=True)

        self.assertFalse(_valid_as_standout_journalism())
