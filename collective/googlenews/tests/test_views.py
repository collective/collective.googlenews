# -*- coding: utf-8 -*-
from collective.googlenews.interfaces import GoogleNewsSettings
from collective.googlenews.interfaces import validate_logo
from collective.googlenews.testing import INTEGRATION_TESTING
from plone import api
from plone.formwidget.namedfile.converter import b64encode_file
from zope.component import getMultiAdapter
from zope.interface import Invalid

import unittest


def load_file(name, size=0):
    """Load file from testing directory"""
    path = '/tmp/{0}'.format(name)
    with open(path, 'rb') as f:
        data = f.read()
    return data


def encode_image(image):
    """Return image encoded in base64"""
    return b64encode_file(
        image,
        load_file(image)
    )


class AtomFeedViewTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

    def test_logo(self):
        view = getMultiAdapter((self.portal, self.request), name='atom.xml')
        feed = view.feed()
        self.assertEqual(feed.logo, 'http://nohost/plone/logo.png')

        api.portal.set_registry_record(
            GoogleNewsSettings.__identifier__ + '.logo',
            encode_image('logo_plone_ok.png')
        )
        self.assertEqual(
            feed.logo, 'http://nohost/plone/@@googlenews-logo/logo_plone_ok.png')


class ValidateLogoTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_validate_logo_constraint(self):
        invalid_images = (
            'logo_plone_not_transparent.png',
            'logo_plone_wrong_filetype.jpg',
            'logo_plone_wrong_size.png'
        )
        for image in invalid_images:
            data = encode_image(image)
            with self.assertRaises(Invalid):
                validate_logo(data)

        data = encode_image('logo_plone_ok.png')
        self.assertTrue(validate_logo(data))
