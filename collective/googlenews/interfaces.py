# -*- coding: utf-8 -*-

from zope import schema
from zope.interface import Interface

from collective.googlenews import _

TYPES_VOCAB = u"plone.app.vocabularies.ReallyUserFriendlyTypes"
keywords_msgid = _(u"Please read https://support.google.com/news/publisher/answer/116037").replace(" ", "")


class IGoogleNewsLayer(Interface):
    """Browser layer for this addon"""


class GoogleNewsSettings(Interface):
    """Settings site wide of this addon"""

    # XXX: default value is declared at profiles/default/registry.xml
    portal_types = schema.List(
        title=_(u"Portal types"),
        description=_(u"Select portal types you want to apply digit id."),
        value_type=schema.Choice(vocabulary=TYPES_VOCAB),
    )

    keywords_mapping = schema.List(
        title=_(u"Keywords Mapping"),
        description=_(keywords_msgid),
        value_type=schema.TextLine(title=_(u"keyword|googlekeyword"))
    )
