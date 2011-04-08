from collective.googlenews.tests import base

class Test(base.UnitTestCase):
    
    def setUp(self):
        super(Test, self).setUp()
#        from collective.gallery import core
#        self.view = core.BaseBrowserView(self.context, self.request)

    def testToto(self):
        self.assertEqual("a", "a title")

class TestIntegration(base.TestCase):
    
    def testProperties(self):
        from collective.googlenews import digitid
        self.failUnless(1 == 400)
