# -*- coding: utf-8 -*-

from zope import schema
from zope.interface import Interface

from collective.googlenews import _


class IGoogleNewsLayer(Interface):
    """Browser layer for this addon"""


class GoogleNewsSettings(Interface):
    """Settings site wide of this addon"""

    # XXX: default value is declared at profiles/default/registry.xml
    portal_types = schema.List(
        title=_(u"Portal types"),
        description=_(u"Select portal types you want to apply digit id."),
        value_type=schema.Choice(vocabulary=u'plone.app.vocabularies.UserFriendlyTypes'),
        )
