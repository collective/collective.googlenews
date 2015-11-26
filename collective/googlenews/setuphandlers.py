# -*- coding: utf-8 -*-
from collective.googlenews.logger import logger
from plone import api


class Empty:
    pass


def add_catalog_indexes(context):
    """Add indexes to the portal_catalog. For more information, see
    http://maurits.vanrees.org/weblog/archive/2009/12/catalog.
    """

    def extras(title):
        # see http://old.zope.org/Members/dedalu/ZCTextIndex_python
        extras = Empty()
        extras.doc_attr = title
        extras.index_type = 'Okapi BM25 Rank'
        extras.lexicon_id = 'plone_lexicon'
        return extras

    setup_tool = api.portal.get_tool('portal_setup')
    profile = 'profile-collective.googlenews:default'
    setup_tool.runImportStepFromProfile(profile, 'catalog')

    catalog = api.portal.get_tool('portal_catalog')
    indexes = catalog.indexes()

    wanted = (
        ('standout_journalism', 'BooleanIndex'),
        ('news_keywords', 'KeywordIndex'),
    )

    indexables = []
    for name, meta_type in wanted:
        if name not in indexes:
            if meta_type == 'ZCTextIndex':
                catalog.addIndex(name, meta_type, extras(name))
            else:
                catalog.addIndex(name, meta_type)
            indexables.append(name)
            logger.info('Added {0} for field {1}.'.format(meta_type, name))

    if len(indexables) > 0:
        logger.info('Indexing new indexes {0}.'.format(', '.join(indexables)))
        catalog.manage_reindexIndex(ids=indexables)


def import_various(context):
    """Import step for configuration not handled in XML files."""

    # only run step if a flag file is present
    if context.readDataFile('collective.googlenews.marker.txt') is None:
        return

    add_catalog_indexes(context)
