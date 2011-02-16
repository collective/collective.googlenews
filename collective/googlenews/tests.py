import unittest2 as unittest
from collective.googlenews.testing import INTEGRATION_TESTING

class IntegrationTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def test_setup(self):

        portal = self.layer['portal']

        self.assertEqual(u"2", u"Some title")
