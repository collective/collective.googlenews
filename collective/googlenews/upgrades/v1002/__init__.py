# -*- coding: utf-8 -*-
from collective.googlenews.config import PROJECTNAME
from collective.googlenews.logger import logger
from collective.googlenews.setuphandlers import add_catalog_indexes


def update_portal_catalog(setup_tool):
    """Add catalog indexes and metadata for Google News behavior fields."""
    profile = 'profile-{0}:default'.format(PROJECTNAME)
    setup_tool.runImportStepFromProfile(profile, 'catalog')
    add_catalog_indexes(setup_tool)
    logger.info('Portal catalog successfully updated')
