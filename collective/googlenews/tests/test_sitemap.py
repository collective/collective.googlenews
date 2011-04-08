from collective.googlenews.tests import base
from collective.googlenews.tests import utils

class Test(base.UnitTestCase):
    
    def setUp(self):
        super(Test, self).setUp()
        from collective.googlenews import sitemap
        self.view = sitemap.GoogleNewsSiteMap(self.context, self.request)
        self.view._state = utils.FakePlonePortalState()

    def test_brain2news(self):
        pass

    def test_news(self):
        self.view.news()

class TestIntegration(base.TestCase):
    
    def test_news(self):
        pass
