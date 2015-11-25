# -*- coding: utf-8 -*-
from collective.googlenews import _
from collective.googlenews.utils import validate_logo
from plone.directives import form
from z3c.form import field
from z3c.form import group
from zope import schema
from zope.interface import Interface

EDITORS_PICKS_HELP = 'https://support.google.com/news/publisher/answer/1407682'
TYPES_VOCAB = u'plone.app.vocabularies.ReallyUserFriendlyTypes'
keywords_msgid = _(u'Please read https://support.google.com/news/publisher/answer/116037').replace(' ', '')


class IGoogleNewsLayer(Interface):

    """Browser layer for this addon"""


class GoogleNewsSettings(form.Schema):

    """Main settings of this addon"""

    # XXX: default value is declared at profiles/default/registry.xml
    portal_types = schema.List(
        title=_(u'Portal types'),
        description=_(u'Select portal types you want to apply digit id.'),
        value_type=schema.Choice(vocabulary=TYPES_VOCAB),
    )

    keywords_mapping = schema.List(
        title=_(u'Keywords Mapping'),
        description=_(keywords_msgid),
        value_type=schema.TextLine(title=_(u'keyword|googlekeyword'))
    )


class IGoogleNewsEditorsPicksSettings(form.Schema):

    """Editor picks settings of this addon"""

    logo = schema.ASCII(
        title=_(u"Logo image to be used on Editors' Picks feeds"),
        description=_(
            u'Google News requires a logo image to be linked in the feed. '
            u'The image must follow the specifications defined in the '
            u'<a href="{0}">feed guidelines</a>.'.format(EDITORS_PICKS_HELP)
        ),
        required=False,
        constraint=validate_logo,
    )


class GoogleNewsGroup(group.Group):

    """Default settings group."""

    label = _(u'Default')
    description = _('Default Configuration')
    fields = field.Fields(GoogleNewsSettings)


class GoogleNewsEditorsPicksGroup(group.Group):

    """Editor Picks settings group."""

    label = _(u"Editors' Picks")
    description = _("Editors' Picks Configuration")
    fields = field.Fields(IGoogleNewsEditorsPicksSettings)


class IGoogleNewsSchema(GoogleNewsSettings, IGoogleNewsEditorsPicksSettings):

    """Schema for all groups configuration."""
