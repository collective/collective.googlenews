# -*- coding: utf-8 -*-
from collective.googlenews import digitid
from collective.googlenews.tests import base, utils


class Test(base.UnitTestCase):

    def test_randomid(self):
        id = digitid.randomid()
        # check common rule
        self.failUnless(id.startswith('-'))
        # check on with 1000 ids
        digits = [digitid.randomid()[1:] for i in range(1000)]
        for digit in digits:
            self.assertTrue(digit.isdigit())
            self.assertTrue(100 <= int(digit) <= 9999)

    def test_generateNewId(self):
        self.context.REQUEST = self.requestNoLayer
        id = self.context.generateNewId()
        self.failUnless(id == 'a-title')
        self.context.REQUEST = self.request
        id = self.context.generateNewId()
        self.failUnless(id.startswith('a-title-'))
        digit = id[len('a-title-'):]
        self.failUnless(digit.isdigit())

    def test_dexterity_generateNewId(self):
        self.context = utils.FakeDexterityContext()
        self.context.REQUEST = self.requestNoLayer
        id = self.context.generateNewId(None, self.context)
        self.failUnless(id == 'dex-title')
        self.context.REQUEST = self.request
        id = self.context.generateNewId(None, self.context)
        self.failUnless(id.startswith('dex-title-'))
        digit = id[len('dex-title-'):]
        self.failUnless(digit.isdigit())

    def test_nameFromTitle(self):
        adapter = digitid.NameFromTitle(self.context)
        id = adapter.title
        self.failUnless(id.startswith('a title-'))
        digit = id[len('a title-'):]
        self.failUnless(digit.isdigit())
