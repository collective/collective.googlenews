# -*- coding: utf-8 -*-

from zope import schema
from zope.interface import Interface

from collective.googlenews import _


class IGoogleNewsLayer(Interface):
    """Browser layer for this addon"""


class GoogleNewsSettings(Interface):
    """Settings site wide of this addon"""

    portal_types = schema.List(
        title=_(u"Portal types"),
        description=_(u"add portal types you want to apply digit id"),
        value_type=schema.ASCIILine(title=_(u"Portal type")),
        )
