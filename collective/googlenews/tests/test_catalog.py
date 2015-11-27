# -*- coding: utf-8 -*-
from collective.googlenews.testing import INTEGRATION_TESTING
from plone import api

import unittest


class CatalogTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.catalog = self.portal['portal_catalog']

        with api.env.adopt_roles(['Manager']):
            self.folder = api.content.create(self.portal, 'Folder', 'folder')

        self.dummy1 = api.content.create(self.folder, 'Dexterity Item', 'd1')

    def test_standout_journalism_indexed(self):
        self.dummy1.standout_journalism = True
        self.dummy1.reindexObject()
        results = self.catalog(standout_journalism=True)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].getURL(), self.dummy1.absolute_url())

    def test_news_keywords_indexed(self):
        self.dummy1.news_keywords = [
            u'World Cup', u'Brazil 2014', u'Spain vs Netherlands']
        self.dummy1.reindexObject()
        unique_news_keywords = self.catalog.uniqueValuesFor('news_keywords')
        results = self.catalog(news_keywords='World Cup')
        self.assertEqual(len(unique_news_keywords), 3)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].getURL(), self.dummy1.absolute_url())

    def test_catalog_not_lost_on_package_reinstall(self):
        from collective.googlenews.config import PROJECTNAME
        self.dummy1.standout_journalism = True
        self.dummy1.reindexObject()
        qi = self.portal['portal_quickinstaller']
        qi.reinstallProducts(products=[PROJECTNAME])
        results = self.catalog(standout_journalism=True)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].getURL(), self.dummy1.absolute_url())
