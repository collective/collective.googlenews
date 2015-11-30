# -*- coding: utf-8 -*-
from collective.googlenews.testing import INTEGRATION_TESTING
from DateTime import DateTime
from plone import api

import unittest


class Test(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        request = self.layer['request']
        self.view = api.content.get_view(
            name='googlenews-sitemap.xml', context=self.portal, request=request)

        with api.env.adopt_roles(['Manager']):
            self.n1 = api.content.create(
                type='News Item',
                container=self.portal,
                id='n1',
                title='News Item 1',
            )
            self.n1.setEffectiveDate(DateTime())
            self.n1.reindexObject()

            self.n2 = api.content.create(
                type='News Item',
                container=self.portal,
                id='n2',
                title='News Item 2',
            )
            self.n2.setEffectiveDate(DateTime())
            self.n2.reindexObject()

            self.n3 = api.content.create(
                type='News Item',
                container=self.portal,
                id='n3',
                title='News Item 3',
            )
            self.n3.setEffectiveDate(DateTime() - 3)
            self.n3.reindexObject()

    def test_news(self):
        expected = [
            dict(
                loc='http://nohost/plone/n2',
                publication_date=self.n2.effective_date.ISO(),
                title='News Item 2',
                keywords=None,
            ),
            dict(
                loc='http://nohost/plone/n1',
                publication_date=self.n1.effective_date.ISO(),
                title='News Item 1',
                keywords=None,
            ),
        ]
        self.assertEqual(self.view.news(), expected)

    def test_portaltitle(self):
        self.assertEqual(self.view.portal_title(), u'Plone site')

    def test_portallanguage(self):
        self.assertEqual(self.view.portal_language(), 'en')

    def test_view(self):
        render = self.view()
        self.assertIn(u'<news:title>News Item 1</news:title>', render)
        self.assertIn(u'<news:title>News Item 2</news:title>', render)
        self.assertNotIn(u'<news:title>News Item 3</news:title>', render)
