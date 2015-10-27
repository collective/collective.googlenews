# -*- coding: utf-8 -*-
from collective.googlenews.config import PROJECTNAME
from collective.googlenews.logger import logger


def add_editor_picks_tab(setup_tool):
    """Add support for Google News Editors' Picks feeds."""
    profile = 'profile-{0}:default'.format(PROJECTNAME)
    setup_tool.runImportStepFromProfile(profile, 'plone.app.registry')
    logger.info("Google News Editors' Picks feeds support successfully added")
