from collective.googlenews.tests import base

class TestIntegration(base.TestCase):
    
    def testProperties(self):
        self.failUnless(1 == 400)
