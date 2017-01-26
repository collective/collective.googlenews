# -*- coding: utf-8 -*-
from collective.googlenews.testing import _setup_content
from collective.googlenews.testing import INTEGRATION_TESTING
from collective.googlenews.utils import get_current_standout_journalism
from plone import api
from plone.api.exc import InvalidParameterError
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


class BehaviorsTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.dummy1 = api.content.create(self.portal, 'Dexterity Item', 'd1')

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

    def test_standout_journalism_validation(self):
        # create and publish 7 items in the past
        _setup_content(7, in_the_past=True)
        results = get_current_standout_journalism()
        self.assertEqual(len(results), 0)

        # create and publish 7 items
        _setup_content(7)
        results = get_current_standout_journalism()
        self.assertEqual(len(results), 7)

        # we can publish a new item as long as it's not marked as standout
        obj = api.content.create(self.portal, 'Dexterity Item', 'foo')
        api.content.transition(obj=obj, transition='publish')

        obj = api.content.create(
            self.portal, 'Dexterity Item', 'bar', standout_journalism=True)
        with self.assertRaises(InvalidParameterError):
            api.content.transition(obj=obj, transition='publish')
