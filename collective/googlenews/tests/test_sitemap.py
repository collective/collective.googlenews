# -*- coding: utf-8 -*-

from collective.googlenews.tests import base
from collective.googlenews.tests import utils


class Test(base.UnitTestCase):

    def setUp(self):
        super(Test, self).setUp()
        from collective.googlenews import sitemap
        self.view = sitemap.GoogleNewsSiteMap(self.context, self.request)
        self.view.portal_state = utils.FakePlonePortalState()
        self.view.settings = utils.FakeSettings()
        self.view.update()

    def test_brain2news(self):
        pass

    def test_news(self):
        self.view.news()

    def test_get_query_constraints(self):
        query = self.view.get_query_constraints()
        self.assertIn('sort_limit', query)
        self.assertEqual(query['sort_limit'], 1000)
        self.assertIn('sort_on', query)
        self.assertEqual(query['sort_on'], 'effective')
        self.assertIn('sort_order', query)
        self.assertEqual(query['sort_order'], 'reverse')
        self.assertIn('effective', query)
        effective = query['effective']['range']
        self.assertIn(effective, 'min:max')
