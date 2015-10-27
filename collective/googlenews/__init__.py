# -*- coding: utf-8 -*-
from collective.googlenews.config import PROJECTNAME
from collective.googlenews.logger import logger
from zope.i18nmessageid import MessageFactory

_ = MessageFactory(PROJECTNAME)


from collective.googlenews.interfaces import IGoogleNewsEditorsPicksSettings
from plone import api
from plone.formwidget.namedfile.converter import b64decode_file
from Products.CMFPlone.browser.syndication.adapters import FolderFeed


@property
def logo(self):
    """Return Google News logo url if available, else return portal logo."""
    logo = api.portal.get_registry_record(
        IGoogleNewsEditorsPicksSettings.__identifier__ + '.logo')
    if logo is None:
        # return portal logo
        return self._logo
    # return Google News logo
    filename, data = b64decode_file(logo)
    return '{0}/@@googlenews-editorspicks/{1}'.format(
        api.portal.get().absolute_url(),
        filename
    )

setattr(FolderFeed, '_logo', FolderFeed.logo)
setattr(FolderFeed, 'logo', logo)
logger.info("Patched FolderFeed to use Google News Editors' Picks logo")
