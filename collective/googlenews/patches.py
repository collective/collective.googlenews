# -*- coding: utf-8 -*-
from collective.googlenews.interfaces import GoogleNewsSettings
from collective.googlenews.logger import logger
from plone import api
from plone.formwidget.namedfile.converter import b64decode_file


def logo(self):
    """Return a Google News compliant logo if available."""
    logo = api.portal.get_registry_record(
        GoogleNewsSettings.__identifier__ + '.logo')

    if logo is None:
        return self._logo  # no Google News compliant logo, return portal logo

    filename, data = b64decode_file(logo)
    return '{0}/@@googlenews-logo/{1}'.format(
        api.portal.get().absolute_url(), filename)

patched_logo = lambda: property(logo)  # noqa: E731


def apply_patched_logo(scope, original, replacement):
    setattr(scope, '_{0}'.format(original), getattr(scope, original, None))
    setattr(scope, original, replacement())
    logger.info(
        'Patched FolderFeed to return a Google News compliant logo, if available')
