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

    def test_generateNewId(self):
        self.context.REQUEST = self.requestNoLayer
        id = self.context.generateNewId()
        self.failUnless(id=='a-title')
        self.context.REQUEST = self.request
        id = self.context.generateNewId()
        self.failUnless(id.startswith('a-title-'))
        self.failUnless(id.endswith('.html'))
        digit = id[len('a-title-'):-5]
        self.failUnless(digit.isdigit())
        self.failUnless(len(digit)>2)
        self.failUnless(len(digit)<5)

    def test_nameFromTitle(self):
        from collective.googlenews import digitid
        adapter = digitid.NameFromTitle(self.context)
        id = adapter.title
        self.failUnless(id.startswith('a title-'))
        self.failUnless(id.endswith('.html'))
        digit = id[len('a title-'):-5]
        self.failUnless(digit.isdigit())
        self.failUnless(len(digit)>2)
        self.failUnless(len(digit)<5)
