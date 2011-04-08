from collective.googlenews.tests import base

class Test(base.UnitTestCase):
    
    def setUp(self):
        super(Test, self).setUp()
#        from collective.gallery import core
#        self.view = core.BaseBrowserView(self.context, self.request)

    def test_randomid(self):
        from collective.googlenews import digitid
        id = digitid.randomid()
        #check common rule
        self.failUnless(id.startswith('-'))
        self.failUnless(id.endswith('.html'))
        #check on with 1000 ids
        digits = [digitid.randomid()[1:-5] for i in range(1000)]
        for digit in digits:
            self.failUnless(digit.isdigit())
            self.failUnless(len(digit)>2)
            self.failUnless(len(digit)<5)

class TestIntegration(base.TestCase):
    
    def testProperties(self):
        from collective.googlenews import digitid
        self.failUnless(1 == 400)
