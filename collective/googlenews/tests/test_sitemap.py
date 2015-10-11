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

    def test_get_genres(self):
        # return an empty list
        brain = utils.FakeBrain()
        genres = self.view.get_genres(brain)
        self.assertIsInstance(genres, list)
        self.assertEqual(len(genres), 0)

    def test_get_keywords(self):
        brain = utils.FakeBrain()
        self.view.settings.keywords_mapping = ['economie|economy']
        brain.Subject.append('economie')
        brain.Subject.append('non traduit')
        keywords = self.view.get_keywords(brain)
        self.assertTrue(len(keywords), 1)
        self.assertIn('economy', keywords)


class TestIntegration(base.TestCase):

    def test_news(self):
        pass
