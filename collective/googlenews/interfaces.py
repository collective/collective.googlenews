# -*- coding: utf-8 -*-
from collective.googlenews import _
from collective.googlenews.utils import validate_logo
from plone.directives import form
from zope import schema
from zope.interface import Interface

EDITORS_PICKS_LINK = u'https://support.google.com/news/publisher/answer/1407682'


class IGoogleNewsLayer(Interface):

    """Browser layer for this addon"""


class GoogleNewsSettings(form.Schema):

    """Main settings of this addon"""

    # XXX: default value is declared at profiles/default/registry.xml
    portal_types = schema.List(
        title=_(u'Portal types'),
        description=_(u'Select portal types that will be considered news articles.'),
        value_type=schema.Choice(
            vocabulary=u'plone.app.vocabularies.ReallyUserFriendlyTypes'),
    )

    logo = schema.ASCII(
        title=_(u'Logo image'),
        description=_(
            u"Google News requires Editors' Picks feed logos to follow some "
            u'<a href="{0}">general guidelines</a>. This image will replace '
            u'the logo in all Atom feeds on the site.'.format(EDITORS_PICKS_LINK)
        ),
        required=False,
        constraint=validate_logo,
    )
