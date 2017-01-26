# -*- coding: utf-8 -*-
from collective.googlenews.config import GUARD_EXPRESSION
from collective.googlenews.logger import logger
from collective.googlenews.utils import get_workflows_with_publish_transition
from plone import api
from Products.CMFCore.Expression import Expression
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer


@implementer(INonInstallable)
class HiddenProfiles(object):  # pragma: no cover

    def getNonInstallableProfiles(self):
        """Do not show on Plone's list of installable profiles."""
        return [
            u'collective.googlenews:uninstall',
        ]


class Empty:
    pass


def add_catalog_indexes(context=None):
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


def add_guard_expressions(context=None):
    """Add guard expression to all workflows with "publish" transition."""
    for wf in get_workflows_with_publish_transition():
        guard = wf.transitions['publish'].guard
        if guard.getExprText() == '':
            guard.expr = Expression(GUARD_EXPRESSION)
            logger.info('Guard expression added to {0} workflow'.format(wf.id))
        else:
            msg = 'Guard expression not added to {0} workflow (current value is "{1}")'
            logger.warn(msg.format(wf.id, guard.getExprText()))


def remove_guard_expressions():
    """Remove guard expression from all workflows with "publish" transition."""
    for wf in get_workflows_with_publish_transition():
        guard = wf.transitions['publish'].guard
        if guard.getExprText() == GUARD_EXPRESSION:
            guard.expr = None
            logger.info('Guard expression removed from {0} workflow'.format(wf.id))


def install_post_handler(context):
    """Handler for install steps not handled in XML files."""
    add_catalog_indexes()
    add_guard_expressions()


def uninstall_post_handler(context):
    """Handler for uninstall steps not handled in XML files."""
    remove_guard_expressions()
